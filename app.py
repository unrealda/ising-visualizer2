import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from ising_model import run_ising_simulation  # 在 ising_model.py 中定义此函数
from visualizer import plot_spin_arrows, plot_spin_ratio_vs_temp
import os
import tempfile

# 页面配置
st.set_page_config(layout="wide", page_title="2D Ising Model Simulator")

st.title("🧊 2D Ising Model Simulator & Visualizer")
st.markdown("""
本平台使用 **Wolff 算法** 进行二维伊辛模型模拟，支持：
- 🔁 温度扫描
- 🎯 自旋箭头动画（红↑蓝↓）
- 📈 自旋比例图
- 🌀 磁滞回线（最终温度）
""")

# 用户输入参数
with st.sidebar:
    st.header("⚙️ 模拟参数")
    L = st.slider("晶格边长 L", 10, 100, 20)
    Ntrial = st.slider("每个温度的迭代次数", 10, 500, 100)
    Tmin = st.number_input("最低温度 Tmin", min_value=0.1, value=1.0)
    Tmax = st.number_input("最高温度 Tmax", min_value=Tmin+0.1, value=3.5)
    nT = st.slider("温度步数 nT", 3, 50, 20)
    lattice_type = st.selectbox("晶格类型", ["Square", "Triangular"])

# 开始模拟
if st.button("▶️ 开始模拟"):
    with st.spinner("正在进行伊辛模型模拟，请稍候..."):
        outdir = tempfile.mkdtemp()
        result = run_ising_simulation(
            L=L,
            Tmin=Tmin,
            Tmax=Tmax,
            nT=nT,
            Ntrial=Ntrial,
            Lattice=lattice_type,
            outdir=outdir
        )

        st.success("✅ 模拟完成！")

        # 分页显示结果
        st.subheader("🎯 自旋箭头图")
        idx = st.slider("选择温度帧索引", 0, nT - 1, 0)
        fig_arrow = plot_spin_arrows(result["spin_configs"][idx], result["temps"][idx])
        st.pyplot(fig_arrow)

        st.subheader("📊 自旋比例图")
        fig_ratio = plot_spin_ratio_vs_temp(result["temps"], result["up_ratios"], result["down_ratios"])
        st.pyplot(fig_ratio)

        st.subheader("📈 磁化率 & 磁化强度")
        fig_mag = plt.figure(figsize=(8,4))
        plt.plot(result["temps"], result["magnetizations"], 'r-o', label='Magnetization')
        plt.plot(result["temps"], result["susceptibilities"], 'b-s', label='Susceptibility')
        plt.xlabel("Temperature")
        plt.title("Magnetization & Susceptibility")
        plt.legend()
        plt.grid(True)
        st.pyplot(fig_mag)

        st.subheader("🌀 最终温度磁滞回线")
        fig_hys = plt.figure(figsize=(6,4))
        plt.plot(result["H_vals"], result["hysteresis"], 'o-', linewidth=1.5)
        plt.xlabel("External Field H")
        plt.ylabel("Magnetization")
        plt.title(f"Hysteresis at T = {result['T_final']:.2f}")
        plt.grid(True)
        st.pyplot(fig_hys)

        st.info(f"📁 所有数据已保存在临时目录: `{outdir}`，模拟结果不会长期保存，请及时下载。")
