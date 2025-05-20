# 🔍 FastAPI Monitoring with Prometheus + Grafana

This setup enables monitoring your FastAPI application's metrics (e.g. request count, prediction distribution, error rate) using **Prometheus** for metric collection and **Grafana** for visualization.

---

## 📁 Folder Structure

```
your-project/
├── fastapi/
│   └── app.main\_wmonitor.py     # FastAPI app exposing /metrics
├── monitoring/
│   ├── prometheus.yml
│   └── docker-compose.yml
```

---

## ⚙️ Step 1: Configure Prometheus

### `monitoring/prometheus.yml`

```yaml
global:
  scrape_interval: 5s
  
scrape_configs:
  - job_name: "fastapi"
    static_configs:
      - targets: ["host.docker.internal:8000"]
```

>Note: `host.docker.internal` allow docker to connect Host

---

## 🐳 Step 2: Run Prometheus + Grafana with Docker

### `monitoring/docker-compose.yml`

```yaml
version: '3'

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

### Launch the services:

```bash
cd monitoring
docker compose up -d
```

---

## 🚀 Step 3: Launch Your FastAPI App

In another terminal:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Make sure your FastAPI app exposes a `/metrics` endpoint using `prometheus_client`.

---

## 🌐 Step 4: Access the Interfaces

* **Prometheus**: [http://localhost:9090](http://localhost:9090)
* **Grafana**: [http://localhost:3000](http://localhost:3000)
  * Default login: `admin / admin`

---

## 📊 Step 5: Configure Grafana

1. Add **Prometheus** as a data source (`http://prometheus:9090` inside Docker, or `http://localhost:9090` if external).
2. Create a new **Dashboard** → **Add Panel**.
3. Use PromQL queries to visualize metrics:

### Sample PromQL queries:

* RMSE:

  ```promql
  validation_rmse_sum
  ```

* 預測值的變化趨勢

    ```promql
    histogram_quantile(0.5, rate(prediction_distribution_bucket[5m]))
    ```

Note: 
rate(X[5m]) 表示：計算最近 5 分鐘，X 的 每秒變化率，。
histogram_quantile(0.5, ...): 中位數
---

## ✅ Summary

| Tool       | Port | Role                       |
| ---------- | ---- | -------------------------- |
| FastAPI    | 8000 | API service with /metrics  |
| Prometheus | 9090 | Scrapes and stores metrics |
| Grafana    | 3000 | Visualizes metrics         |
---