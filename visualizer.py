# visualizer.py
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def plot_magnetization(df):
    fig, ax1 = plt.subplots()
    ax1.errorbar(df["Temperature"], df["Magnetization"],
                 yerr=np.sqrt(df["Magnetization_Var"]),
                 fmt='o-', color='tab:red', label='Magnetization')
    ax1.set_xlabel("Temperature")
    ax1.set_ylabel("Magnetization", color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(df["Temperature"], df["Susceptibility"],
             's-', color='tab:blue', label='Susceptibility')
    ax2.set_ylabel("Susceptibility", color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    fig.tight_layout()
    return fig

def plot_binder(df):
    fig, ax = plt.subplots()
    ax.plot(df["Temperature"], df["Binder_Ratio"], 'd-', color='tab:purple')
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Binder Ratio")
    ax.grid(True)
    return fig

def plot_cluster_hist(all_cluster_sizes):
    fig, ax = plt.subplots()
    ax.hist(all_cluster_sizes, bins=30, density=True, alpha=0.7, color='tab:green')
    ax.set_xlabel("Cluster Size")
    ax.set_ylabel("Probability Density")
    ax.set_title("Cluster Size Distribution")
    ax.grid(True)
    return fig

def fig_to_bytes(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    return buf
