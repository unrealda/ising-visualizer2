import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
from ising_utils import run_simulation_and_generate, make_arrow_plot, make_hysteresis_plot, make_spin_ratio_plot

st.set_page_config(layout="wide")
st.title("2D Ising Model Simulator with Visualizations")

with st.sidebar:
    st.header("Simulation Parameters")
    L = st.slider("Lattice Size LxL", 10, 100, 20, step=10)
    lattice_type = st.selectbox("Lattice Type", ["Square", "Triangular"])
    Ntrial = st.slider("Monte Carlo Trials per T", 100, 1000, 200, step=100)
    Tmin = st.number_input("Minimum Temperature", value=1.0, step=0.1)
    Tmax = st.number_input("Maximum Temperature", value=4.0, step=0.1)
    nT = st.slider("Number of Temperature Points", 3, 30, 10)
    show_spin_ratio = st.checkbox("Show Spin Ratio Graph")
    show_hysteresis = st.checkbox("Show Hysteresis Animation")
    start = st.button("Start Simulation")

if start:
    folder = lattice_type.lower()
    os.makedirs(folder, exist_ok=True)
    st.info("Running simulation, please wait...")
    run_simulation_and_generate(L, lattice_type, Ntrial, Tmin, Tmax, nT)

    st.success("Simulation Complete!")

    st.header("Magnetization and Susceptibility")
    st.image(os.path.join(folder, "Magnetization_Chi.pdf"))

    st.header("Spin Configuration Arrows Animation")
    st.image(os.path.join(folder, f"{folder}_ising_arrows.gif"))

    if show_spin_ratio:
        st.header("Spin Up/Down Ratio vs Temperature")
        st.image(os.path.join(folder, "Spin_Ratio_vs_Temperature.png"))

    if show_hysteresis:
        st.header("Hysteresis Loop Across Temperatures")
        st.image(os.path.join(folder, "Hysteresis_AllTemps.gif"))
        st.subheader("Final Temperature Hysteresis Process")
        st.image(os.path.join(folder, "Hysteresis_FinalTemp.gif"))
