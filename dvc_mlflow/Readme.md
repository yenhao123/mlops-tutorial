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
# 切換到版本 1 的 commit
git checkout data-v1
dvc checkout    # 還原 v1 資料

# 切換到版本 2 的 commit
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
