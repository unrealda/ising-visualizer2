import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
from io import BytesIO
from ising_model import run_ising_simulation
from visualizer import generate_arrow_plot

st.set_page_config(layout="wide")
st.title("2D Ising Model Visualizer - Wolff Algorithm")

# Initialize session state
if 'simulation_done' not in st.session_state:
    st.session_state.simulation_done = False

st.sidebar.header("Simulation Parameters")
L = st.sidebar.slider("Lattice size (LxL)", 8, 64, 16)
Tmin = st.sidebar.number_input("Minimum Temperature", value=1.5)
Tmax = st.sidebar.number_input("Maximum Temperature", value=3.5)
nT = st.sidebar.slider("Number of Temperature Steps", 5, 100, 20)
Ntrial = st.sidebar.slider("MC Trials per Temperature", 10, 1000, 100)

# Run button
if st.sidebar.button("Run Simulation"):
    with st.spinner("Running simulation and generating plots..."):
        folder = "sim_output"
        os.makedirs(folder, exist_ok=True)
        T_list, spin_configs, M, Chi = run_ising_simulation(L, Tmin, Tmax, nT, Ntrial, folder)

        st.session_state.simulation_done = True
        st.session_state.T_list = T_list
        st.session_state.M = M
        st.session_state.Chi = Chi
        st.session_state.spin_snapshots = spin_configs

        st.success("Simulation complete!")

# If data exists, show results
if st.session_state.simulation_done:
    T_list = st.session_state.T_list
    M = st.session_state.M
    Chi = st.session_state.Chi
    spin_configs = st.session_state.spin_snapshots

    # Show magnetization and susceptibility plot
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.set_xlabel('Temperature')
    ax1.set_ylabel('Magnetization', color=color)
    ax1.plot(T_list, M, 'o-', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Susceptibility', color=color)
    ax2.plot(T_list, Chi, 's--', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    st.pyplot(fig)

    # Snapshot selection
    t_idx = st.slider("Select temperature snapshot to visualize", 0, len(T_list)-1, 0)
    snapshot = spin_configs[t_idx]
    T = T_list[t_idx]
    Lx, Ly = snapshot.shape

    # Create arrow plot using text() with color
    fig2, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, Ly+1)
    ax.set_ylim(0, Lx+1)
    ax.set_aspect('equal')
    ax.axis('off')

    up_count = 0
    down_count = 0
    for x in range(Ly):
        for y in range(Lx):
            if snapshot[y, x] == 1:
                ax.text(x+1, Lx-y, '\u2191', ha='center', va='center', fontsize=14, color='red')
                up_count += 1
            else:
                ax.text(x+1, Lx-y, '\u2193', ha='center', va='center', fontsize=14, color='blue')
                down_count += 1

    ax.set_title(f'T = {T:.3f} | ↑: {up_count}, ↓: {down_count}', fontsize=14)
    st.pyplot(fig2)

    # Download button
    buf = BytesIO()
    fig2.savefig(buf, format="png")
    st.download_button("Download Snapshot Image", data=buf.getvalue(), file_name="ising_snapshot.png", mime="image/png")
else:
    st.info("Set parameters and click 'Run Simulation' to begin.")
