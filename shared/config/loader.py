"""
Python Loader yaml files
"""
import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent

def load_yaml(filename: str):
    path = CONFIG_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_agents():
    return load_yaml("agents.yaml")