import os
from sklearn.datasets import load_diabetes
import pandas as pd

# ======== 1. 載入與儲存資料（可追蹤） ========
X, y = load_diabetes(return_X_y=True)
feature_names = load_diabetes().feature_names

# 儲存資料為 CSV，讓 DVC 可追蹤
os.makedirs("data", exist_ok=True)
data = pd.DataFrame(X, columns=feature_names)
data['target'] = y
data.to_csv("data/diabetes.csv", index=False)