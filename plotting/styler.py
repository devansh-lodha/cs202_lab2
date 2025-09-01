# plotting/styler.py
"""
Centralizes all styling configurations for matplotlib and seaborn plots
to ensure a consistent, publication-quality aesthetic.
"""
import matplotlib.pyplot as plt
import seaborn as sns

def apply_global_styles():
    """Applies a consistent, professional style to all plots."""
    sns.set_style("whitegrid")
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.left'] = False
    plt.rcParams['grid.color'] = '#EAEAEA'
    plt.rcParams['grid.linestyle'] = '--'
    try:
        plt.rcParams['font.family'] = 'Lato'
        print("Confirmation: Global font successfully set to 'Lato'.")
    except Exception:
        plt.rcParams['font.family'] = 'Arial' # Fallback
        print("WARNING: 'Lato' not found. Defaulting to 'Arial'.")

# --- Standard Color Palettes ---
COLORS_MAIN = {
    'Rectifier': 'lightgreen',
    'Developer': 'skyblue',
    'Baseline LLM': 'salmon'
}

COLORS_DONUT = {
    'Corrective': 'lightgreen',
    'Semantic': 'salmon',
    'Cosmetic': 'skyblue',
    'Trivial': '#D3D3D3',
    'Regressive': '#A9A9A9'
}