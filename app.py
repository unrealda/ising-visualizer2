import streamlit as st
from visualizer import generate_hysteresis_loop, generate_final_hysteresis_animation

def main():
    st.title("伊辛模型模拟与磁滞回线")

    # 用户输入
    L = st.slider("选择格子大小 L (例如：10)", min_value=5, max_value=20, value=10)
    Tmin = st.slider("选择最小温度 Tmin (例如：0.5)", min_value=0.1, max_value=3.0, value=0.5)
    Tmax = st.slider("选择最大温度 Tmax (例如：3.0)", min_value=0.1, max_value=3.0, value=3.0)
    nT = st.slider("选择温度步数 (例如：50)", min_value=10, max_value=100, value=50)
    Ntrial = st.slider("选择试验次数 (例如：100)", min_value=10, max_value=500, value=100)
    lattice_type = st.selectbox("选择格子类型", ("Square", "Triangular"))

    key = f"{lattice_type}_L{L}_Tmin{Tmin}_Tmax{Tmax}"

    if st.button("生成磁滞回线与图像"):
        with st.spinner("生成中..."):
            # 生成磁滞回线
            generate_hysteresis_loop(L, lattice_type, Tmin, Tmax, nT, Ntrial, key)
            
            # 生成最终温度下的磁滞回线动画
            gif_path = generate_final_hysteresis_animation(L, lattice_type, Tmin, Tmax, nT, Ntrial, key)
            st.success("生成完毕！")
            st.image(gif_path, caption="最终温度的磁滞回线动画", use_column_width=True)

if __name__ == "__main__":
    main()
