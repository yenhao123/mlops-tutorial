## 📘 MLOps Overview

### 🔍 什麼是 MLOps？

MLOps（Machine Learning Operations）是 DevOps 的一種延伸，專門用於機器學習模型的開發、部署與維運。其核心目標是讓整個 ML 流程更具**自動化**與**可重現性**，確保模型的可靠性與可擴展性。

---

### 🚧 常見挑戰與解法

| 挑戰類型       | 問題描述                | 解法建議與工具                                   |
| ---------- | ------------------- | ----------------------------------------- |
| 實驗難以追蹤     | 訓練參數與結果繁雜，版本混亂      | 使用 DVC 或 MLflow 進行版本控制與追蹤                 |
| 模型部署複雜     | 不同客戶與部署情境需求不同，缺乏彈性  | 使用 FastAPI + Docker + K8s 部署              |
| 模型難以監控     | 無法即時掌握推論錯誤或資料漂移     | 使用 Prometheus + Grafana 進行指標監控            |
| retrain 不穩 | retrain 頻繁出錯，人工操作繁瑣 | 使用 Airflow / Kubeflow 建構 retrain pipeline |

---

### 🔁 MLOps Lifecycle

#### 📦 Develop 階段

**1️⃣ Data Version Control**

* 資料、模型、程式都需版本控制（如 Git）
* 可支援雲端儲存（S3, GDrive...）
* 🔧 工具：DVC

**2️⃣ Experiment Tracking**

* 記錄參數、metrics、模型 artifact
* 統一格式建構專案與訓練流程
* 🔧 工具：MLflow Tracking / Projects / Models / Registry

#### 🚀 Deploy 階段

**Infrastructure 層面**

* 提供模型部署所需的計算與儲存資源（如 AWS、Azure）

**Customer 層面**（平台需滿足）：

* ✅ Load Balancing（負載平衡）
* ✅ Resource Control（資源限制）
* ✅ Self-Healing（容錯能力）
* ✅ Isolation（隔離不同使用者）
* ✅ Rolling Updates（不中斷更新）

🔧 工具：Docker、Kubernetes、FastAPI

#### 📈 Monitor 階段

\*\*目的：\*\*追蹤線上模型效能與異常狀況，以支援 retrain 或 rollback

**監控重點指標：**

| 分類       | 內容範例                                       |
| -------- | ------------------------------------------ |
| 模型效能     | 準確率、RMSE、AUC、F1-score（需標記資料）               |
| 資料漂移     | 特徵分布變化、JSD/KS/Wasserstein 距離等              |
| 輸出分布     | 分類比例異常、預測分佈偏斜                              |
| API 回應延遲 | latency / throughput / error rate（SLO/SLA） |

🔧 工具：Prometheus + Grafana、SageMaker Model Monitor