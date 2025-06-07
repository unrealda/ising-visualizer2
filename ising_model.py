# ising_model.py
import numpy as np
import pandas as pd
from collections import deque

def square_neighbors(L):
    neighbors = {}
    for i in range(L):
        for j in range(L):
            site = i * L + j
            neighbors[site] = []
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = (i+dx)%L, (j+dy)%L
                neighbor_site = ni * L + nj
                neighbors[site].append(neighbor_site)
    return neighbors

def triangular_neighbors(L):
    neighbors = {}
    for i in range(L):
        for j in range(L):
            site = i * L + j
            neighbors[site] = []
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,1),(1,-1)]:
                ni, nj = (i+dx)%L, (j+dy)%L
                neighbor_site = ni * L + nj
                neighbors[site].append(neighbor_site)
    return neighbors

def wolff_algorithm(L, neighbors, T, Ntrial):
    N = L * L
    beta = 1.0 / T
    p = 1 - np.exp(-2 * beta)
    S = np.random.choice([-1, 1], size=N)
    M_list = []
    cluster_sizes = []

    for _ in range(Ntrial):
        seed = np.random.randint(N)
        cluster = set([seed])
        pocket = deque([seed])

        while pocket:
            site = pocket.pop()
            for neigh in neighbors[site]:
                if S[neigh] == S[site] and neigh not in cluster and np.random.rand() < p:
                    cluster.add(neigh)
                    pocket.append(neigh)
        S[list(cluster)] *= -1
        M = np.sum(S) / N
        M_list.append(M)
        cluster_sizes.append(len(cluster))

    return M_list, cluster_sizes

def simulate(L, lattice, Tmin, Tmax, nT, Ntrial):
    if lattice.lower() == 'square':
        neighbors = square_neighbors(L)
    elif lattice.lower() == 'triangular':
        neighbors = triangular_neighbors(L)
    else:
        raise ValueError("Unknown lattice type")

    T_list = np.linspace(Tmin, Tmax, nT)
    M_mean = []
    M_var = []
    Chi = []
    Binder = []
    all_cluster_sizes = []

    for T in T_list:
        M_list, cluster_sizes = wolff_algorithm(L, neighbors, T, Ntrial)
        M_arr = np.array(M_list)
        M_abs = np.abs(M_arr)
        M_mean.append(np.mean(M_abs))
        M_var.append(np.var(M_arr))
        Chi.append(L*L * (np.mean(M_arr**2) - np.mean(M_abs)**2) / T)
        M2 = np.mean(M_arr**2)
        M4 = np.mean(M_arr**4)
        Binder.append(1 - M4 / (3 * M2**2))
        all_cluster_sizes.extend(cluster_sizes)

    result_df = pd.DataFrame({
        "Temperature": T_list,
        "Magnetization": M_mean,
        "Magnetization_Var": M_var,
        "Susceptibility": Chi,
        "Binder_Ratio": Binder
    })

    return result_df, all_cluster_sizes
