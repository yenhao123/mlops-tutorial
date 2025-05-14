## 📌 1. 訓練模型

請依序執行以下步驟：

1. 載入資料並前處理：

   ```bash
   python load_data.py
   ```
2. 使用 PyTorch 訓練模型並記錄於 MLflow：

   ```bash
   python mlflow_pytorch.py
   ```

---

## 📌 2. 切換不同資料版本

### ✅ 資料版本需求

請確認已放入以下版本資料：

* `data/diabetes_v1.csv`
* `data/diabetes_v2.csv`

### ✅ 添加資料版本至 Git + DVC

```bash
# 版本 1
cp data/diabetes_v1.csv data/diabetes.csv
dvc add data/diabetes.csv
git commit -am "Add v1 data"
git push

# 版本 2
cp data/diabetes_v2.csv data/diabetes.csv
dvc add data/diabetes.csv
git commit -am "Add v2 data"
git push
```

### ✅ 切換資料版本

```bash
# 切換到版本 1 的 commit
git checkout <commit-v1>
dvc checkout    # 還原 v1 資料

# 切換到版本 2 的 commit
git checkout <commit-v2>
dvc checkout    # 還原 v2 資料
```

> `dvc checkout` 會根據當前 Git commit 的 `.dvc` 文件，還原對應版本的資料檔案。

### ✅ 驗證切換後的資料版本是否一致
1. 執行 check_data_version.py
2. 判斷是否 Hash match


