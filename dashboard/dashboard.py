import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 📊 membaca dataset
df = pd.read_csv("dashboard/main_data.csv", parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"])

# 🏆 judul
st.title("📦 Analisis Data Pesanan E-Commerce")

# 📅 menambahkan kolom nama hari
df['order_weekday'] = df['order_purchase_timestamp'].dt.day_name()

# 📈 hitung jumlah pesanan per hari dalam seminggu
weekday_orders = df['order_weekday'].value_counts().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

# 📊 visualisasi jumlah pesanan per hari
def plot_weekday_orders():
    max_value = weekday_orders.max()
    colors = ['#08306b' if value == max_value else '#c6dbef' for value in weekday_orders]
    fig, ax = plt.subplots()
    ax.bar(weekday_orders.index, weekday_orders.values, color=colors)
    ax.set_xlabel("Hari dalam Seminggu")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Jumlah Pesanan per Hari dalam Seminggu")
    st.pyplot(fig)

# ⏰ hitung jumlah pesanan per jam
df['order_hour'] = df['order_purchase_timestamp'].dt.hour
hourly_orders = df['order_hour'].value_counts().sort_index()

# 📊 visualisasi jumlah pesanan per jam
def plot_hourly_orders():
    colors = sns.color_palette("Blues", len(hourly_orders))
    fig, ax = plt.subplots()
    ax.bar(hourly_orders.index, hourly_orders.values, color=colors, edgecolor="black")
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Jumlah Pesanan per Jam dalam Sehari")
    ax.set_xticks(range(24))
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

# 🚚 visualisasi rata-rata waktu pengiriman
df['delivery_duration'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
avg_delivery_time = df['delivery_duration'].mean()
def plot_delivery_distribution():
    fig, ax = plt.subplots()
    sns.histplot(df['delivery_duration'], bins=30, kde=True, color='skyblue', ax=ax)
    ax.axvline(avg_delivery_time, color='red', linestyle='dashed', linewidth=2, label=f'📌 Rata-rata: {avg_delivery_time:.2f} hari')
    ax.set_title("Rata-rata Waktu Pengiriman")
    ax.set_xlabel("Hari")
    ax.set_ylabel("Frekuensi")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

# 📆 visualisasi jumlah pesanan per bulan
df['order_month'] = df['order_purchase_timestamp'].dt.to_period("M")
monthly_orders = df['order_month'].value_counts().sort_index()
max_orders_month = monthly_orders.idxmax()
max_orders_value = monthly_orders.max()
def plot_monthly_orders():
    fig, ax = plt.subplots()
    plt.xticks(rotation=60)
    ax.plot(monthly_orders.index.astype(str), monthly_orders.values, marker='o', linestyle='-', color='b', label='📦 Jumlah Pesanan')
    ax.axvline(str(max_orders_month), color='r', linestyle='dashed', label='🔥 Puncak Pesanan')
    ax.scatter(str(max_orders_month), max_orders_value, color='red', zorder=3)
    ax.text(str(max_orders_month), max_orders_value, f"{max_orders_month} ({max_orders_value})", verticalalignment='bottom', horizontalalignment='right', fontsize=10, color='red')
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Jumlah Pesanan per Bulan")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

# 🚚 kategori waktu pengiriman
bins = [0, 3, 7, float("inf")]
labels = ["cepat", "normal", "lama"]
df["delivery_category"] = pd.cut(df["delivery_duration"], bins=bins, labels=labels)
delivery_distribution = df["delivery_category"].value_counts()
def plot_delivery_category():
    sorted_categories = delivery_distribution.sort_values(ascending=False)
    colors = plt.cm.Blues_r(np.linspace(0.3, 1, len(sorted_categories)))
    fig, ax = plt.subplots()
    ax.bar(sorted_categories.index, sorted_categories.values, color=colors, edgecolor="black")
    ax.set_xlabel("Kategori Waktu Pengiriman")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Kategori Waktu Pengiriman Pesanan")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

# 📦 distribusi lama pengiriman
def plot_delivery_days():
    fig, ax = plt.subplots()
    sns.histplot(df["delivery_days"], bins=20, kde=True, color="blue", ax=ax)
    ax.set_xlabel("Hari Pengiriman")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Distribusi Pengiriman Pesanan")
    st.pyplot(fig)

# ❌ hubungan waktu pengiriman dengan tingkat pembatalan
df["is_canceled_or_refunded"] = (df["order_status"] == "canceled").astype(int)
cancel_refund_rate = df.groupby("delivery_category", observed=True)["is_canceled_or_refunded"].mean() * 100
def plot_cancel_refund_rate():
    fig, ax = plt.subplots()
    sns.barplot(x=cancel_refund_rate.index, y=cancel_refund_rate.values, hue=cancel_refund_rate.index, palette=["lightblue", "steelblue", "darkblue"], legend=False, ax=ax)
    ax.set_xlabel("Kategori Waktu Pengiriman")
    ax.set_ylabel("Tingkat Pembatalan/Refund (%)")
    ax.set_title("Tingkat Pembatalan/Refund Berdasarkan Kategori Pengiriman")
    st.pyplot(fig)

# 📌 sidebar
st.sidebar.header("📊 Pilih Visualisasi")
options = {
    "📅 Jumlah Pesanan per Hari": plot_weekday_orders,
    "⏰ Jumlah Pesanan per Jam": plot_hourly_orders,
    "🚚 Rata-rata Waktu Pengiriman": plot_delivery_distribution,
    "📆 Jumlah Pesanan per Bulan": plot_monthly_orders,
    "🚀 Kategori Waktu Pengiriman": plot_delivery_category,
    "📦 Distribusi Pengiriman Pesanan": plot_delivery_days,
    "❌ Tingkat Pembatalan/Refund": plot_cancel_refund_rate
}
selected_option = st.sidebar.selectbox("🛒 Pilih Grafik", list(options.keys()))
options[selected_option]()

st.sidebar.markdown("---")
st.sidebar.markdown("💡 **Tips:** Pilih kategori di atas untuk melihat visualisasi")