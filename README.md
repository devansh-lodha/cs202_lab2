# CS202 Lab 2: Automated Commit Message Rectification Pipeline

## 1. Overview

This project is a complete, production-grade ETL pipeline developed for the "CS202: Software Tools and Techniques" course. Its purpose is to mine the `geocoder` open-source repository, identify bug-fixing commits, and use a series of Large Language Models (LLMs) to automatically evaluate and rectify the quality of their commit messages. The entire framework is designed to be modular, resumable, and professional.

## 2. Key Features

-   **Automated Repository Mining**: Uses `PyDriller` to efficiently traverse the Git history and extract relevant commits based on keywords and regex.
-   **Professional & Modular Architecture**: The codebase is strictly organized with a `src` package, a centralized `config.yaml`, and a complete separation of concerns between data processing, LLM interaction, and visualization.
-   **Dual-LLM Analysis Pipeline**:
    -   A baseline T5 model (`mamiksik/CommitPredictorT5`) generates an initial commit message.
    -   An advanced Qwen model (`Qwen/Qwen3-4B-Instruct-2507`) performs three complex tasks:
        1.  **Rectification**: Rewrites messages into the Conventional Commits standard.
        2.  **Evaluation**: Scores the quality of developer, baseline, and rectified messages.
        3.  **Classification**: Categorizes the type of improvement made.
-   **Resumable & Fault-Tolerant**: The pipeline saves its progress to a CSV after every single analysis, allowing it to be stopped and safely resumed without losing work.
-   **Publication-Quality Visualizations**: A separate, dedicated script generates a suite of beautiful and insightful plots ready for an academic report.

## 3. Project Architecture

The project follows a clean, decoupled architecture:

```
cs202_lab2_project/
├── config.yaml               # All configuration, including LLM prompts
├── main.py                   # Main entry point for the analysis pipeline
├── visualize.py              # Separate script to generate plots
├── requirements.txt          # Project dependencies
├── README.md                 # This file
└── src/
    ├── __init__.py
    ├── config_loader.py      # Loads the YAML config
    ├── data_handler.py       # Manages DataFrame I/O and state
    ├── data_miner.py         # Mines the Git repository
    ├── pipeline.py           # The main pipeline orchestration class
    ├── reporting.py          # Generates the final console report
    ├── row_processor.py      # Logic for processing a single row with Qwen
    ├── utils.py              # Shared helper functions
    └── llm/
        ├── __init__.py
        ├── prompt_templates.py # Formats prompts with data
        ├── qwen_handler.py   # Handles the advanced Qwen model
        └── t5_handler.py     # Handles the baseline T5 model
```

## 4. Setup and Usage

### Step A: Environment Setup

1.  Clone the repository and navigate into the project directory.
2.  Create and activate a Python virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Step B: Run the Analysis Pipeline

This will perform the repository mining and all LLM analysis tasks. This process can take several hours depending on your hardware.

```bash
python main.py
```
The script will produce `lab2_results_final.csv` and print a final summary report to the console.

### Step C: Generate the Visualizations

After the main pipeline is complete, run this script to generate the plots.

```bash
python visualize.py
```
This will create a `visuals/` directory containing the three publication-quality PNG files for the report.

## 5. Results Overview

The pipeline confirmed that the Rectifier model significantly improves commit message quality, raising the average score from **2.10 (Developer)** to **2.99 (Rectifier)** on a 5-point scale. The majority of these improvements were substantive "Corrective" and "Semantic" changes.

![Quality Comparison Chart](./visuals/figure_1_quality_comparison.png)

## 6. Technologies Used

-   Python 3.12
-   PyDriller
-   Pandas
-   Hugging Face Transformers
-   PyTorch
-   Matplotlib & Seaborn
```
