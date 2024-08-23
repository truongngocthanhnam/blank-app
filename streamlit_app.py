import streamlit as st
import numpy as np
import pandas as pd

# Hàm tính toán diện tích thép
def calculate_steel_area(concrete_strength, steel_strength, bending_moment, effective_depth):
    # Tính toán mô men kháng
    concrete_modulus = 0.85 * concrete_strength
    steel_modulus = steel_strength
    neutral_axis_depth = (bending_moment / (concrete_modulus * effective_depth * 1000)) ** (1/2)
    steel_area = bending_moment / (steel_modulus * (effective_depth - neutral_axis_depth))
    return steel_area

# Hàm tính toán diện tích thép cho một thanh dầm
def beam_design(concrete_strength, steel_strength, bending_moment, shear_force, width, effective_depth):
    # Tính toán diện tích thép cho uốn
    steel_area_bending = calculate_steel_area(concrete_strength, steel_strength, bending_moment, effective_depth)

    # Tính toán diện tích thép cho cắt
    steel_area_shear = 0.5 * shear_force / (steel_strength * (effective_depth - 0.5 * width))

    # Tính toán diện tích thép tổng
    steel_area_total = max(steel_area_bending, steel_area_shear)

    return steel_area_total

# Giao diện Streamlit
st.title("Ứng dụng thiết kế bê tông cốt thép đơn giản theo Eurocode")

# Nhập thông tin vật liệu
concrete_strength = st.number_input("Cường độ bê tông (MPa)", min_value=10, max_value=100, value=25)
steel_strength = st.number_input("Cường độ thép (MPa)", min_value=200, max_value=1000, value=500)

# Nhập thông tin thiết kế
width = st.number_input("Chiều rộng dầm (mm)", min_value=100, max_value=1000, value=200)
effective_depth = st.number_input("Chiều cao hữu dụng dầm (mm)", min_value=100, max_value=1000, value=400)
bending_moment = st.number_input("Mô men uốn (kNm)", min_value=1, max_value=1000, value=100)
shear_force = st.number_input("Lực cắt (kN)", min_value=1, max_value=1000, value=50)

# Tính toán và hiển thị kết quả
steel_area = beam_design(concrete_strength, steel_strength, bending_moment * 1000, shear_force * 1000, width, effective_depth)

st.write("Diện tích thép cần thiết: ", steel_area, "mm²")

# Bảng hiển thị kết quả
st.subheader("Kết quả")
data = {
    "Tham số": ["Cường độ bê tông (MPa)", "Cường độ thép (MPa)", "Chiều rộng dầm (mm)", "Chiều cao hữu dụng dầm (mm)", "Mô men uốn (kNm)", "Lực cắt (kN)", "Diện tích thép (mm²)"],
    "Giá trị": [concrete_strength, steel_strength, width, effective_depth, bending_moment, shear_force, steel_area]
}
df = pd.DataFrame(data)
st.table(df)
