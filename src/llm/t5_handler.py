# src/llm/t5_handler.py
"""Handles baseline commit message generation using the T5 model."""
import logging
import torch
import pandas as pd
from tqdm.auto import tqdm
from transformers import AutoTokenizer, T5ForConditionalGeneration
from src.config_loader import config
from src.utils import clear_gpu_memory

def generate_baseline_messages(df: pd.DataFrame, device: torch.device) -> pd.DataFrame:
    """Generates baseline commit messages for rows that do not have them."""
    model_name = config['models']['baseline_llm']
    batch_size = config['inference']['t5_batch_size']
    logging.info(f"Running baseline message generation with {model_name}...")
    
    rows_needing_baseline = df[df["Baseline_Message"].isnull()]
    if rows_needing_baseline.empty:
        logging.info("All baseline messages are already generated.")
        return df

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)
    
    diffs_to_process = rows_needing_baseline["Diff"].tolist()
    all_messages = []

    for i in tqdm(range(0, len(diffs_to_process), batch_size), desc="Generating Baseline Messages"):
        batch_diffs = diffs_to_process[i:i + batch_size]
        inputs = tokenizer(batch_diffs, return_tensors="pt", max_length=512, truncation=True, padding=True).to(device)
        outputs = model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
        all_messages.extend(tokenizer.batch_decode(outputs, skip_special_tokens=True))

    df.loc[rows_needing_baseline.index, "Baseline_Message"] = all_messages
    logging.info("Baseline message generation complete.")
    del model, tokenizer
    clear_gpu_memory()
    return df