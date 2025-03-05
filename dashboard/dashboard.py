import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# baca dataset
df = pd.read_csv("dashboard/main_data.csv", parse_dates=['order_purchase_timestamp'])  

# sidebar 
st.sidebar.header("Filter Data")
min_date = df['order_purchase_timestamp'].min().date()
max_date = df['order_purchase_timestamp'].max().date()

start_date = st.sidebar.date_input("Mulai Tanggal", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Akhir Tanggal", max_date, min_value=min_date, max_value=max_date)

# filter data berdasarkan tanggal
filtered_df = df[(df['order_purchase_timestamp'].dt.date >= start_date) & (df['order_purchase_timestamp'].dt.date <= end_date)]

st.title("Dashboard Analisis Pesanan")
st.write(f"Menampilkan data dari {start_date} hingga {end_date}")

# rata-rata waktu pengiriman berdasarkan status pesanan
agg_data = filtered_df.groupby('order_status')['delivery_duration'].mean().reset_index()
st.subheader("Rata-rata Durasi Pengiriman berdasarkan Status Pesanan")
st.dataframe(agg_data)

# visualisasi distribusi durasi pengiriman
st.subheader("Distribusi Durasi Pengiriman")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_df['delivery_duration'], bins=30, kde=True, ax=ax)
ax.set_xlabel("Durasi Pengiriman (hari)")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# visualisasi jumlah pesanan per bulan
filtered_df['order_month'] = filtered_df['order_purchase_timestamp'].dt.to_period('M')
monthly_orders = filtered_df['order_month'].value_counts().sort_index()
max_orders_month = monthly_orders.idxmax()
max_orders_value = monthly_orders.max()

st.subheader("Jumlah Pesanan per Bulan")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_orders.index.astype(str), monthly_orders.values, marker='o', linestyle='-', color='b', label='Jumlah Pesanan')
ax.axvline(str(max_orders_month), color='r', linestyle='dashed', label='Puncak Pesanan')
ax.scatter(str(max_orders_month), max_orders_value, color='red', zorder=3)
ax.text(str(max_orders_month), max_orders_value, f"{max_orders_month} ({max_orders_value})", verticalalignment='bottom', horizontalalignment='right', fontsize=10, color='red')
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.set_title("Jumlah Pesanan per Bulan")
ax.legend()
ax.grid()
st.pyplot(fig)

st.write("Dashboard ini menampilkan data berdasarkan rentang tanggal yang dipilih.")