import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from ising_model import run_ising_simulation
from visualizer import generate_spin_plot

st.set_page_config(layout="wide")
st.title("2D Ising Model Simulator with Wolff Algorithm")

col1, col2 = st.columns(2)

with col1:
    lattice_size = st.slider("Lattice Size (L x L)", min_value=10, max_value=100, value=20, step=5)
    lattice_type = st.selectbox("Lattice Type", options=["Square", "Triangular"])
    n_trials = st.number_input("Monte Carlo Steps per Temperature", min_value=10, max_value=1000, value=100)

with col2:
    Tmin = st.number_input("Minimum Temperature", min_value=0.1, max_value=5.0, value=1.5, step=0.1)
    Tmax = st.number_input("Maximum Temperature", min_value=0.1, max_value=5.0, value=3.5, step=0.1)
    nT = st.slider("Number of Temperature Points", min_value=3, max_value=100, value=20)

if st.button("Run Simulation"):
    with st.spinner("Running Wolff algorithm simulation..."):
        results = run_ising_simulation(
            L=lattice_size,
            lattice=lattice_type,
            Ntrial=n_trials,
            Tmin=Tmin,
            Tmax=Tmax,
            nT=nT
        )

    st.success("Simulation completed!")

    # Magnetization and Susceptibility plot
    T_list = results["temperature"]
    M_list = results["magnetization"]
    Chi_list = results["susceptibility"]
    Mvar_list = results["Mvar"]

    fig1, ax1 = plt.subplots()
    ax1.errorbar(T_list, M_list, yerr=np.sqrt(Mvar_list), fmt='o-', label='Magnetization')
    ax1.set_ylabel("Magnetization", color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(T_list, Chi_list, 's--', color='tab:red', label='Susceptibility')
    ax2.set_ylabel("Susceptibility", color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    ax1.set_xlabel("Temperature")
    ax1.set_title("Magnetization and Susceptibility vs Temperature")
    fig1.tight_layout()
    st.pyplot(fig1)

    # Optional: display spin configuration at final temperature
    final_spin_config = results["final_spin"]
    fig2 = generate_spin_plot(final_spin_config)
    st.pyplot(fig2)

    # Optional: display spin ratio plot
    fig3 = results.get("spin_ratio_fig")
    if fig3:
        st.pyplot(fig3)

    # Optional: display hysteresis animation GIF if available
    gif_path = results.get("hysteresis_gif")
    if gif_path:
        st.image(gif_path, caption="Hysteresis Loop Animation")
