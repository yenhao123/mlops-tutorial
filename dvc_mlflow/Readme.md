# 📚 MLOps Tutorials: DVC + MLflow 實作指南

本專案展示如何使用 DVC 和 MLflow 搭配進行機器學習實驗管理，涵蓋：

### 🧪 教學主題：

1. 使用 MLflow 紀錄模型參數與指標
2. 使用 DVC 切換不同資料版本
3. 使用 DVC + MLflow 管理整體實驗與資料版本

---

## ⚙️ 0. Requirements

1. 建立初始資料：

   ```bash
   python load_data.py
   ```

2. 準備訓練程式：

   ```bash
   python train.py
   ```

---

## 📌 1. 使用 MLflow 紀錄模型參數

1. 執行訓練程式，MLflow 將自動記錄：

   ```bash
   python train.py
   ```

2. 啟動 MLflow UI 查看實驗記錄：

   ```bash
   mlflow ui
   ```

   前往：`http://localhost:5000`

---

## 📌 2. 使用 DVC 切換不同資料版本

### ✅ 資料需求：

請將以下資料放入 `data/` 資料夾：

* `data/diabetes_v1.csv`
* `data/diabetes_v2.csv`

### ✅ 建立資料版本分支並追蹤：

```bash
# 建立資料版本 1 分支
git checkout -b data-v1
cp data/diabetes_v1.csv data/diabetes.csv
dvc add data/diabetes.csv
git add data/diabetes.csv.dvc .gitignore
git commit -m "Add data version 1"
git push -u origin data-v1

# 建立資料版本 2 分支
git checkout main
git checkout -b data-v2
cp data/diabetes_v2.csv data/diabetes.csv
dvc add data/diabetes.csv
git add data/diabetes.csv.dvc
git commit -m "Add data version 2"
git push -u origin data-v2
```

### ✅ 切換資料版本：

```bash
# 切換至資料版本 1
git checkout data-v1
dvc checkout

# 切換至資料版本 2
git checkout data-v2
dvc checkout
```

### ✅ 驗證資料一致性：

```bash
python check_data_version.py
```

若輸出：

```
✅ Hash match!
```

代表資料與 DVC 記錄一致。

---

## 📌 3. 使用 DVC + MLflow 管理實驗與資料版本

### 📁 專案結構：

```
.
├── data/                  # 資料集
├── models/                # 輸出模型
├── params.yaml            # 訓練參數
├── train.py               # 訓練程式
├── dvc.yaml               # DVC pipeline 定義
├── dvc.lock               # Pipeline 鎖檔
├── mlruns/                # MLflow 實驗紀錄
```

### `params.yaml`（管理超參數）：

```yaml
train:
  lr: 0.01
  epochs: 100
```

### 🔧 建立 DVC Pipeline：

```bash
dvc stage add -n train --force \
  -d train.py \
  -d data/diabetes.csv \
  -o models/model.pt \
  -p train.lr,train.epochs \
  python train.py
```

---

### 🚀 執行實驗：

```bash
dvc repro                                # 使用預設參數訓練
dvc exp run --set-param train.lr=0.001   # 改變學習率進行實驗
dvc exp show                             # 顯示各實驗結果
```

---

### 📊 MLflow UI：

```bash
mlflow ui
```

> 進入 `http://localhost:5000` 查看每次實驗記錄（包括參數與 RMSE）

---

## 🔁 切換資料與模型版本（建議搭配 Git 分支）

### 切換資料版本：

```bash
git checkout data-v1
dvc checkout

git checkout data-v2
dvc checkout
```

### 載入指定實驗模型（`finetune.py`）：

```python
model_uri = f"runs:/{run_id}/model"
model = mlflow.pytorch.load_model(model_uri)
```

## 📌 4. 使用 Wrapper 讓 MLflow 更易用

### ❓ 問題：為什麼需要 Wrapper？

MLflow 雖然功能強大，但需要在訓練程式中手動嵌入大量 logging 語法
---

### 📦 準備內容：

* `mlflow_wrapper.py`：封裝 MLflow 操作的函式
* `params.yaml`：記錄訓練參數

範例 `params.yaml`（若尚未建立）：

```yaml
train:
  lr: 0.01
  epochs: 100
```

---

### 🧪 使用方式：

將原本的訓練入口改為：

```python
from mlflow_wrapper import run_with_mlflow_from_yaml

run_with_mlflow_from_yaml(
    script="train.py",
    yaml_path="params.yaml",
    section="train",
    artifacts=["models/model.pt"]
)
```