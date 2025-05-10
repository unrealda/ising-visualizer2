import matplotlib.pyplot as plt
import numpy as np
import os

def plot_spin_arrows(S, T, filename=None):
    """
    绘制当前构型下的箭头图（红↑、蓝↓）并保存/展示。

    Parameters:
        S: 2D numpy array，自旋矩阵 (+1 or -1)
        T: 当前温度
        filename: 若不为None，则保存至此路径
    """
    Lx, Ly = S.shape
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, Ly + 1)
    ax.set_ylim(0, Lx + 1)
    ax.set_aspect('equal')
    ax.axis('off')

    up_count = np.sum(S == 1)
    down_count = np.sum(S == -1)

    for x in range(Ly):
        for y in range(Lx):
            spin = S[y, x]
            if spin == 1:
                ax.text(x + 1, Lx - y, '↑', fontsize=14, color='r', ha='center', va='center')
            else:
                ax.text(x + 1, Lx - y, '↓', fontsize=14, color='deepskyblue', ha='center', va='center')

    # 标注温度和计数
    ax.text(1.2, Lx + 0.5, f'T = {T:.3f}', fontsize=12, weight='bold')
    ax.text(Ly * 0.4, Lx + 0.5, f'↑: {up_count}', fontsize=12, color='r', weight='bold')
    ax.text(Ly * 0.7, Lx + 0.5, f'↓: {down_count}', fontsize=12, color='deepskyblue', weight='bold')

    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=150)
        plt.close()
    else:
        plt.show()


def plot_spin_ratio_vs_temp(temps, up_ratios, down_ratios, outpath=None):
    """
    绘制↑/↓比例随温度的变化曲线图。

    Parameters:
        temps: 温度数组
        up_ratios: 向上自旋比例
        down_ratios: 向下自旋比例
        outpath: 保存路径（若有）
    """
    plt.figure(figsize=(7, 4))
    plt.plot(temps, up_ratios, 'r-o', label='↑ ratio')
    plt.plot(temps, down_ratios, 'b-s', label='↓ ratio')
    plt.xlabel('Temperature T')
    plt.ylabel('Ratio')
    plt.title('Spin Ratio vs Temperature')
    plt.grid(True)
    plt.legend()
    if outpath:
        plt.savefig(outpath, dpi=150)
        plt.close()
    else:
        plt.show()
