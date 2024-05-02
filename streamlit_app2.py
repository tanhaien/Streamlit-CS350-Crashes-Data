import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
df = pd.read_csv('2017_Crashes_10000_sample.csv')

# Tạo widget để người dùng nhập số 'top' mà họ muốn xem
top_n = st.number_input('Nhập số "top" tai nạn bạn muốn xem (ví dụ: 3, 5, 7, 10):', min_value=1, value=3)

# Tính toán top điều kiện thời tiết và giờ trong ngày có nhiều tai nạn nhất
top_weather_conditions = df['WEATH_COND_DESCR'].value_counts().head(top_n).index.tolist()
top_crash_hours = df['CRASH_HOUR'].value_counts().head(top_n).index.tolist()

# Vẽ biểu đồ số lượng va chạm dựa trên top điều kiện thời tiết
plt.figure(figsize=(10, 5))
plt.title(f'Số Lượng Va Chạm Dựa Trên Top {top_n} Điều Kiện Thời Tiết')
plt.xlabel('Điều Kiện Thời Tiết')
plt.ylabel('Số Lượng Va Chạm')
weather_crashes = df[df['WEATH_COND_DESCR'].isin(top_weather_conditions)].groupby('WEATH_COND_DESCR').size()
plt.bar(weather_crashes.index, weather_crashes.values)
st.pyplot(plt)

# Vẽ biểu đồ số lượng va chạm dựa trên top giờ trong ngày
plt.figure(figsize=(10, 5))
plt.title(f'Số Lượng Va Chạm Dựa Trên Top {top_n} Giờ Trong Ngày')
plt.xlabel('Giờ Trong Ngày')
plt.ylabel('Số Lượng Va Chạm')
hour_crashes = df[df['CRASH_HOUR'].isin(top_crash_hours)].groupby('CRASH_HOUR').size()
plt.bar(hour_crashes.index, hour_crashes.values)
st.pyplot(plt)
