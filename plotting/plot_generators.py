# plotting/plot_generators.py
"""
Contains dedicated functions for generating each of the visualizations
for the final report. Each function is self-contained and returns a
matplotlib Figure object.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patches as mpatches
from plotting.styler import COLORS_MAIN, COLORS_DONUT

def create_quality_comparison_chart(df: pd.DataFrame) -> plt.Figure:
    """Generates the horizontal bar chart comparing average scores."""
    mean_scores = df[['Developer_Score', 'Baseline_LLM_Score', 'Rectifier_Score']].mean()
    mean_scores.index = ['Developer', 'Baseline LLM', 'Rectifier']
    scores_series = mean_scores.sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(scores_series.index, scores_series.values, color=[COLORS_MAIN[label] for label in scores_series.index])
    fig.suptitle('Rectifier Achieves Highest Average Quality Score', fontsize=22, fontweight='bold', ha='left', x=0.125, y=0.98)
    ax.set_title('Comparing mean scores of commit messages on a 1-5 scale', fontsize=14, loc='left', pad=10, color='gray')
    ax.set_xlabel('Average Quality Score', fontsize=12, labelpad=15, color='gray')
    ax.tick_params(axis='y', length=0)
    ax.set_yticks(range(len(scores_series)))
    ax.set_yticklabels(scores_series.index, fontsize=14, fontweight='bold')
    ax.bar_label(bars, fmt='%.2f', padding=-40, fontsize=12, fontweight='bold', color='white')
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    return fig

def create_score_distribution_chart(df: pd.DataFrame) -> plt.Figure:
    """Generates the violin plot showing score distributions."""
    df_long = df.melt(value_vars=['Developer_Score', 'Baseline_LLM_Score', 'Rectifier_Score'], var_name='Message Source', value_name='Quality Score')
    df_long['Message Source'] = df_long['Message Source'].map({'Developer_Score': 'Developer', 'Baseline_LLM_Score': 'Baseline LLM', 'Rectifier_Score': 'Rectifier'})
    order = ['Developer', 'Baseline LLM', 'Rectifier']
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.violinplot(data=df_long, x='Message Source', y='Quality Score', order=order, palette=COLORS_MAIN, inner='box', hue='Message Source', legend=False, ax=ax, linewidth=2)
    sns.stripplot(data=df_long, x='Message Source', y='Quality Score', order=order, color='#404040', alpha=0.1, jitter=0.2, size=3, ax=ax)
    fig.suptitle("Rectifier's Scores are Less Variable and Skew Higher", fontsize=22, fontweight='bold', ha='left', x=0.125, y=0.98)
    ax.set_title('Score distribution reveals consistency and performance', fontsize=14, loc='left', pad=10, color='gray')
    ax.set_xlabel('Message Source', fontsize=12, labelpad=15, color='gray')
    ax.set_ylabel('Quality Score', fontsize=12, labelpad=15, color='gray')
    ax.set_ylim(0.5, 5.5)
    ax.set_yticks(range(1, 6))
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, fontsize=14, fontweight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    return fig

def create_improvement_breakdown_chart(df: pd.DataFrame) -> plt.Figure:
    """Generates the donut chart with non-overlapping external labels for small slices."""
    category_counts = df['Improvement_Category'].value_counts()
    category_order = ['Corrective', 'Semantic', 'Cosmetic', 'Trivial', 'Regressive']
    df_donut = pd.DataFrame({'counts': category_counts}).reindex(category_order).dropna().sort_values(by='counts', ascending=False)
    percentages = df_donut['counts'] * 100 / df_donut['counts'].sum()
    fig, ax = plt.subplots(figsize=(12, 9), subplot_kw=dict(aspect="equal"))
    wedges, _, autotexts = ax.pie(df_donut['counts'], wedgeprops=dict(width=0.4, edgecolor='w', linewidth=4), colors=[COLORS_DONUT.get(label, '#CCCCCC') for label in df_donut.index], startangle=90, autopct='%1.1f%%', pctdistance=0.85)
    plt.setp(autotexts, size=14, weight="bold", color="white")
    small_slices = percentages[percentages < 4]
    wedge_indices = [list(percentages.index).index(label) for label in small_slices.index]
    sorted_wedges = sorted(zip(wedge_indices, small_slices.index, small_slices.values), key=lambda x: wedges[x[0]].theta1)
    label_y_start = 1.2
    label_y_step = 0.18
    for i, (wedge_idx, label, pct) in enumerate(sorted_wedges):
        autotexts[wedge_idx].set_visible(False)
        wedge = wedges[wedge_idx]
        ang = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        y_text = label_y_start - (i * label_y_step)
        ax.annotate(f"{label}: {pct:.1f}%", xy=(x, y), xytext=(1.3, y_text), horizontalalignment='left', fontsize=12, arrowprops=dict(arrowstyle="-", connectionstyle="angle,angleA=0,angleB=90", color='gray'))
    fig.suptitle("Over 70% of Rectifier's Changes are Substantive", fontsize=22, fontweight='bold', ha='center', y=0.98)
    ax.set_title("Breakdown of improvement categories by frequency", fontsize=14, pad=10, color='gray', ha='center')
    ax.text(0, 0, 'Improvement\nTypes', ha='center', va='center', fontsize=24, fontweight='bold', color='#333333')
    legend_patches = [mpatches.Patch(color=COLORS_DONUT.get(label, '#CCCCCC'), label=label) for label in df_donut.index]
    ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(0.95, 0.5), fontsize=14, frameon=False, title='Category', title_fontproperties={'size':16, 'weight':'bold'})
    fig.tight_layout(rect=[0, 0.05, 0.9, 0.93])
    return fig