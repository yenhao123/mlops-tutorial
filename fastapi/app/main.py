import torch
import torch.nn as nn
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel


# 設定 input format
class InputData(BaseModel):
    features: list[float]


app = FastAPI()


# 載入模型
class Net(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 64), nn.ReLU(), nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.net(x)


model = Net(in_features=10)
model.load_state_dict(torch.load("models/model.pt"))
model.eval()


@app.post("/predict")
def predict(data: InputData):
    x = torch.tensor([data.features], dtype=torch.float32)
    with torch.no_grad():
        y = model(x)
    return {"prediction": y.item()}
