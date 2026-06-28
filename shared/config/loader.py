"""
Python Loader yaml files
"""
import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent
AGENTS_CONFIG = "agents.yaml"
GROUND_TRUTH_DATASET = "ragas_ground_truth_ds.yaml"

def load_yaml(filename: str):
    path = CONFIG_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_agents():
    return load_yaml(AGENTS_CONFIG)

def load_golden_dataset() -> list[dict]:
    """Load the golden dataset of role-tagged questions and ground truths.

    Returns:
        A list of dicts, each with 'role', 'question', and 'ground_truth'.
    """
    return load_yaml(GROUND_TRUTH_DATASET)