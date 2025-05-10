# 这个代码块是为了提供一个可运行版本的 `run_ising_simulation` 函数（位于 ising_model.py 中）

import numpy as np

def run_ising_simulation(L, Tmin, Tmax, nT, Ntrial, Lattice, outdir):
    """
    模拟 Ising 模型（Wolff算法），输出包含温度、自旋构型、磁化率、磁化强度等结果。
    """
    T_list = np.linspace(Tmin, Tmax, nT)
    spin_configs = []
    up_ratios = []
    down_ratios = []
    magnetizations = []
    susceptibilities = []

    N = L * L
    for T in T_list:
        beta = 1.0 / T
        S = 2 * (np.random.randint(0, 2, size=(L, L))) - 1
        M_list = []

        for _ in range(Ntrial):
            # 用简单 Metropolis 而不是 Wolff 算法（简化版本）
            for _ in range(N):
                i, j = np.random.randint(0, L), np.random.randint(0, L)
                dE = 2 * S[i, j] * (
                    S[i, (j+1)%L] + S[i, (j-1)%L] + S[(i+1)%L, j] + S[(i-1)%L, j]
                )
                if np.random.rand() < np.exp(-beta * dE):
                    S[i, j] *= -1
            M_list.append(np.sum(S))

        spin_configs.append(S.copy())
        up_ratios.append(np.sum(S == 1) / N)
        down_ratios.append(np.sum(S == -1) / N)
        magnetizations.append(np.mean(np.abs(M_list)) / N)
        susceptibilities.append((np.var(M_list) / (T * N)))

    # 磁滞回线（只计算最后一个温度）
    T_final = T_list[-1]
    beta = 1 / T_final
    H_vals = np.concatenate([np.linspace(-1, 1, 20), np.linspace(0.95, -1, 20)])
    S = np.ones((L, L))
    M_H = []

    for H in H_vals:
        for _ in range(Ntrial):
            for _ in range(N):
                i, j = np.random.randint(0, L), np.random.randint(0, L)
                dE = 2 * S[i, j] * (
                    S[i, (j+1)%L] + S[i, (j-1)%L] + S[(i+1)%L, j] + S[(i-1)%L, j]
                ) + 2 * H * S[i, j]
                if np.random.rand() < np.exp(-beta * dE):
                    S[i, j] *= -1
        M_H.append(np.sum(S) / N)

    return {
        "temps": T_list,
        "spin_configs": spin_configs,
        "magnetizations": magnetizations,
        "susceptibilities": susceptibilities,
        "up_ratios": up_ratios,
        "down_ratios": down_ratios,
        "H_vals": H_vals,
        "hysteresis": M_H,
        "T_final": T_final
    }
