import numpy as np

def square_neighbors(L):
    N = L * L
    site_dic = {}
    x_y_dic = []
    
    for j in range(N):
        row = j // L
        col = j % L
        key = f"{row},{col}"
        site_dic[key] = j
        x_y_dic.append([row, col])
        
    nbr = []
    for j in range(N):
        row, col = x_y_dic[j]
        neighbors = [
            site_dic.get(f"{row},{(col + 1) % L}"),
            site_dic.get(f"{(row + 1) % L},{col}"),
            site_dic.get(f"{row},{(col - 1) % L}"),
            site_dic.get(f"{(row - 1) % L},{col}")
        ]
        nbr.append(neighbors)
    
    return nbr, site_dic, x_y_dic

def triangular_neighbors(L):
    N = L * L
    site_dic = {}
    x_y_dic = []
    
    for j in range(N):
        row = j // L
        col = j % L
        key = f"{row},{col}"
        site_dic[key] = j
        x_y_dic.append([row, col])
        
    nbr = []
    for j in range(N):
        row, col = x_y_dic[j]
        neighbors = [
            site_dic.get(f"{row},{(col + 1) % L}"),
            site_dic.get(f"{(row + 1) % L},{col}"),
            site_dic.get(f"{row},{(col - 1) % L}"),
            site_dic.get(f"{(row - 1) % L},{col}"),
            site_dic.get(f"{(row + 1) % L},{(col - 1) % L}"),
            site_dic.get(f"{(row - 1) % L},{(col + 1) % L}")
        ]
        nbr.append(neighbors)
    
    return nbr, site_dic, x_y_dic

def run_ising_model(L, Lattice, Tmin, Tmax, nT, Ntrial):
    if Lattice == 'Square':
        nbr, site_dic, x_y_dic = square_neighbors(L)
    elif Lattice == 'Triangular':
        nbr, site_dic, x_y_dic = triangular_neighbors(L)
    else:
        raise ValueError("Invalid lattice type.")

    N = L * L
    T_num = np.linspace(Tmin, Tmax, nT)
    M = np.zeros(nT)
    Mvar = np.zeros(nT)
    M2 = np.zeros(nT)
    Chi = np.zeros(nT)
    Mean_cluster_size = np.zeros(nT)

    for i, t in enumerate(T_num):
        beta = 1.0 / t
        p = 1 - np.exp(-2 * beta)
        S = 2 * (np.random.randint(2, size=N) - 1) - 1

        N_cluster_size = np.zeros(Ntrial)
        Magnetization = np.zeros(Ntrial)

        for itera in range(Ntrial):
            k = np.random.randint(N)
            Pocket = [k]
            Cluster = [k]

            while Pocket:
                s = Pocket[np.random.randint(len(Pocket))]
                for l in nbr[s]:
                    if S[l] == S[s] and l not in Cluster and np.random.rand() < p:
                        Pocket.append(l)
                        Cluster.append(l)
                Pocket = [x for x in Pocket if x != s]

            N_cluster_size[itera] = len(Cluster)
            S[Cluster] = -S[Cluster]
            Magnetization[itera] = np.sum(S)
        
        # Collect results for further analysis
        M[i] = np.mean(np.abs(Magnetization)) / N
        M2[i] = np.mean(Magnetization**2) / N**2
        Mvar[i] = np.var(Magnetization / N) / N
        Chi[i] = (N / t) * (M2[i] - M[i]**2)
        Mean_cluster_size[i] = np.mean(N_cluster_size)

    return T_num, M, Mvar, M2, Chi, Mean_cluster_size
