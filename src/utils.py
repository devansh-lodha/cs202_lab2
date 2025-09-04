# src/utils.py
"""Utility functions used across the data processing pipeline."""
import logging
import sys
import gc
import re
import json
from typing import Any
import torch

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s', stream=sys.stdout, datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger("pydriller").setLevel(logging.WARNING)
    logging.getLogger("transformers").setLevel(logging.WARNING)

def select_device():
    if torch.cuda.is_available(): return torch.device("cuda")
    if torch.backends.mps.is_available(): return torch.device("mps")
    return torch.device("cpu")

def clear_gpu_memory():
    gc.collect()
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    elif torch.backends.mps.is_available(): torch.mps.empty_cache()

def parse_json_from_response(response: str, key: str, is_score: bool = False) -> Any:
    """
    Safely extracts a value from a JSON object embedded in an LLM response string.
    If `is_score` is True, it aggressively attempts to convert the value to an integer.
    """
    default_value = 0 if is_score else ""
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if not json_match:
        return default_value
    try:
        json_obj = json.loads(json_match.group(0))
        value = json_obj.get(key)

        if value is None:
            return default_value

        if is_score:
            try:
                return int(float(value))
            except (ValueError, TypeError):
                return 0
        
        return value
    except (json.JSONDecodeError, KeyError, TypeError):
        return default_value