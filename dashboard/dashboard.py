import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

sns.set_theme(style="whitegrid")

df = pd.read_csv("dashboard/main_data.csv")

# pastikan tipe datetime
df['dteday'] = pd.to_datetime(df['dteday'])

st.sidebar.title("🔧 Filter Data")

min_date = df['dteday'].min()
max_date = df['dteday'].max()

start_date = st.sidebar.date_input("Start Date", min_date)
end_date = st.sidebar.date_input("End Date", max_date)

filtered_df = df[
    (df['dteday'] >= pd.to_datetime(start_date)) &
    (df['dteday'] <= pd.to_datetime(end_date))
]


st.title("🚲 Bike Sharing Insights")
st.markdown("Analisis penggunaan sepeda berdasarkan waktu dan kondisi lingkungan")

total_rentals = filtered_df['total_rentals'].sum()
avg_rentals = filtered_df['total_rentals'].mean()
max_rentals = filtered_df['total_rentals'].max()

col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", f"{int(total_rentals):,}")
col2.metric("Average per Hour", f"{int(avg_rentals)}")
col3.metric("Max Rentals", f"{int(max_rentals)}")

# =========================
# PERTANYAAN 1
# =========================
st.subheader("📊 Pengaruh Musim & Cuaca")

col1, col2 = st.columns(2)

# SEASON
season_avg = filtered_df.groupby("season")["total_rentals"].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(
    data=season_avg,
    x="season",
    y="total_rentals",
    color="#1B2631",
    ax=ax1
)
ax1.set_title("Average Rentals by Season")
ax1.set_xlabel("Season")
ax1.set_ylabel("Average Rentals")

col1.pyplot(fig1)

# WEATHER
weather_avg = filtered_df.groupby("weathersit")["total_rentals"].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(
    data=weather_avg,
    x="weathersit",
    y="total_rentals",
    color="#1B2631",
    ax=ax2
)
ax2.set_title("Average Rentals by Weather")
ax2.set_xlabel("Weather Condition")
ax2.set_ylabel("Average Rentals")

plt.xticks(rotation=25)
col2.pyplot(fig2)

# =========================
# PERTANYAAN 2
# =========================
st.subheader("⏰ Pola Penggunaan Sepeda (Weekday vs Weekend)")

hourly_pattern = (
    filtered_df.groupby(['hr','day_type'])['total_rentals']
    .mean()
    .reset_index()
)

fig3, ax3 = plt.subplots(figsize=(10,5))

sns.lineplot(
    data=hourly_pattern,
    x='hr',
    y='total_rentals',
    hue='day_type',
    ax=ax3
)

ax3.set_title("Bike Usage Pattern per Hour")
ax3.set_xlabel("Hour")
ax3.set_ylabel("Average Rentals")

st.pyplot(fig3)


st.subheader("📈 Tren Bulanan")

filtered_df['month_year'] = filtered_df['dteday'].dt.to_period('M')

monthly = (
    filtered_df.groupby('month_year')['total_rentals']
    .mean()
    .reset_index()
)

monthly['month_year'] = monthly['month_year'].astype(str)

fig4, ax4 = plt.subplots(figsize=(10,4))

sns.lineplot(
    data=monthly,
    x='month_year',
    y='total_rentals',
    color="#1B2631",
    ax=ax4
)

ax4.set_title("Monthly Trend of Rentals")
ax4.set_xlabel("Month")
ax4.set_ylabel("Average Rentals")

plt.xticks(rotation=45)

st.pyplot(fig4)

st.markdown("---")
st.caption("Dibuat untuk submission Dicoding - Data Scientist 🚀")