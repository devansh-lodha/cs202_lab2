# visualize.py
"""Orchestrates the generation of all visualizations for the Lab 2 report."""
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.config_loader import config
from plotting import styler, plot_generators

def main():
    """Main function to load final data and generate all outputs."""
    input_csv = config['io']['output_csv_path']
    output_dir = config['io']['visuals_dir']
    # ---------------------------------------------------------
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"FATAL: Final results file '{input_csv}' not found. Please run main.py first.")
        sys.exit()

    styler.apply_global_styles()

    plots_to_generate = {
        "figure_1_quality_comparison.png": plot_generators.create_quality_comparison_chart,
        "figure_2_score_distribution.png": plot_generators.create_score_distribution_chart,
        "figure_3_improvement_breakdown.png": plot_generators.create_improvement_breakdown_chart,
    }

    print("--- Generating Lab 2 Report Visualizations ---")
    for filename, generator_func in plots_to_generate.items():
        print(f"Generating {filename}...")
        fig = generator_func(df)
        fig.savefig(os.path.join(output_dir, filename), bbox_inches='tight')
    
    print(f"\nAll plots saved to '{output_dir}' directory.")

if __name__ == "__main__":
    main()