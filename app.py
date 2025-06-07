# app.py
import streamlit as st
import numpy as np
from ising_model import simulate
from visualizer import plot_magnetization, plot_binder, plot_cluster_hist, fig_to_bytes

def main():
    st.title("伊辛模型模拟器 (Wolff群集算法)")

    with st.sidebar:
        L = st.slider("晶格边长 (L)", 10, 100, 20)
        lattice = st.selectbox("晶格类型", ["Square", "Triangular"])
        Tmin = st.number_input("最低温度", 0.1, 10.0, 1.0)
        Tmax = st.number_input("最高温度", Tmin, 10.0, 4.0)
        nT = st.slider("温度点数", 5, 50, 20)
        Ntrial = st.number_input("每个温度的试验次数", 10, 2000, 100)
        simulate_button = st.button("开始模拟")

    if simulate_button:
        with st.spinner("正在运行模拟..."):
            df, all_cluster_sizes = simulate(L, lattice, Tmin, Tmax, nT, Ntrial)

        st.subheader("模拟结果表格：")
        st.dataframe(df.round(5))

        st.subheader("磁化强度与磁化率：")
        fig1 = plot_magnetization(df)
        st.pyplot(fig1)
        st.download_button(
            label="下载 Magnetization 图像 (PNG)",
            data=fig_to_bytes(fig1),
            file_name="Magnetization_vs_T.png",
            mime="image/png"
        )

        st.subheader("Binder 比率：")
        fig2 = plot_binder(df)
        st.pyplot(fig2)
        st.download_button(
            label="下载 Binder 图像 (PNG)",
            data=fig_to_bytes(fig2),
            file_name="Binder_vs_T.png",
            mime="image/png"
        )

        st.subheader("所有温度下的群集大小分布：")
        fig3 = plot_cluster_hist(all_cluster_sizes)
        st.pyplot(fig3)
        st.download_button(
            label="下载 Cluster Size Histogram (PNG)",
            data=fig_to_bytes(fig3),
            file_name="ClusterSize_Distribution.png",
            mime="image/png"
        )

        csv = df.to_csv(index=False).encode()
        st.download_button(
            label="下载数据表 (CSV)",
            data=csv,
            file_name="Simulation_Data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
