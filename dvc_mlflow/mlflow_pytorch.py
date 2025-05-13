import os
import pandas as pd
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

import mlflow
import mlflow.pytorch

import subprocess

# ======== 1. 載入與儲存資料（可追蹤） ========
# 從 CSV 讀入資料
df = pd.read_csv("data/diabetes.csv")
X = df.drop(columns=["target"]).values
y = df["target"].values
feature_names = df.columns.drop("target")

print("✅ 已從 data/diabetes.csv 載入資料")

# ======== 2. 資料預處理 ========
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

train_loader = DataLoader(TensorDataset(X_train_tensor, y_train_tensor), batch_size=32, shuffle=True)

# ======== 3. 建立模型 ========
class Net(nn.Module):
    def __init__(self, in_features):
        super(Net, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.net(x)

model = Net(in_features=X.shape[1])
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# ======== 4. 開始 MLflow 實驗記錄 ========
with mlflow.start_run():
    for epoch in range(100):
        model.train()
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(batch_X), batch_y)
            loss.backward()
            optimizer.step()

    # 評估
    model.eval()
    with torch.no_grad():
        preds = model(X_test_tensor)
        mse = mean_squared_error(y_test, preds.numpy())
        rmse = np.sqrt(mse)


    # 記錄到 MLflow
    mlflow.log_param("epochs", 100)
    mlflow.log_param("lr", 0.01)
    mlflow.log_metric("rmse", rmse)
    mlflow.pytorch.log_model(model, "model")
    print(f"📈 Logged RMSE: {rmse:.3f}")

# ======== 5. （選擇性）使用 subprocess 執行 DVC 操作 ========
# 若你尚未初始化 DVC，可打開下列註解：
# subprocess.run("dvc init", shell=True)
# subprocess.run("dvc add data/diabetes.csv", shell=True)
# subprocess.run("git add data/diabetes.csv.dvc .gitignore", shell=True)
# subprocess.run('git commit -m "Add diabetes dataset tracked by DVC"', shell=True)
