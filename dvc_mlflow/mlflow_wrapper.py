import mlflow
import subprocess
import yaml

def run_with_mlflow_from_yaml(script: str, yaml_path: str, section: str = "train", artifacts: list = None):
    """
    從 YAML 讀取參數，執行一個外部 Python 腳本，並記錄參數與 artifacts。

    Args:
        script (str): 要執行的 Python 檔案名稱，例如 'train.py'
        yaml_path (str): 參數設定的 YAML 檔路徑，例如 'params.yaml'
        section (str): YAML 中的參數區塊 key，例如 'train'
        artifacts (list, optional): 要記錄的輸出檔案，例如 ['model.pt']
    """
    # 讀取 YAML
    with open(yaml_path, "r", encoding="utf-8") as f:
        full_config = yaml.safe_load(f)
        params = full_config.get(section)
        if params is None:
            raise ValueError(f"YAML 中沒有名為 '{section}' 的區段")

    with mlflow.start_run():
        # log 所有參數
        for key, value in params.items():
            mlflow.log_param(key, value)

        # 組合執行命令，例如：python train.py --lr 0.001 --epochs 200
        param_str = ' '.join(f'--{k} {v}' for k, v in params.items())
        cmd = f"python {script} {param_str}"
        print(f"📦 Running command: {cmd}")
        subprocess.run(cmd, shell=True, check=True)

        # log artifacts
        if artifacts:
            for path in artifacts:
                try:
                    mlflow.log_artifact(path)
                except Exception as e:
                    print(f"❗ Failed to log artifact {path}: {e}")
