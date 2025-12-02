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

## 部署至 Streamlit Cloud
請在部署設定的 Secrets 欄位填入：
GROQ_API_KEY = "你的_gsk_金鑰"