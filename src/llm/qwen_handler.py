# src/llm/qwen_handler.py
"""
Contains the handler for the advanced analysis LLM (Qwen), which performs
rectification, evaluation, and classification of commit messages.
"""
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, LogitsProcessor
from src.config_loader import config
from src.llm import prompt_templates

# This class is a safety valve to prevent crashes from numerical instability.
class SafeLogitsProcessor(LogitsProcessor):
    """
    A LogitsProcessor that sanitizes logits to prevent crashes from `inf` or `nan` values.
    It replaces any invalid numbers with safe, finite equivalents.
    """
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        # torch.nan_to_num is a robust, built-in function to clean up tensors.
        return torch.nan_to_num(scores, nan=0.0, posinf=1e4, neginf=-1e4)

class QwenHandler:
    """A handler for orchestrating complex tasks with the Qwen model."""
    def __init__(self):
        model_name = config['models']['analysis_llm']
        logging.info(f"Loading Analysis LLM: {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype="auto", device_map="auto"
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Instantiate our safety valve
        self.safe_logits_processor = SafeLogitsProcessor()
        logging.info("Analysis LLM loaded successfully with SafeLogitsProcessor.")

    def _generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generates a single response from the LLM, now with safety checks."""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                model_inputs.input_ids,
                attention_mask=model_inputs.attention_mask,
                max_new_tokens=config['inference']['max_output_tokens'],
                do_sample=True, temperature=0.7, top_p=0.8,
                logits_processor=[self.safe_logits_processor]
            )
            response_ids = generated_ids[0][len(model_inputs.input_ids[0]):]
        return self.tokenizer.decode(response_ids, skip_special_tokens=True).strip()

    def rectify_message(self, diff: str) -> str:
        """Generates a rectified commit message for a given diff."""
        prompts = prompt_templates.format_rectify_prompt(diff)
        return self._generate(prompts['system'], prompts['user'])

    def evaluate_message(self, diff: str, message: str) -> str:
        """Generates a quality score and justification for a given message and diff."""
        prompts = prompt_templates.format_evaluate_prompt(diff, message)
        return self._generate(prompts['system'], prompts['user'])

    def classify_improvement(self, old_message: str, new_message: str) -> str:
        """Classifies the improvement between an old and new message."""
        prompts = prompt_templates.format_classify_prompt(old_message, new_message)
        return self._generate(prompts['system'], prompts['user'])