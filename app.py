import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from ising_model import run_ising_simulation, generate_lattice_frame, simulate_hysteresis
from visualizer import create_arrow_plot, create_spin_ratio_plot, create_hysteresis_animation

st.set_page_config(layout="wide")
st.title("🎯 2D Ising Model Simulator with Wolff Algorithm")

# Sidebar parameters
st.sidebar.header("Simulation Parameters")
L = st.sidebar.slider("Lattice size (L x L)", 10, 100, 20)
Tmin = st.sidebar.slider("Minimum Temperature", 0.5, 5.0, 1.5, step=0.1)
Tmax = st.sidebar.slider("Maximum Temperature", 0.5, 5.0, 3.5, step=0.1)
nT = st.sidebar.slider("Number of Temperatures", 3, 30, 10)
Ntrial = st.sidebar.slider("Monte Carlo Trials per T", 10, 500, 100)
Lattice = st.sidebar.selectbox("Lattice Type", ["Square", "Triangular"])

if st.sidebar.button("Run Simulation"):
    with st.spinner("Running Ising simulation..."):
        T_list, M_list, Chi_list, final_spins, spin_ratios = run_ising_simulation(L, Lattice, Tmin, Tmax, nT, Ntrial)
        st.success("Simulation completed.")

        # Magnetization and Susceptibility plot
        fig1, ax1 = plt.subplots()
        ax1.errorbar(T_list, M_list, fmt='x--', label='Magnetization')
        ax2 = ax1.twinx()
        ax2.plot(T_list, Chi_list, 'r-o', label='Susceptibility')
        ax1.set_xlabel("Temperature")
        ax1.set_ylabel("Magnetization")
        ax2.set_ylabel("Susceptibility")
        ax1.set_title("Magnetization and Susceptibility vs Temperature")
        st.pyplot(fig1)

        # Arrow plot animation and final spin configuration
        st.markdown("### Final Spin Configuration")
        arrow_fig = create_arrow_plot(final_spins, spin_ratios[-1], T_list[-1])
        st.pyplot(arrow_fig)

        st.markdown("### Spin Direction Ratios")
        fig_ratio = create_spin_ratio_plot(T_list, spin_ratios)
        st.pyplot(fig_ratio)

        # Hysteresis loop animation
        st.markdown("### Hysteresis Loop (GIF)")
        gif_path = create_hysteresis_animation(L, Lattice, T_list, Ntrial, peak_temperature=T_list[np.argmax(Chi_list)])
        with open(gif_path, "rb") as f:
            st.image(f.read(), format="gif")
