import hashlib
import yaml

def file_md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def load_dvc_hash(dvc_file):
    with open(dvc_file, "r") as f:
        content = yaml.safe_load(f)
        return content["outs"][0]["md5"]
    
data_path = "data/diabetes.csv"
dvc_path = "data/diabetes.csv.dvc"

file_hash = file_md5(data_path)
dvc_hash = load_dvc_hash(dvc_path)

print(f"📦 Data file hash     : {file_hash}")
print(f"📄 DVC tracked hash   : {dvc_hash}")
print("✅ Hash match!" if file_hash == dvc_hash else "❌ Hash mismatch!")