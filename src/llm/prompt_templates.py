# src/llm/prompt_templates.py
"""
Formats prompt templates from the central configuration with runtime data.
This separation ensures that the core LLM interaction logic is clean and
independent of the specific prompt text.
"""
from src.config_loader import config

def format_rectify_prompt(diff: str) -> dict:
    """Formats the system and user prompts for the rectification task."""
    return {
        "system": config['prompts']['rectify']['system'],
        "user": config['prompts']['rectify']['user'].format(diff=diff)
    }

def format_evaluate_prompt(diff: str, message: str) -> dict:
    """Formats the system and user prompts for the evaluation task."""
    return {
        "system": config['prompts']['evaluate']['system'],
        "user": config['prompts']['evaluate']['user'].format(diff=diff, message=message)
    }

def format_classify_prompt(old_message: str, new_message: str) -> dict:
    """Formats the system and user prompts for the classification task."""
    return {
        "system": config['prompts']['classify']['system'],
        "user": config['prompts']['classify']['user'].format(old_message=old_message, new_message=new_message)
    }