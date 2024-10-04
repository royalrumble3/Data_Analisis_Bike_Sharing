import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

st.title('Bike Sharing Dashboard')

# Fungsi untuk plot pola peminjaman sepeda
def plot_daily_rentals(day_df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(day_df.index, day_df['registered'], label='Registered')
    ax.plot(day_df.index, day_df['casual'], label='Casual')
    ax.set_title('Pola Peminjaman Sepeda Terdaftar dan Tidak Terdaftar dari Waktu ke Waktu (Dataset Harian)')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah')
    ax.legend()
    ax.tick_params(rotation=45)
    return fig

# Fungsi untuk plot pengaruh musim terhadap penggunaan sepeda
def plot_seasonal_effect(day_df):
    seasonal_data = day_df.groupby('season')['cnt'].mean()
    season_names = ['Spring', 'Summer', 'Fall', 'Winter']
    fig, ax = plt.subplots()
    ax.bar(season_names, seasonal_data)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Jumlah Sewa Harian')
    ax.set_title('Pengaruh Musim Terhadap Penggunaan Sepeda')
    return fig

# Membaca data
day_csv = 'analisis dengan python\datasets\day.csv'
day_df = pd.read_csv(day_csv)
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df.set_index('dteday', inplace=True)

# Membuat komponen filter rentang tanggal
min_date = day_df.index.min().date()
max_date = day_df.index.max().date()
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Memfilter DataFrame berdasarkan rentang tanggal
filtered_df = day_df[(day_df.index >= pd.to_datetime(start_date)) & 
                     (day_df.index <= pd.to_datetime(end_date))]

# Pilihan untuk menampilkan plot
plot_selection = st.sidebar.selectbox('Pilih Visualisasi', ['Pola Peminjaman Harian', 'Pengaruh Musim'])

# Tampilkan plot berdasarkan pilihan
if plot_selection == 'Pola Peminjaman Harian':
    fig = plot_daily_rentals(filtered_df)
    st.pyplot(fig)
elif plot_selection == 'Pengaruh Musim':
    fig = plot_seasonal_effect(filtered_df)
    st.pyplot(fig)
else:
    st.write("Silakan pilih visualisasi dari sidebar.")

st.caption('Copyright © fiyandamamuri')
