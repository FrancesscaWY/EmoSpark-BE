import requests

# 配置区（必须修改！）===============================================
API_KEY = "i9bkgztwIm4EjytCTcqizHm8"  # 从百度智能云控制台获取
SECRET_KEY = ("zSKa2rlTHLQY32LiNidWiag77Rt5UzfG")
# ===============================================================

# 初始化全局变量
access_token = None
emotion_keywords = {
    "快乐": ["开心", "高兴", "快乐", "幸福", "哈哈", "喜欢"],
    "悲伤": ["伤心", "难过", "哭泣", "悲痛", "泪流满面", "心碎"],
    "恐惧": ["害怕", "恐怖", "吓人", "恐慌", "心惊胆战", "恐惧"],
    "生气": ["生气", "愤怒", "发火", "气死", "怒火", "暴躁"],
    "惊讶": ["惊讶", "震惊", "居然", "想不到", "天啊", "竟然"],
    "厌恶": ["恶心", "讨厌", "嫌弃", "反感", "吐了", "厌恶"],
}


# 获取百度API访问令牌
def get_access_token():
    global access_token
    try:
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": API_KEY,
            "client_secret": SECRET_KEY
        }
        response = requests.get(url, params=params, timeout=10).json()
        access_token = response["access_token"]
    except Exception as e:
        print(f"[错误] 获取access_token失败: {str(e)}")


# 调用情感倾向分析API
def analyze_emotion(text):
    if not access_token:
        get_access_token()

    try:
        url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify"
        headers = {"Content-Type": "application/json"}
        payload = {
            "text": text[:1024],  # 遵守百度API文本长度限制
            "access_token": access_token
        }
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()  # 检查HTTP错误状态码
        return response.json()
    except Exception as e:
        print(f"[错误] API请求异常: {str(e)}")
        return {}


# 七种情绪分类逻辑
def detect_emotion(text):
    if not text.strip():
        return "没有情绪"

    # 调用百度API
    result = analyze_emotion(text)

    # 调试输出（可注释）
    print("[调试信息] 百度API返回:", result)

    # 处理API错误码
    if "error_code" in result:
        return f"API错误: {result['error_msg']}(code:{result['error_code']})"

    # 解析情感结果
    try:
        sentiment = result["items"][0]["sentiment"]  # 0-中性，1-正向，2-负向
    except KeyError:
        return "数据解析失败，请检查API权限"

    # 情绪分类逻辑
    if sentiment == 1:
        return "快乐"
    elif sentiment == 0:
        return "没有情绪"
    else:  # 负向情绪细化分类
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                return emotion
        return "生气"  # 默认负向情绪


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        "终于拿到冠军了，太兴奋了！",  # 快乐
        "这服务态度让我非常愤怒！",  # 生气
        "看到车祸现场我浑身发抖...",  # 恐惧
        "今天天气不错。",  # 没有情绪
        "这虫子太恶心了！",  # 厌恶
    ]

    for text in test_cases:
        print(f"文本：「{text}」")
        print(f"情绪：{detect_emotion(text)}\n")