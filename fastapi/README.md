# 🚀 ML API with FastAPI + Docker + GitHub Actions

## 📁 專案結構

```
.
├── app/
│   └── main.py               # FastAPI 服務端點
├── models/
│   └── model.pt              # 預先訓練好的模型（須自行準備）
├── test/
│   └── test.py               # test 測試檔
├── requirements.txt          # 依賴套件
├── Dockerfile                # Docker 打包設定
└── .github/
    └── workflows/
        └── ci.yml            # GitHub Actions CI 設定
```
>.github 要放在更目錄層

---

## 📦 安裝與啟動

兩種方法:

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

### 1️⃣ 使用本地 `test/test.py` 測試

1. 啟動 API（使用 Python 或 Docker）：

   ```bash
   uvicorn app.main:app --reload
   ```

   或：

   ```bash
   docker run -p 8000:8000 fastapi-ml
   ```

2. 執行測試腳本（需先安裝 `requests` 套件）：

   ```bash
   python test/test.py
   ```

3. 預期會輸出：

   ```text
   ✅ Response: 200
   🔍 Content: {"prediction": ...}
   ```

> 📌 `test/test.py` 中會向 `/predict` 發送一筆特徵資料並印出回應結果。

---

### 2️⃣ 使用 GitHub Actions 自動測試

每次執行以下任一動作，CI 都會自動啟動並測試 `/predict` API 是否回應成功：

* 推送 (`git push`) 到 `main` 分支
* 發送 Pull Request 到 `main`

CI 會自動完成：

* 建立 Python 環境並安裝依賴
* 啟動 FastAPI 伺服器
* 執行 `test/test.py` 測試推論
* 回報結果（成功 / 失敗）

你可以在 GitHub 網站上點選 `Actions` 分頁檢查每次執行狀態與輸出 log。