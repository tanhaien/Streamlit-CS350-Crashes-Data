import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Giả sử 'data' là DataFrame chứa dữ liệu tai nạn với cột 'Severity'
data = pd.read_csv('2017_Crashes_10000_sample.csv')

# Placeholder cho việc tải dữ liệu thực tế
data = pd.DataFrame({
    'Severity': ['Fatal', 'Injury', 'Property Damage Only', 'Injury', 'Fatal']
})

# Giả sử 'data' là DataFrame chứa cột 'Severity'
severity_counts = data['Severity'].value_counts()
print(severity_counts)
severity_percentage = data['Severity'].value_counts(normalize=True) * 100
print(severity_percentage)


# Tạo user input để lọc dữ liệu
severity_filter = st.sidebar.multiselect('Chọn mức độ nghiêm trọng:', options=data['Severity'].unique(), default=data['Severity'].unique())

# Lọc dữ liệu dựa trên lựa chọn của người dùng
filtered_data = data[data['Severity'].isin(severity_filter)]

# Tính toán số lượng tai nạn cho mỗi mức độ nghiêm trọng
severity_counts = filtered_data['Severity'].value_counts()

