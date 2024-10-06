import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image

# Set style seaborn and figure aesthetics
sns.set(style='darkgrid')

# Load logo and display it in the sidebar
logo = Image.open('image/Logo.png')
st.sidebar.image(logo, use_column_width=True)

st.title('🚴 Bike Sharing Dashboard 🚴‍♀️')

# Fungsi untuk plot pola peminjaman sepeda
def plot_daily_rentals(day_df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(day_df.index, day_df['registered'], label='Registered', color='blue')
    ax.plot(day_df.index, day_df['casual'], label='Casual', color='green')
    ax.set_title('Pola Peminjaman Sepeda Terdaftar dan Tidak Terdaftar dari Waktu ke Waktu (Dataset Harian)', fontsize=16)
    ax.set_xlabel('Tanggal', fontsize=12)
    ax.set_ylabel('Jumlah', fontsize=12)
    ax.legend(loc='upper left', fontsize=10)
    ax.tick_params(axis='x', rotation=45)
    return fig

# Fungsi untuk plot pengaruh musim terhadap penggunaan sepeda
def plot_seasonal_effect(day_df):
    seasonal_data = day_df.groupby('season')['cnt'].mean()
    season_names = ['Spring', 'Summer', 'Fall', 'Winter']
    colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99']
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(season_names, seasonal_data, color=colors)
    ax.set_xlabel('Musim', fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Sewa Harian', fontsize=12)
    ax.set_title('Pengaruh Musim Terhadap Penggunaan Sepeda', fontsize=16)
    return fig

# Membaca data
day_csv = 'https://raw.githubusercontent.com/royalrumble3/Data_Analisis_Bike_Sharing/main/datasets/day.csv'
day_df = pd.read_csv(day_csv)
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df.set_index('dteday', inplace=True)

# Membuat komponen filter rentang tanggal
min_date = day_df.index.min().date()
max_date = day_df.index.max().date()
st.sidebar.title('Filter and Visualizations')

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Memfilter DataFrame berdasarkan rentang tanggal
filtered_df = day_df[(day_df.index >= pd.to_datetime(start_date)) & 
                     (day_df.index <= pd.to_datetime(end_date))]

# Sidebar pilihan untuk menampilkan plot
plot_selection = st.sidebar.radio('Pilih Visualisasi', ['Pola Peminjaman Harian', 'Pengaruh Musim'])

# Display each chart in its own section
st.markdown('### Visualisasi Data')

if plot_selection == 'Pola Peminjaman Harian':
    st.markdown('#### Pola Peminjaman Sepeda Harian')
    fig = plot_daily_rentals(filtered_df)
    st.pyplot(fig)
    st.markdown('---')
elif plot_selection == 'Pengaruh Musim':
    st.markdown('#### Pengaruh Musim Terhadap Penggunaan Sepeda')
    fig = plot_seasonal_effect(filtered_df)
    st.pyplot(fig)
    st.markdown('---')
else:
    st.write("Silakan pilih visualisasi dari sidebar.")

# Add a footer with copyright
st.caption('Copyright © Niko Riant 2024')
