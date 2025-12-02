# Streamlit x Groq Visualizer Demo

## 專案簡介
這是 Taica AIGC 課程模組四的延伸實作。
本專案解決了 Streamlit Cloud 無法運行本地 LLM 的問題，並透過 **Groq API** 整合 **Mermaid.js**，打造了一個能自動畫圖的 AI 助手。

## 核心技術
- **模型**：Llama 3.3-70b-versatile (via Groq LPU)
- **前端**：Streamlit
- **視覺化**：Mermaid.js + Regex Parsing
- **特點**：免費、極速、支援自動圖表生成

## 如何執行
1. 申請 [Groq API Key](https://console.groq.com/keys)。
2. 安裝套件：`pip install -r requirements.txt`
3. 執行：`streamlit run app.py`

## 如何使用
1. 在首頁輸入Groq API Key
2. 進入後即可**對話**並且能將你的**想法轉化為視覺化圖表**
3. Llama 3.3 偶爾會「幻覺」出錯誤的 Mermaid 語法，導致無法生成圖表出現錯誤

## 排除錯誤
1. 重新整理你的 Streamlit 網頁。
2. 在側邊欄勾選 「🛠️ 開啟 Mermaid 除錯模式」。
3. 再次嘗試要求 AI 畫圖。
4. 如果還是出現 "Syntax error"，請看圖表上方的黑色代碼區塊。(可將那段代碼複製起來，貼到線上的 Mermaid Live Editor。這個網站會明確告訴你哪一行語法錯了)
