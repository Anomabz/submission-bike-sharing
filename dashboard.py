import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page title
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("hour.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

hour_df = load_data()

# Sidebar: Filter Tahun
st.sidebar.header("Filter Data")
year_option = st.sidebar.selectbox("Pilih Tahun", options=[2011, 2012])
filtered_df = hour_df[hour_df['dteday'].dt.year == year_option]

# Dashboard Title
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown("Dashboard ini menampilkan insight utama dari perilaku penyewa sepeda berdasarkan waktu dan musim.")

# Layout Kolom untuk Metric Utama
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")
with col2:
    avg_temp = filtered_df['temp'].mean()
    st.metric("Rata-rata Suhu (Normalisasi)", value=f"{avg_temp:.2f}")
with col3:
    max_rentals = filtered_df['cnt'].max()
    st.metric("Puncak Sewa (Per Jam)", value=f"{max_rentals:,}")

st.divider()

# Visualisasi 1: Pola Jam
st.subheader("Pola Penyewaan Sepeda per Jam: Hari Kerja vs Hari Libur")
fig, ax = plt.subplots(figsize=(12, 5))
sns.pointplot(data=filtered_df, x='hr', y='cnt', hue='workingday', ax=ax)
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Rata-rata Sewa")
# Mengganti legenda
new_labels = ['Hari Libur', 'Hari Kerja']
for t, l in zip(ax.legend_.get_texts(), new_labels):
    t.set_text(l)
st.pyplot(fig)

# Visualisasi 2: Musim
st.subheader("Total Penyewaan Berdasarkan Musim")
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
filtered_df['season_label'] = filtered_df['season'].map(season_mapping)
season_data = filtered_df.groupby('season_label')['cnt'].sum().reindex(['Spring', 'Summer', 'Fall', 'Winter'])

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x=season_data.index, y=season_data.values, palette='viridis', ax=ax2)
ax2.set_ylabel("Total Penyewaan")
st.pyplot(fig2)

# Kesimpulan Singkat
st.info("Insight: Penyewaan mencapai puncak pada jam sibuk hari kerja (pagi & sore), sedangkan musim gugur (Fall) adalah periode yang paling diminati.")