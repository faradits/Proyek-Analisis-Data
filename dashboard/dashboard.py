import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Mengambil data dari sumber
day_df = pd.read_csv('https://raw.githubusercontent.com/faradits/Proyek-Analisis-Data/refs/heads/main/dataset/day.csv')

# Mengubah nilai numerik menjadi kategori yang lebih deskriptif
day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['yr'] = day_df['yr'].map({0: '2011', 1: '2012'})
day_df['mnth'] = day_df['mnth'].map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
day_df['weekday'] = day_df['weekday'].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
day_df['workingday'] = day_df['workingday'].map({0: 'Holiday', 1: 'Workingday'})
day_df['weathersit'] = day_df['weathersit'].map({1: 'Clear/Partly Cloudy', 2: 'Cloudy/Mist', 3: 'Light Rain/Light Snow', 4: 'Heavy Rain/Heavy Snow/Thunderstorm'})

# Mengubah kolom yang relevan menjadi tipe data category
day_df['season'] = day_df['season'].astype('category')
day_df['yr'] = day_df['yr'].astype('category')
day_df['mnth'] = day_df['mnth'].astype('category')
day_df['weekday'] = day_df['weekday'].astype('category')
day_df['workingday'] = day_df['workingday'].astype('category')
day_df['weathersit'] = day_df['weathersit'].astype('category')

# Menambahkan kolom total_user sebagai penjumlahan dari casual dan registered
day_df['total_user'] = day_df['casual'] + day_df['registered']

# Mengonversi kolom 'dteday' menjadi tipe datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Dashboard Streamlit
st.set_page_config(page_title="Bike Sharing Data Dashboard", layout="wide")  # Set page layout
st.title("🚴‍♂️ Bike Sharing Data Dashboard")

# Sidebar untuk filter
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Select Year", day_df['yr'].unique())
selected_season = st.sidebar.multiselect("Select Season", day_df['season'].unique(), default=day_df['season'].unique())
selected_weather = st.sidebar.multiselect("Select Weather", day_df['weathersit'].unique(), default=day_df['weathersit'].unique())

# Input rentang waktu menggunakan kalender
start_date = st.sidebar.date_input("Start Date", value=day_df['dteday'].min())
end_date = st.sidebar.date_input("End Date", value=day_df['dteday'].max())

# Filter data sesuai pilihan tahun, musim, cuaca, dan rentang waktu
filtered_data = day_df[(day_df['yr'] == selected_year) & 
                       (day_df['season'].isin(selected_season)) & 
                       (day_df['weathersit'].isin(selected_weather)) & 
                       (day_df['dteday'] >= pd.to_datetime(start_date)) & 
                       (day_df['dteday'] <= pd.to_datetime(end_date))]

st.header(f"Data Summary for Year: {selected_year}")
st.write(f"Displaying data for the following seasons: {', '.join(selected_season)} and weather conditions: {', '.join(selected_weather)}")
st.write(filtered_data.describe())

# Visualisasi total pengguna berdasarkan musim
st.subheader("Total Users by Season")
season_total = filtered_data.groupby('season')['total_user'].sum().reset_index()

fig, ax = plt.subplots()
sns.barplot(x='season', y='total_user', data=season_total, ax=ax, palette='viridis')
ax.set_xlabel('Season')
ax.set_ylabel('Total Users')
ax.set_title('Total Users by Season')
st.pyplot(fig)

# Visualisasi total pengguna berdasarkan cuaca
st.subheader("Total Users by Weather")
weather_total = filtered_data.groupby('weathersit')['total_user'].sum().reset_index()

fig, ax = plt.subplots()
sns.barplot(x='weathersit', y='total_user', data=weather_total, ax=ax, palette='coolwarm')
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Total Users')
ax.set_title('Total Users by Weather')
st.pyplot(fig)

# Visualisasi total pengguna kasual vs terdaftar
st.subheader("Casual vs Registered Users")
user_type_total = filtered_data[['casual', 'registered']].sum()

fig, ax = plt.subplots()
ax.pie(user_type_total, labels=['Casual', 'Registered'], autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# Menampilkan data mentah
st.subheader("Raw Data")
st.write(filtered_data)

# Menambahkan statistik tambahan
st.subheader("Statistics Summary")
st.write(f"Average Total Users: {filtered_data['total_user'].mean():.2f}")
st.write(f"Maximum Total Users: {filtered_data['total_user'].max()}")
st.write(f"Minimum Total Users: {filtered_data['total_user'].min()}")

# Histogram total pengguna
st.subheader("Distribution of Total Users")
fig, ax = plt.subplots()
sns.histplot(filtered_data['total_user'], bins=20, kde=True, ax=ax)
ax.set_xlabel('Total Users')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Total Users')
st.pyplot(fig)