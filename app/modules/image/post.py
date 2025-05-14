import requests
with open("0RZPD93P2SUQ.jpg", "rb") as f:
    image_data = f.read()

res = requests.post(
    url="http://127.0.0.1:5000/analyze_frame",
    data=image_data,
    headers={"Content-Type": "application/octet-stream"}
)

print(res.json())
