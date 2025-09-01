# src/config_loader.py
"""
Loads the central YAML configuration file for the project.

This module ensures that the configuration is loaded only once and can be
accessed as a shared Python object across the entire application, providing
a single source of truth for all settings.
"""
import yaml

def load_config(path: str = 'config.yaml') -> dict:
    """Loads a YAML file and returns its content as a dictionary."""
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"FATAL ERROR: Configuration file not found at '{path}'.")
        exit()
    except yaml.YAMLError as e:
        print(f"FATAL ERROR: Error parsing YAML configuration file: {e}")
        exit()

# Load the configuration once when the module is first imported.
config = load_config()