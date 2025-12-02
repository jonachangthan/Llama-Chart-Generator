import re

def parse_response_for_mermaid(response_text):
    """
    解析 AI 的文字回應，找出被 ```mermaid ... ``` 包裹的代碼塊。
    
    Args:
        response_text (str): AI 的完整回應字串。
        
    Returns:
        list: 一個列表，包含字典元素。
              例如: [{'type': 'text', 'content': '你好...'}, {'type': 'mermaid', 'content': 'graph TD; A-->B;'}]
    """
    # 定義正規表示式模式，用來捕捉 mermaid 區塊
    # r'(```mermaid\n[\s\S]*?\n```)'
    # \s\S 確保匹配包括換行符在內的所有字符
    # *? 非貪婪匹配，確保找到最短的閉合區塊
    pattern = r'(```mermaid\n[\s\S]*?\n```)'
    
    # 使用 re.split 切割字串，因為模式中有括號 ()，所以分割符本身也會被保留下來
    parts = re.split(pattern, response_text)
    
    parsed_content = []
    for part in parts:
        if not part.strip():
            continue
            
        if part.startswith("```mermaid") and part.endswith("```"):
            # 這是一個 mermaid 區塊，移除前後的標記與換行
            mermaid_code = part.replace("```mermaid\n", "").replace("\n```", "").strip()
            parsed_content.append({"type": "mermaid", "content": mermaid_code})
        else:
            # 這是一般文字
            parsed_content.append({"type": "text", "content": part})
            
    return parsed_content