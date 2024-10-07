import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page layout and title config first
st.set_page_config(layout="wide")

# Set style for seaborn
sns.set(style='dark')

# Title of the page
st.title("Bike Sharing Dashboard - Weather Impact Analysis")

# Loading data
day_csv = 'https://raw.githubusercontent.com/royalrumble3/Data_Analisis_Bike_Sharing/main/datasets/day.csv'
day_df = pd.read_csv(day_csv)
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df.set_index('dteday', inplace=True)

# Sidebar for filter options
with st.sidebar:
    st.image("https://raw.githubusercontent.com/royalrumble3/Data_Analisis_Bike_Sharing/refs/heads/main/image/bike-svgrepo-com.svg")
    st.header("Filter:")

    # Date range filter
    min_date = day_df.index.min().date()
    max_date = day_df.index.max().date()
    start_date, end_date = st.date_input(
        label="Date Filter",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    st.header("Visit my Profile:")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/nikoriantcahyono/)")
    with col2:
        st.markdown("[![Github](https://img.icons8.com/glyph-neue/64/FFFFFF/github.png)](https://github.com/royalrumble3)")

# Filtering data based on date selection
filtered_df = day_df[(day_df.index >= pd.to_datetime(start_date)) & 
                     (day_df.index <= pd.to_datetime(end_date))]

# New section: Displaying total daily rentals
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_registered = filtered_df['registered'].sum()
    st.metric('Registered User', value=daily_rent_registered)

with col2:
    daily_rent_casual = filtered_df['casual'].sum()
    st.metric('Casual User', value=daily_rent_casual)

with col3:
    daily_rent_total = filtered_df['cnt'].sum()  # 'cnt' is the total rides count in the dataset
    st.metric('Total User', value=daily_rent_total)

st.markdown('---')  # A divider line


def plot_daily_rentals(day_df):
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted size
    ax.plot(day_df.index, day_df['registered'], label='Registered')
    ax.plot(day_df.index, day_df['casual'], label='Casual')
    ax.set_title('Daily Bike Rentals (Registered vs Casual)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Rentals')
    ax.legend()
    ax.tick_params(rotation=45)
    return fig

def plot_seasonal_effect(day_df):
    seasonal_data = day_df.groupby('season')['cnt'].mean()
    season_names = ['Spring', 'Summer', 'Fall', 'Winter']
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted size
    ax.bar(season_names, seasonal_data)
    ax.set_xlabel('Season')
    ax.set_ylabel('Average Daily Rentals')
    ax.set_title('Seasonal Effect on Bike Rentals')
    return fig

# Display plots directly in the main section
st.subheader("Daily Rental Pattern")
fig1 = plot_daily_rentals(filtered_df)
st.pyplot(fig1)

st.subheader("Seasonal Effect on Bike Rentals")
fig2 = plot_seasonal_effect(filtered_df)
st.pyplot(fig2)



# Menghitung jumlah pengguna saat holiday, workingday, dan weekday
total_holiday_users = day_df.loc[day_df['holiday'] == 1, 'cnt'].sum()
total_workingday_users = day_df.loc[day_df['workingday'] == 1, 'cnt'].sum()
total_weekday_users = day_df.loc[(day_df['holiday'] == 0) & (day_df['workingday'] == 0), 'cnt'].sum()

# Membuat DataFrame
data = {'Day Type': ['Holiday', 'Working Day', 'Weekday'],
        'Total Users': [total_holiday_users, total_workingday_users, total_weekday_users]}
day_type_df = pd.DataFrame(data)

# Menampilkan DataFrame in Streamlit
st.subheader("Total Users Based on Day Type")
st.dataframe(day_type_df)

# Plotting User Count by Day Type
st.subheader("Comparison of User Count by Day Type")
plt.figure(figsize=(8, 5))
sns.barplot(x='Day Type', y='Total Users', data=day_type_df, palette='Set2')
plt.xlabel("Day Type")
plt.ylabel("Total Users")
plt.title("User Count Comparison Based on Day Type")
st.pyplot(plt)

st.caption('Copyright © NikoRiant')