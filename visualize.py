# visualize.py
"""
Orchestrates the generation of all publication-quality visualizations
for the lab report by calling dedicated generator functions.
"""
import pandas as pd
import os
import sys
from src.config_loader import config
from plotting import styler, plot_generators

def main():
    """Main function to load data, apply styles, and generate all plots."""
    input_csv = config['io']['output_csv_path']
    output_dir = config['io']['output_chart_path']
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        df = pd.read_csv(input_csv)
        print("Successfully loaded 'lab2_results_final.csv'.")
    except FileNotFoundError:
        print(f"FATAL ERROR: Results file not found at '{input_csv}'. Run main.py first.")
        sys.exit()

    # Apply global styles once
    styler.apply_global_styles()

    # Define all plots to be generated
    plots_to_generate = {
        "figure_1_quality_comparison.png": plot_generators.create_quality_comparison_chart,
        "figure_2_score_distribution.png": plot_generators.create_score_distribution_chart,
        "figure_3_improvement_breakdown.png": plot_generators.create_improvement_breakdown_chart
    }

    # Loop through and generate each plot
    for filename, generator_func in plots_to_generate.items():
        print(f"Generating {filename}...")
        fig = generator_func(df)
        output_path = os.path.join(output_dir, filename)
        fig.savefig(output_path)
        print(f"Saved: {output_path}")

    print("\nAll plots have been successfully generated and saved.")

if __name__ == "__main__":
    main()