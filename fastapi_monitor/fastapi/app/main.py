import torch
import torch.nn as nn
from fastapi import FastAPI, Response
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, Summary, generate_latest


# 設定 input format
class InputData(BaseModel):
    features: list[float]


# 輸入格式：驗證
class ValidationInput(BaseModel):
    features: list[float]
    label: float


app = FastAPI()

# Prometheus 指標
REQUEST_COUNT = Counter("request_count", "Total number of prediction requests")
ERROR_COUNT = Counter("error_count", "Total prediction errors")
PREDICTION_DISTRIBUTION = Histogram(
    "prediction_distribution", "Distribution of prediction outputs"
)
rmse_help = "RMSE between prediction and label"
VALIDATION_RMSE = Summary("validation_rmse", rmse_help)


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
    REQUEST_COUNT.inc()
    try:
        x = torch.tensor([data.features], dtype=torch.float32)
        with torch.no_grad():
            y = model(x)
        y_val = y.item()
        PREDICTION_DISTRIBUTION.observe(y_val)
        return {"prediction": y_val}
    except Exception:
        ERROR_COUNT.inc()
        raise


@app.post("/validate")
def validate(data: ValidationInput):
    try:
        x = torch.tensor([data.features], dtype=torch.float32)
        with torch.no_grad():
            y = model(x)
        y_val = y.item()
        squared_error = (y_val - data.label) ** 2
        VALIDATION_RMSE.observe(squared_error**0.5)  # RMSE for single sample
        return {
            "prediction": y_val,
            "label": data.label,
            "rmse": squared_error**0.5,
        }
    except Exception:
        ERROR_COUNT.inc()
        raise


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
