# src/data_handler.py
"""
Handles all data loading, merging, and saving operations for the pipeline's DataFrame.
"""
import os
import logging
import pandas as pd
from src.config_loader import config

class DataHandler:
    def __init__(self, mined_df: pd.DataFrame):
        self.df = self._initialize_dataframe(mined_df)
        self.output_path = config['io']['output_csv_path']

    def _initialize_dataframe(self, mined_df: pd.DataFrame) -> pd.DataFrame:
        """Loads existing results and merges them with newly mined data."""
        output_path = config['io']['output_csv_path']
        if os.path.exists(output_path):
            logging.info(f"Resuming from existing file: {output_path}")
            processed_df = pd.read_csv(output_path)
            merged_df = pd.merge(mined_df, processed_df, on=["Hash", "Message", "Filename", "Diff"], how='left')
        else:
            logging.info("No existing results file found. Starting a new run.")
            merged_df = mined_df
        
        expected_cols = ["Baseline_Message", "Rectified_Message", "Improvement_Category", "Improvement_Reason", 
                         "Developer_Score", "Baseline_LLM_Score", "Rectifier_Score", "Developer_Justification", 
                         "Baseline_LLM_Justification", "Rectifier_Justification"]
        for col in expected_cols:
            if col not in merged_df.columns:
                merged_df[col] = None
        return merged_df

    def get_dataframe(self) -> pd.DataFrame:
        """Returns the current state of the DataFrame."""
        return self.df

    def get_rows_to_process(self, column_to_check: str) -> pd.DataFrame:
        """Returns a view of the DataFrame for rows that need processing."""
        return self.df[self.df[column_to_check].isnull()]

    def update_row(self, index, data: dict):
        """Updates a single row in the DataFrame with new data."""
        for key, value in data.items():
            self.df.loc[index, key] = value

    def save_progress(self):
        """Saves the entire DataFrame to the output CSV file."""
        self.df.to_csv(self.output_path, index=False)