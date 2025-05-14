import pandas as pd
import numpy as np
import yaml
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from torch.utils.data import TensorDataset, DataLoader
import mlflow.pytorch

# 讀參數
with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)
lr = params["train"]["lr"]
epochs = params["train"]["epochs"]

# 載入資料
df = pd.read_csv("data/diabetes.csv")
X = df.drop(columns=["target"]).values
y = df["target"].values

# 預處理
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

train_loader = DataLoader(TensorDataset(X_train_tensor, y_train_tensor), batch_size=32, shuffle=True)

# 模型
class Net(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    def forward(self, x):
        return self.net(x)

model = Net(in_features=X.shape[1])
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=lr)

# MLflow 開始紀錄
with mlflow.start_run():
    for epoch in range(epochs):
        model.train()
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(batch_X), batch_y)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        preds = model(X_test_tensor)
        mse = mean_squared_error(y_test, preds.numpy())
        rmse = np.sqrt(mse)

    mlflow.log_param("lr", lr)
    mlflow.log_param("epochs", epochs)
    mlflow.log_metric("rmse", rmse)
    mlflow.pytorch.log_model(model, "model")

    torch.save(model.state_dict(), "models/model.pt")  # 輸出模型供 DVC 管理
