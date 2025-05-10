import numpy as np
import matplotlib.pyplot as plt
import imageio
from ising_model import run_ising_model

def save_lattice(T, S, L, site_dic, xy_dic, key):
    lattice = np.zeros((L, L))
    for i in range(len(S)):
        row, col = xy_dic[i]
        lattice[row, col] = S[i]
    filename = f"{key}/{key}_lat_{T:.3f}.dat"
    np.savetxt(filename, lattice, fmt="%d")

def generate_hysteresis_loop(L, Lattice, Tmin, Tmax, nT, Ntrial, key):
    T_num, M, Mvar, M2, Chi, Mean_cluster_size = run_ising_model(L, Lattice, Tmin, Tmax, nT, Ntrial)

    fig, ax1 = plt.subplots()
    ax1.errorbar(T_num, M, yerr=np.sqrt(Mvar), fmt="x--", label="Magnetization")
    ax1.set_ylabel("Magnetization")
    
    ax2 = ax1.twinx()
    ax2.plot(T_num, Chi, "o-r", linewidth=1.2, label="Susceptibility")
    ax2.set_ylabel(r"$\chi = (\langle M^2 \rangle - \langle |M| \rangle^2)$")

    ax1.set_xlabel("Temperature")
    ax1.set_title(f"Magnetization and Susceptibility vs Temperature ({L}x{L} {Lattice} Lattice)")
    fig.grid(True)
    plt.tight_layout()

    plt.savefig(f"{key}/Magnetization_Chi.pdf")

def generate_final_hysteresis_animation(L, Lattice, Tmin, Tmax, nT, Ntrial, key):
    T_num, M, Mvar, M2, Chi, Mean_cluster_size = run_ising_model(L, Lattice, Tmin, Tmax, nT, Ntrial)
    
    # Final temperature and hysteresis loop
    final_T = T_num[-1]
    H_vals = np.concatenate([np.arange(-1, 1.1, 0.05), np.arange(0.95, -1, -0.05)])
    M_H = np.zeros(len(H_vals))

    for h_idx, H in enumerate(H_vals):
        # Simulate and store magnetization for each external field H
        pass  # Simulate hysteresis loop (similar to ising_model)

    # Generate animated GIF of hysteresis loop
    images = []
    fig, ax = plt.subplots()
    for i in range(len(H_vals)):
        ax.clear()
        ax.plot(H_vals[:i+1], M_H[:i+1], "o-", linewidth=1.5, color="r")
        ax.set_title(f"Final Hysteresis Loop at T = {final_T:.2f}")
        ax.set_xlabel("External Field H")
        ax.set_ylabel("Magnetization")
        ax.set_xlim([-1.1, 1.1])
        ax.set_ylim([-1.1, 1.1])
        ax.grid(True)

        frame_path = f"{key}/temp_frame_{i}.png"
        fig.savefig(frame_path)
        images.append(imageio.imread(frame_path))

    gif_path = f"{key}/Hysteresis_Final_Temperature.gif"
    imageio.mimsave(gif_path, images, duration=0.08)
    return gif_path
