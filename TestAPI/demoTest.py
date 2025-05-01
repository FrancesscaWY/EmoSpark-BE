import requests

# 发送测试数据
test_data = {
    "value": 10  # 你可以修改这个值进行其他测试
}

# 确保 FastAPI 后端在 http://127.0.0.1:8000 上运行
url = "http://127.0.0.1:8000/check_even"

# 发送 POST 请求
response = requests.post(url, json=test_data)

# 输出 API 响应内容
if response.status_code == 200:
    print("Response JSON:", response.json())  # 打印响应数据
else:
    print(f"Request failed with status code {response.status_code}")
