import requests

# 测试数据 - 请根据你的数据库实际情况调整这些ID
test_data = {
    "child_id": 1,          # 存在的儿童ID
    "therapist_id": 101,    # 存在的心理师ID
    "assigned_at": "2023-05-15T10:30:00"  # 分配时间
}

# 确保 FastAPI 后端在 http://127.0.0.1:8000 上运行
base_url = "http://127.0.0.1:8000"
api_url = f"{base_url}/doctor/{test_data['child_id']}/{test_data['therapist_id']}"

# 发送 POST 请求
print(f"Testing API: POST {api_url}")
response = requests.post(
    api_url,
    json={"assigned_at": test_data["assigned_at"]}
)

# 输出 API 响应内容
if response.status_code == 201:
    print("✅ 关联创建成功")
    print("响应数据:", response.json())
elif response.status_code == 404:
    print("❌ 未找到儿童或心理师")
    print("错误详情:", response.json())
elif response.status_code == 400:
    print("❌ 请求数据无效")
    print("错误详情:", response.json())
else:
    print(f"❌ 请求失败，状态码: {response.status_code}")
    print("响应内容:", response.text)
