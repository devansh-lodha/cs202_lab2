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
        """
        Intelligently merges newly mined data with existing results OR initializes a clean
        DataFrame with a stable schema for a fresh run.
        """
        cols = config['columns']
        key_cols = [cols['hash'], cols['message'], cols['filename'], cols['diff']]
        
        output_path = config['io']['output_csv_path']
        if os.path.exists(output_path):
            logging.info(f"Resuming from existing file: {output_path}")
            processed_df = pd.read_csv(output_path)
            analysis_cols = [
                cols['baseline_msg'], cols['rectified_msg'], cols['improvement_cat'],
                cols['improvement_reason'], cols['dev_score'], cols['llm_score'],
                cols['rectifier_score'], cols['dev_justify'], cols['llm_justify'],
                cols['rectifier_justify']
            ]
            cols_to_merge = key_cols + [c for c in analysis_cols if c in processed_df.columns]
            merged_df = pd.merge(mined_df, processed_df[cols_to_merge], on=key_cols, how='left')
        else:
            logging.info("No existing results file found. Initializing new DataFrame schema.")
            merged_df = mined_df
            
            # Define columns and their correct initial types
            string_cols = [
                cols['baseline_msg'], cols['rectified_msg'], cols['improvement_cat'],
                cols['improvement_reason'], cols['dev_justify'], cols['llm_justify'],
                cols['rectifier_justify']
            ]
            numeric_cols = [
                cols['dev_score'], cols['llm_score'], cols['rectifier_score']
            ]
            
            # Initialize with types that pandas understands correctly
            for col in string_cols:
                merged_df[col] = pd.Series(dtype='object')
            for col in numeric_cols:
                merged_df[col] = pd.Series(dtype='float64') # Use float to allow for NaN
        
        return merged_df

    def get_dataframe(self) -> pd.DataFrame:
        return self.df

    def get_rows_to_process(self, column_to_check: str) -> pd.DataFrame:
        """Returns rows that need processing based on a check for null values."""
        return self.df[self.df[column_to_check].isnull()]

    def update_row(self, index, data: dict):
        """Updates a single row in the DataFrame with new data."""
        for key, value in data.items():
            self.df.loc[index, key] = value

    def save_progress(self):
        """Saves the entire DataFrame to the output CSV file."""
        self.df.to_csv(self.output_path, index=False)