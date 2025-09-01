# main.py
"""
Main entry point for the CS202 Lab 2 analysis pipeline.
"""
import pandas as pd
from src.pipeline import AnalysisPipeline
from src.reporting import generate_text_report
from src.utils import setup_logging
from src.config_loader import config

if __name__ == "__main__":
    setup_logging()
    
    # Run the main data processing pipeline
    pipeline = AnalysisPipeline()
    pipeline.run()
    
    # Generate the final text summary from the completed CSV
    final_df = pd.read_csv(config['io']['output_csv_path'])
    generate_text_report(final_df)