import requests

# 模擬輸入資料與實際標籤
features = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
label = 2.0

# 發送 /validate 請求
val_url = "http://127.0.0.1:8000/validate"
val_payload = {"features": features, "label": label}

val_response = requests.post(val_url, json=val_payload)

print("🧪 Validation Response:")
print(val_response.json())
