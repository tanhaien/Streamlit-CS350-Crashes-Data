import pandas as pd
import streamlit as st

#B1 : Tham khảo atributes trên trang chủ
#B2 : Lấy những dữ liệu và bảng biểu đã được phân tích
#B3 : Vẽ biểu đồ

# Đọc dữ liệu từ file CSV
df = pd.read_csv('2017_Crashes_10000_sample.csv')

# Phân tích Severity Breakdown
severity_counts = df['CRASH_SEVERITY_DESCR'].value_counts()
st.bar_chart(severity_counts)

# Phân tích Crash Characteristics
crash_types = df['MANR_COLL_DESCR'].value_counts()
st.bar_chart(crash_types)

# Phân tích Temporal Patterns
crash_by_hour = df['CRASH_HOUR'].value_counts()
st.bar_chart(crash_by_hour)

# Phân tích Vehicle Involvement
vehicle_types = df['VEHC_CONFIG_CL'].value_counts()
st.bar_chart(vehicle_types)

