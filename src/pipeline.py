# src/pipeline.py
"""The main pipeline orchestrator class."""
import logging
import pandas as pd
from tqdm.auto import tqdm
from src.config_loader import config
from src.data_miner import mine_repository
from src.data_handler import DataHandler
from src.llm.t5_handler import generate_baseline_messages
from src.llm.qwen_handler import QwenHandler
from src.row_processor import RowProcessor
from src.utils import select_device, clear_gpu_memory

class AnalysisPipeline:
    """Orchestrates the full ETL and analysis pipeline."""
    def __init__(self):
        self.config = config
        self.device = select_device()

    def run(self) -> None:
        """Executes all stages of the pipeline."""
        logging.info(f"Selected device: {self.device}")
        
        # 1. Extract
        mined_df = mine_repository(self.config['io']['processing_limit'])
        
        # 2. Initialize Data Handler
        data_handler = DataHandler(mined_df)
        
        # 3. Baseline Message Generation
        df = data_handler.get_dataframe()
        df = generate_baseline_messages(df, self.device)
        data_handler.save_progress()

        # 4. Advanced Analysis
        qwen_handler = QwenHandler()
        row_processor = RowProcessor(qwen_handler)
        
        rows_to_process = data_handler.get_rows_to_process(column_to_check="Rectifier_Score")
        
        if not rows_to_process.empty:
            logging.info(f"Found {len(rows_to_process)} rows requiring advanced analysis.")
            for idx, row in tqdm(rows_to_process.iterrows(), total=len(rows_to_process), desc="Advanced Analysis"):
                processed_data = row_processor.process(row)
                data_handler.update_row(idx, processed_data)
                data_handler.save_progress()
                clear_gpu_memory()
        else:
            logging.info("All rows have already been analyzed.")