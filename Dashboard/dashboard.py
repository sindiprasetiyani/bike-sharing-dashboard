import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Style clean 
sns.set_theme(style="whitegrid")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("dashboard/main_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# =========================
# SIDEBAR FILTER 
# =========================
st.sidebar.title("🔧 Filter Data")

start_date = st.sidebar.date_input("Start Date", df['dteday'].min())
end_date = st.sidebar.date_input("End Date", df['dteday'].max())

filtered_df = df[
    (df['dteday'] >= pd.to_datetime(start_date)) &
    (df['dteday'] <= pd.to_datetime(end_date))
]

# =========================
# HEADER 
# =========================
st.title("🚲 Bike Sharing Insights")
st.write("Analisis pola penggunaan sepeda berdasarkan waktu dan kondisi lingkungan")

# =========================
# METRICS 
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", int(filtered_df['total_rentals'].sum()))
col2.metric("Average per Day", int(filtered_df.groupby('dteday')['total_rentals'].sum().mean()))
col3.metric("Max Rentals", int(filtered_df['total_rentals'].max()))

# =========================
# TREND HARIAN
# =========================
st.markdown("## 📈 Analisis Tren Peminjaman Harian")

daily = filtered_df.groupby('dteday')['total_rentals'].sum().reset_index()

fig, ax = plt.subplots(figsize=(14,6))
ax.plot(
    daily['dteday'],
    daily['total_rentals'],
    linewidth=2,
    color='#1B2631'
)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

st.caption("Terlihat fluktuasi penggunaan yang dipengaruhi oleh waktu dan kondisi tertentu.")

# =========================
# POLA JAM
# =========================
st.markdown("## ⏰ Pola Penggunaan per Jam")

hourly = filtered_df.groupby('hr')['total_rentals'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(
    data=hourly,
    x='hr',
    y='total_rentals',
    marker='o',
    color='#1B2631',
    ax=ax
)
st.pyplot(fig)

st.caption("Puncak penggunaan terjadi pada jam sibuk (pagi & sore).")


# =========================
# MUSIM
# =========================
st.markdown("## 🌦️ Pengaruh Musim")

season = filtered_df.groupby('season')['total_rentals'].mean().reset_index()

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(
    data=season,
    x='season',
    y='total_rentals',
    color='#1B2631',
    ax=ax
)
st.pyplot(fig)

st.caption("Musim tertentu menunjukkan tingkat penggunaan lebih tinggi.")

# =========================
# SEGMENTASI
# =========================
st.markdown("## 📊 Segmentasi Penggunaan")

filtered_df['usage_category'] = pd.qcut(
    filtered_df['total_rentals'],
    q=3,
    labels=['Low', 'Medium', 'High']
)

fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(
    x='usage_category',
    data=filtered_df,
    color='#1B2631',
    ax=ax
)
st.pyplot(fig)

st.caption("Distribusi penggunaan menunjukkan variasi tingkat aktivitas pengguna.")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.write("Dashboard ini dibuat untuk analisis eksploratif penggunaan bike sharing.")