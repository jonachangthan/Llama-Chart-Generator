import streamlit as st
from groq import Groq, AuthenticationError, APIConnectionError
from streamlit_mermaid import st_mermaid
from utils import parse_response_for_mermaid

# --- 1. 頁面設定 ---
st.set_page_config(page_title="Groq 視覺化圖表助手", page_icon="📊", layout="wide")

# --- 2. 輔助函式：驗證 API Key ---
def validate_api_key(key):
    """
    嘗試連線 Groq API 以驗證 Key 是否有效
    """
    try:
        temp_client = Groq(api_key=key)
        temp_client.models.list() # 嘗試發送請求測試
        return True, None
    except AuthenticationError:
        return False, "❌ 驗證失敗：API Key 無效，請檢查是否複製完整 (需包含 gsk_ 前綴)。"
    except APIConnectionError:
        return False, "❌ 連線失敗：無法連接 Groq 伺服器，請檢查網路。"
    except Exception as e:
        return False, f"❌ 發生未預期的錯誤：{str(e)}"

# --- 3. 側邊欄：登入與設定 ---
with st.sidebar:
    st.title("📊 Groq 圖表助手")
    st.markdown("基於 **Llama 3.3** 與 **Mermaid.js** 技術")
    
    # 初始化 session state
    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = None

    # --- API Key 管理區 ---
    if not st.session_state.groq_api_key:
        # 1. 自動檢查 Secrets
        if "GROQ_API_KEY" in st.secrets:
            valid, msg = validate_api_key(st.secrets["GROQ_API_KEY"])
            if valid:
                st.session_state.groq_api_key = st.secrets["GROQ_API_KEY"]
                st.success("已自動載入系統 Key ✅")
                st.rerun()
            else:
                st.error("系統預設 Key 無效。")

        # 2. 手動輸入
        user_input_key = st.text_input("請輸入 Groq API Key", type="password", placeholder="gsk_...")
        
        if st.button("驗證並登入"):
            if not user_input_key:
                st.warning("請輸入內容！")
            else:
                with st.spinner("正在驗證金鑰..."):
                    is_valid, error_msg = validate_api_key(user_input_key)
                
                if is_valid:
                    st.session_state.groq_api_key = user_input_key
                    st.success("登入成功！")
                    st.rerun()
                else:
                    st.error(error_msg)
        st.caption("還沒有 Key？[點此免費申請](https://console.groq.com/keys)")
        
    else:
        st.success("🟢 API 連線狀態：正常")
        if st.button("登出 / 更換 Key"):
            st.session_state.groq_api_key = None
            st.session_state.messages = []
            st.rerun()
            
    st.divider()
    
    # --- 新增功能：除錯模式 ---
    debug_mode = st.checkbox(
        "🛠️ 開啟 Mermaid 除錯模式", 
        value=False, 
        help="勾選後，會顯示原始圖表代碼，方便檢查語法錯誤 (Syntax Error)。"
    )

    st.divider()
    if st.button("🗑️ 清除對話紀錄"):
        st.session_state.messages = []
        st.rerun()

# --- 4. 主程式邏輯 ---
st.title("📊 Groq + Mermaid 自動圖表生成器")

# 未登入時的引導畫面
if not st.session_state.groq_api_key:
    st.info("⬅️ 請先在左側邊欄輸入 API Key 才能開始使用。")
    st.markdown("""
    ### 功能介紹
    本系統利用 **Groq LPU** 加速推論，能將你的想法轉化為視覺化圖表：
    - 🔄 **流程圖** (Flowcharts)
    - ⏱️ **時序圖** (Sequence Diagrams)
    - 🧠 **心智圖** (Mindmaps)
    """)
    st.stop()

# 已登入，初始化 Client
client = Groq(api_key=st.session_state.groq_api_key)

# --- 核心靈魂：System Prompt (針對 Mermaid 語法優化版) ---
SYSTEM_PROMPT = """
你是一位擅長使用視覺化圖表來解釋複雜概念的專家。
你的目標是協助用戶理解資訊，必要時主動產生 Mermaid.js 圖表代碼。

【絕對關鍵規則】(違反會導致系統報錯)
1. **所有節點文字和標籤，如果包含中文、空格或特殊符號，必須使用雙引號 (") 包裹。**
   - 錯誤: A[開始] --> B{是否成功?}
   - 正確: A["開始"] --> B{"是否成功?"}
2. 請使用最基礎、穩定的 Mermaid 語法。
3. 嚴格將 Mermaid 代碼包裹在 ```mermaid 和 ``` 區塊中。

【一般規則】
1. 當用戶詢問流程、架構、比較或時間軸時，請優先使用圖表輔助。
2. 圖表前後請提供簡短的繁體中文解釋。

【推薦範例】
- 流程圖: graph TD; A["開始"] --> B{"判斷"}; B -- "是" --> C["執行"];
- 時序圖: sequenceDiagram; User->>System: "請求"; System-->>User: "回應";
- 心智圖: mindmap; root(("核心")); I1["分支"];
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- 顯示歷史紀錄 ---
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            parsed_parts = parse_response_for_mermaid(message["content"])
            for part in parsed_parts:
                if part["type"] == "text":
                    st.markdown(part["content"])
                elif part["type"] == "mermaid":
                    # 除錯顯示
                    if debug_mode:
                        st.caption("🛠️ [Debug] 原始代碼:")
                        st.code(part["content"], language="mermaid")
                    
                    st_mermaid(part["content"], height="300px")

# --- 處理輸入 ---
if prompt := st.chat_input("試試問：畫一個使用者註冊的流程圖"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Llama 3.3 正在構思圖表..."):
            try:
                # 使用最新的 Llama 3.3 模型
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.3, # 降低溫度以提高語法穩定性
                    max_tokens=2048,
                    stream=False 
                )
                full_response = completion.choices[0].message.content
                
                # 解析並顯示
                parsed_parts = parse_response_for_mermaid(full_response)
                for part in parsed_parts:
                    if part["type"] == "text":
                        st.markdown(part["content"])
                    elif part["type"] == "mermaid":
                        # 除錯顯示
                        if debug_mode:
                            st.caption("🛠️ [Debug] 原始代碼:")
                            st.code(part["content"], language="mermaid")
                        
                        st_mermaid(part["content"])
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"推論過程發生錯誤：{str(e)}")