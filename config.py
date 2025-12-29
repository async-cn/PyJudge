import yaml
import json
import os

def load(path:str) -> dict:
    with open(path, "r", encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_json(path:str) -> dict:
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)

def load_text(path:str) -> str:
    with open(path, "r", encoding='utf-8') as f:
        return f.read()

def read_global_config() -> dict:
    script_dir = os.path.dirname(__file__)
    return load(os.path.join(script_dir, 'configs/global.yml'))

if __name__ == "__main__":
    print(read_global_config())