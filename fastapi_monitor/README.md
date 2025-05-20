# 🔍 使用 Prometheus + Grafana 監控 FastAPI

這個架構可用於監控 FastAPI 應用程式的各種指標（例如請求次數、預測結果分布、錯誤率），其中：

- **Prometheus** 負責定期收集 `/metrics` 中暴露的數據
- **Grafana** 則用來進行圖形化顯示與觀察趨勢

---

## 📁 專案目錄結構

```

your-project/
├── fastapi/
│   └── app.main\_wmonitor.py     # FastAPI 程式，提供 /metrics
│   └── models/
│       └── model.pt                 # 預訓練模型（需自行提供）
│   └── test/
│       └── test.py                  # 測試 FastAPI API 的腳本
│   └── requirements.txt             # Python 套件清單
│   └── Dockerfile                   # FastAPI 的 Docker 打包檔
├── monitoring/
│   ├── prometheus.yml           # Prometheus 設定檔
│   └── docker-compose.yml       # 啟動 Prometheus + Grafana 的 Docker 配置

```

---

## ⚙️ 步驟一：設定 Prometheus

### `monitoring/prometheus.yml`

```yaml
# prometheus.yml 裡加上你的 FastAPI
global:
  scrape_interval: 5s
  
scrape_configs:
  - job_name: "fastapi"
    static_configs:
      - targets: ["fastapi:8000"]
```

> 📌 說明：`host.docker.internal` 是 Docker container 連接宿主機的方式（適用於 Windows/macOS）

---

## 🐳 步驟二：使用 Docker 啟動 Prometheus + Grafana

### `monitoring/docker-compose.yml`

```yaml
version: "3"

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

### 啟動方式：

```bash
cd monitoring
docker compose up -d
```

---

## 🚀 步驟三：啟動 FastAPI 服務

在另一個終端機執行：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

請確保你的 FastAPI 中有透過 `prometheus_client` 暴露 `/metrics`。

---

## 🌐 步驟四：開啟以下介面

* **Prometheus**: [http://localhost:9090](http://localhost:9090)
* **Grafana**: [http://localhost:3000](http://localhost:3000)

  * 預設帳號密碼：`admin / admin`

---

## 📊 步驟五：設定 Grafana Dashboard

1. 點選左側齒輪 → Data Sources → 新增 **Prometheus**

   * URL：`http://prometheus:9090`（Docker 內部）或 `http://localhost:9090`（外部）
2. 建立新 Dashboard → 新增 Panel
3. 使用 PromQL 查詢指標：

### PromQL 查詢範例：

#### ✅ RMSE（模型預測誤差）總和

```promql
validation_rmse_sum
```

#### ✅ 模型輸出預測值的中位數（Histogram Quantile）

```promql
histogram_quantile(0.5, rate(prediction_distribution_bucket[5m]))
```

> 📌 `rate(X[5m])`：計算最近 5 分鐘 X 每秒變化速率
> 📌 `histogram_quantile(0.5, ...)`：計算中位數（P50），也可改為 P90、P95 觀察尾部

---

## ✅ 工具與角色總覽

| 工具         | Port | 功能說明                           |
| ---------- | ---- | ------------------------------ |
| FastAPI    | 8000 | 提供 `/predict` 與 `/metrics` API |
| Prometheus | 9090 | 抓取並儲存指標資料                      |
| Grafana    | 3000 | 將指標視覺化、繪製圖表                    |

```