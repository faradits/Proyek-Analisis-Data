import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
url = "https://raw.githubusercontent.com/faradits/Proyek-Analisis-Data/refs/heads/main/all_data.csv"
all_df = pd.read_csv(url)

# Dashboard Streamlit
st.set_page_config(page_title="Bike Sharing Data Dashboard")  # Set page layout
st.title("Bike Sharing Data Dashboard 🚴‍♂️")

# Sidebar untuk filter
st.sidebar.header("Filter Data")
# Filter berdasarkan tanggal
start_date = st.sidebar.date_input("Select Start Date", value=datetime(2011, 1, 1))
end_date = st.sidebar.date_input("Select End Date", value=datetime(2012, 12, 31))

# Filter berdasarkan musim dan hari kerja
all_seasons = all_df['season'].unique().tolist()
selected_season = st.sidebar.multiselect("Select Season", all_seasons, default=all_seasons)
all_workingdays = all_df['workingday'].unique().tolist()
selected_workingday = st.sidebar.multiselect("Select Working Day", all_workingdays, default=all_workingdays)

# Github link
st.sidebar.markdown("### Project Repository")
st.sidebar.write("[GitHub](https://github.com/faradits/Proyek-Analisis-Data)")

# Preprocess data
date_column = 'datetime' if 'datetime' in all_df.columns else 'date'
all_df[date_column] = pd.to_datetime(all_df[date_column])
all_df = all_df[(all_df[date_column] >= pd.to_datetime(start_date)) & (all_df[date_column] <= pd.to_datetime(end_date))]

# Filter data berdasarkan pilihan musim dan hari kerja/libur
if selected_season:
    filtered_data = all_df[all_df['season'].isin(selected_season)]
else:
    filtered_data = all_df[all_df['season'].isin([])]  # Jika tidak ada musim yang dipilih, hasilkan data kosong

if selected_workingday:
    filtered_data = filtered_data[filtered_data['workingday'].isin(selected_workingday)]
else:
    filtered_data = filtered_data[filtered_data['workingday'].isin([])]  # Jika tidak ada hari kerja yang dipilih, hasilkan data kosong

# 1. Visualisasi: Penyewaan sepeda selama jam sibuk pagi dan sore hari
st.subheader("1. Bike Rentals During Rush Hours")
st.markdown("This chart shows the number of bike rentals during the morning and evening rush hours.")

# Jika data setelah filter kosong, tampilkan pesan bahwa tidak ada data yang tersedia
if filtered_data.empty:
    st.warning("No data available for the selected filters.")
else:
    filtered_data['rush_hour'] = filtered_data['hour'].apply(
        lambda x: 'Morning (6:00 - 9:00)' if 6 <= x <= 9 else ('Evening (17:00 - 19:00)' if 17 <= x <= 19 else 'Other')
    )

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hour', y='total_user', hue='rush_hour', data=filtered_data, palette='Set2', ax=ax1)
    ax1.set_title('Comparison of Bike Rentals During Rush Hours', fontsize=16)
    ax1.set_xlabel('Hour of the Day', fontsize=12)
    ax1.set_ylabel('Total Bike Rentals', fontsize=12)
    ax1.set_xticks(range(0, 24))
    st.pyplot(fig1)

# 2. Line chart: Which season has the highest number of bike rentals?
st.subheader("2. Season with the Highest Number of Bike Rentals")
st.markdown("The line chart compares the average number of bike rentals in each season.")

# Jika data setelah filter kosong, tampilkan pesan
if filtered_data.empty:
    st.warning("No data available for the selected filters.")
else:
    season_df = filtered_data.groupby('season')['total_user'].mean().reset_index()

    plt.figure(figsize=(6, 4))
    sns.lineplot(x='season', y='total_user', data=season_df, marker='o', color='green')
    plt.title("Average Bike Rentals per Season", fontsize=16)
    plt.ylabel("Average Number of Rentals", fontsize=12)
    plt.xlabel("Season", fontsize=12)
    plt.grid(True)
    st.pyplot(plt)

# 3. Pie chart: Bike rentals on working days vs holidays
st.subheader("3. Bike Rentals on Working Days vs Holidays")
st.markdown("The pie chart shows the proportion of bike rentals on working days and holidays.")

# Jika data setelah filter kosong, tampilkan pesan
if filtered_data.empty:
    st.warning("No data available for the selected filters.")
else:
    day_type_df = filtered_data.groupby('workingday')['total_user'].mean().reset_index()

    # Jika hanya satu tipe hari (workingday atau holiday) yang dipilih, pie chart akan menunjukkan 100% untuk tipe tersebut
    if len(day_type_df) == 1:
        labels = ['Holiday'] if day_type_df['workingday'].values[0] == 0 else ['Working Day']
        sizes = [100]
    else:
        labels = ['Holiday', 'Working Day']
        sizes = day_type_df['total_user'].values

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#FF9999', '#66B2FF'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Bike Rentals on Working Days vs Holidays", fontsize=16)
    st.pyplot(fig)

# Kesimpulan
st.subheader("Conclusion")
st.markdown("""
- **Rush Hours**: From the analysis, it's clear that bike rentals significantly increase during the morning rush hours (6:00 - 9:00 AM) and evening rush hours (5:00 - 7:00 PM), particularly at 8:00 AM, 5:00 PM, and 6:00 PM. This suggests that many people use bikes as a primary mode of transportation for daily activities such as commuting to work, school, or shopping. On holidays, however, the peak rental time shifts to around 1:00 PM.
  
- **Seasonal Trend**: The analysis shows that **Fall** is the season with the highest number of bike rentals, followed by **Summer**. **Winter** sees fewer rentals, and **Spring** records the lowest number of rentals. This suggests that users prefer biking during warmer, more pleasant seasons.

- **Working Days vs Holidays**: 51.6% of bike rentals occur on working days, while 48.4% happen on holidays. This slight difference suggests that while bikes are primarily used for commuting during working days, they are also popular for leisure or errands during holidays. Interestingly, during the **Summer**, holiday rentals surpass working day rentals by 51%.
""")

# Copyright di bagian bawah halaman utama
st.markdown("""
---
© 2024 [Faradita Sabila](https://github.com/faradits)
""")