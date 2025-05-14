3 Tutorials
1. 使用 MLflow 紀錄模型參數
2. 使用 DVC 切換不同資料版本
3. 使用  DVC + MLflow 管理資料與實驗版本

## 0. RequirementS

1. 準備資料：

    ```bash
    python load_data.py
    ```
2. 準備模型 `train.py`

## 📌 1. 使用 MLflow 紀錄模型參數

1. 訓練模型前使用 MLflow 記錄於參數：

    ```bash
    python train.py
    ```

---

## 📌 2. 使用 DVC 切換不同資料版本

### ✅ 資料版本需求

請確認已放入以下版本資料：

* `data/diabetes_v1.csv`
* `data/diabetes_v2.csv`

### ✅ 添加資料版本至 Git + DVC

```bash
# 建立版本 1 分支
git checkout main   # 回到主線
git checkout -b data-v1
cp data/diabetes_v1.csv data/diabetes.csv
dvc add data/diabetes.csv
git commit -am "Add data version 1"
git push -u origin data-v1

# 建立版本 2 分支
git checkout main   # 回到主線
git checkout -b data-v2
cp data/diabetes_v2.csv data/diabetes.csv
dvc add data/diabetes.csv
git commit -am "Add data version 2"
git push -u origin data-v2
```

### ✅ 切換資料版本

```bash
# 切換到版本 1
git checkout data-v1
dvc checkout    # 還原 v1 資料

# 切換到版本 2
git checkout data-v2
dvc checkout    # 還原 v2 資料
```

> `dvc checkout` 會根據當前 Git commit 的 `.dvc` 文件，還原對應版本的資料檔案。

### ✅ 驗證切換後的資料版本是否一致

1. 執行：

   ```bash
   python check_data_version.py
   ```

2. 輸出會顯示：

   ```bash
   📦 Data file hash     : <md5-from-file>
   📄 DVC tracked hash   : <md5-from-.dvc>
   ✅ Hash match!
   ```

> 若出現 `❌ Hash mismatch!` 表示切換或還原未成功。

## 3. 使用  DVC + MLflow 管理資料與實驗版本

### 🧱 專案目錄結構

```
.
├── data/
│   └── diabetes.csv            # 透過 DVC 管理的資料
├── params.yaml                 # 訓練參數（learning rate、epochs）
├── train.py                    # 主要訓練程式
├── finetune.py                 # finetune 程式
├── dvc.yaml                    # DVC pipeline 定義
├── dvc.lock                    # pipeline 結果紀錄
├── mlruns/                     # MLflow 儲存實驗結果
└── models/
    └── model.pt                # 模型輸出（DVC 管理）
```

`params.yaml`：管理超參數

```yaml
train:
  lr: 0.01
  epochs: 100
```

---

`dvc.yaml`：定義 pipeline

如何產生 `dvc.yaml` + `dvc.lock`?
```bash
dvc stage add -n train --force `
  -d train.py `
  -d data/diabetes.csv `
  -o models/model.pt `
  -p train.lr,train.epochs `
  python train.py
```
>* 哪些輸入（`-d`）決定輸出
* 哪些超參數（`-p`）追蹤
* 哪些是輸出（`-o`）模型結果

---

### 🚀 執行訓練實驗

```bash
dvc repro

# 跑不同超參數
dvc exp run --set-param train.lr=0.001
dvc exp run --set-param train.lr=0.01
dvc exp show
```

### 📦 使用 MLflow 查看實驗記錄

```bash
mlflow ui
```

前往瀏覽器 `http://localhost:5000` 查看每次實驗的超參數與 RMSE。

---

### 🔁 資料切換

```bash
# 建立版本 1 分支
git checkout main   # 回到主線
git checkout -b data-v1.1
cp data/diabetes_v1.csv data/diabetes.csv
dvc add data/diabetes.csv
git commit -am "Add data version 1"
git push -u origin data-v1.1

# 建立版本 2 分支
git checkout main   # 回到主線
git checkout -b data-v2.1
cp data/diabetes_v2.csv data/diabetes.csv
dvc add data/diabetes.csv
git commit -am "Add data version 2"
git push -u origin data-v2.1
```

切換到某個資料：

```bash
# 切換到版本 1
git checkout data-v1.1
dvc checkout

# 切換到版本 2
git checkout data-v2.1
dvc checkout
```

### 🔁 模型取用

切換到某個模型版本：
>`finetune.py`

```python
model_uri = f"runs:/{run_id}/model"
model = mlflow.pytorch.load_model(model_uri)
```