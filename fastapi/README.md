## FastAPI + Docker + GitHub Actions

# 🚀 ML API with FastAPI + Docker + GitHub Actions

## 📁 專案結構

```
.
├── app/
│   └── main.py               # FastAPI 服務端點
├── models/
│   └── model.pt              # 預先訓練好的模型（須自行準備）
├── requirements.txt          # 依賴套件
├── Dockerfile                # Docker 打包設定
└── .github/
    └── workflows/
        └── ci.yml            # GitHub Actions CI 設定
```

---

## 📦 安裝與啟動

### 1️⃣ 使用 Python 啟動 API

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2️⃣ 使用 Docker 啟動 API

```bash
docker build -t fastapi-ml .
docker run -p 8000:8000 fastapi-ml
```

---

## 🔍 測試 API
1. 啟動 API
2. 執行 test/test.py


test