1. 執行 `load_data.py`
2. 執行 `mlflow_pytorch.py`

# 初始版本
cp data/diabetes_v1.csv data/diabetes.csv
dvc add data/diabetes.csv
git commit -am "Add v1 data"

# 另一版
cp data/diabetes_v2.csv data/diabetes.csv
dvc add data/diabetes.csv
git commit -am "Add v2 data"
