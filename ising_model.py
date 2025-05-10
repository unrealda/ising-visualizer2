# ising_model.py
import numpy as np
import os

# 邻接生成器
def square_neighbors(L):
    N = L * L
    site_dic = {}
    x_y_dic = {}
    nbr = [[] for _ in range(N)]

    for j in range(N):
        row, col = divmod(j, L)
        key = f"{row},{col}"
        site_dic[key] = j
        x_y_dic[j] = (row, col)

    for j in range(N):
        row, col = x_y_dic[j]
        nbr[j] = [
            site_dic[f"{row},{(col+1)%L}"],
            site_dic[f"{(row+1)%L},{col}"],
            site_dic[f"{row},{(col-1+L)%L}"],
            site_dic[f"{(row-1+L)%L},{col}"]
        ]

    return nbr, site_dic, x_y_dic

def save_latt(T, S, L, xy, folder):
    lat = np.zeros((L, L), dtype=int)
    for i, spin in enumerate(S):
        x, y = xy[i]
        lat[x, y] = spin
    fname = os.path.join(folder, f"lat{T:.3f}.dat")
    np.savetxt(fname, lat, fmt='%d')

def wolff_step(S, L, nbr, beta):
    N = L * L
    p = 1 - np.exp(-2 * beta)
    visited = np.zeros(N, dtype=bool)
    k = np.random.randint(N)
    cluster = [k]
    visited[k] = True
    stack = [k]
    while stack:
        s = stack.pop()
        for l in nbr[s]:
            if not visited[l] and S[l] == S[s] and np.random.rand() < p:
                visited[l] = True
                stack.append(l)
                cluster.append(l)
    for site in cluster:
        S[site] *= -1
    return S, len(cluster)

def run_ising_simulation(L, Tmin, Tmax, nT, Ntrial, folder):
    os.makedirs(folder, exist_ok=True)
    T_list = np.linspace(Tmin, Tmax, nT)
    N = L * L
    nbr, site_dic, xy = square_neighbors(L)

    M_vals = []
    chi_vals = []

    for T in T_list:
        beta = 1 / T
        S = np.random.choice([-1, 1], N)
        M_list = []

        for _ in range(Ntrial):
            S, _ = wolff_step(S, L, nbr, beta)
            M_list.append(np.sum(S))

        M_arr = np.array(M_list)
        M_mean = np.mean(np.abs(M_arr)) / N
        M2_mean = np.mean(M_arr**2) / (N**2)
        chi = (N / T) * (M2_mean - M_mean**2)
        M_vals.append(M_mean)
        chi_vals.append(chi)
        save_latt(T, S, L, xy, folder)

    return T_list, M_vals, chi_vals
