# src/row_processor.py
"""
Contains the logic for processing a single row of the DataFrame with the
advanced analysis LLM.
"""
import pandas as pd  # <--- THIS IS THE FIX
from src.config_loader import config
from src.llm.qwen_handler import QwenHandler
from src.utils import parse_json_from_response

class RowProcessor:
    def __init__(self, qwen_handler: QwenHandler):
        self.handler = qwen_handler
        self.max_input_chars = config['inference']['max_input_chars']

    def process(self, row_data: pd.Series) -> dict:
        """Performs the full rectify, evaluate, and classify sequence for a single row."""
        diff = row_data["Diff"][:self.max_input_chars]
        results = {}

        # 1. Rectify
        rectified_resp = self.handler.rectify_message(diff)
        rectified_msg = parse_json_from_response(rectified_resp, 'rectified_message')
        results["Rectified_Message"] = rectified_msg or "fix: rectification failed"
        
        # 2. Evaluate
        messages_to_eval = {
            "Developer": ("Developer_Score", "Developer_Justification", row_data["Message"]),
            "Baseline_LLM": ("Baseline_LLM_Score", "Baseline_LLM_Justification", row_data["Baseline_Message"]),
            "Rectifier": ("Rectifier_Score", "Rectifier_Justification", results["Rectified_Message"])
        }
        for name, (score_col, just_col, msg) in messages_to_eval.items():
            eval_resp = self.handler.evaluate_message(diff, msg)
            results[score_col] = parse_json_from_response(eval_resp, 'score', is_score=True)
            results[just_col] = parse_json_from_response(eval_resp, 'justification')

        # 3. Classify
        classify_resp = self.handler.classify_improvement(row_data["Message"], results["Rectified_Message"])
        results["Improvement_Category"] = parse_json_from_response(classify_resp, 'improvement_category')
        results["Improvement_Reason"] = parse_json_from_response(classify_resp, 'reason')
        
        return results