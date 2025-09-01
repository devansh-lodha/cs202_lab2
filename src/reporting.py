# src/reporting.py
"""Module for generating the final text-based report from the results CSV."""
import logging
import pandas as pd

def generate_text_report(df: pd.DataFrame) -> None:
    """Analyzes the final DataFrame and prints a summary report to the console."""
    logging.info("Generating final text-based report...")
    
    score_cols = {
        "Developer (RQ1)": "Developer_Score",
        "Baseline LLM (RQ2)": "Baseline_LLM_Score",
        "Rectifier (RQ3)": "Rectifier_Score"
    }
    
    report_lines = ["\n", "="*50, " DETAILED SCORE ANALYSIS", "="*50]

    for name, col in score_cols.items():
        valid_scores = df[col].dropna().astype(int)
        valid_scores = valid_scores[valid_scores > 0]
        
        if not valid_scores.empty:
            avg_score = valid_scores.mean()
            hit_rate = len(valid_scores) * 100 / len(df)
            
            report_lines.append(f"\n--- {name} ---")
            report_lines.append(f"Average Score: {avg_score:.2f} / 5")
            report_lines.append(f"Hit Rate (valid scores > 0): {hit_rate:.1f}%")
            report_lines.append("Score Distribution:")
            report_lines.append(valid_scores.value_counts().sort_index().to_string())
        else:
            report_lines.append(f"\n--- {name} ---\nNo valid scores found.")

    report_lines.extend(["\n", "="*50, " RECTIFICATION IMPROVEMENT ANALYSIS", "="*50])
    if "Improvement_Category" in df.columns and not df["Improvement_Category"].dropna().empty:
        report_lines.append("Improvement Category Distribution:")
        report_lines.append(df["Improvement_Category"].value_counts().to_string())
    report_lines.append("="*50 + "\n")

    print("\n".join(report_lines))