import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from tabulate import tabulate
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Title and introduction
st.title('🚲 Bike Sharing Dashboard')
st.markdown("""
### Proyek Analisis Data: Bike Sharing Dataset
- **Nama:** Aksal Abitahta Turipan
- **Email:** gothsaiko2@gmail.com
- **ID Dicoding:** A006YBF044
""")

# Add a sidebar
st.sidebar.title('Navigation')
pages = st.sidebar.radio('Pages:', [
                         'Introduction', 'Data Overview', 'Analysis Q1', 'Analysis Q2', 'Conclusion'])

# Function to load and process data


@st.cache_data  # Cache the data loading to improve performance
def load_data():
    # You'll need to update these paths to where your data files are stored
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")

    # Data cleaning (same as your original code)
    # Convert dateday to datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'], errors='coerce')
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], errors='coerce')

    # Rename Columns
    day_df.rename(columns={
        'yr': 'year',
        'mnth': 'month',
        'hum': 'humidity',
        'cnt': 'total_rentals'
    }, inplace=True)

    hour_df.rename(columns={
        'yr': 'year',
        'mnth': 'month',
        'hr': 'hour',
        'hum': 'humidity',
        'cnt': 'total_rentals'
    }, inplace=True)

    # Create Feature for analyzing trends
    day_df['day_of_week'] = day_df['dteday'].dt.day_name()
    hour_df['day_of_week'] = hour_df['dteday'].dt.day_name()

    day_df['month_name'] = day_df['dteday'].dt.month_name()
    hour_df['month_name'] = hour_df['dteday'].dt.month_name()

    # Convert year from 0/1 to 2011/2012
    day_df['year_actual'] = day_df['year'].apply(
        lambda x: 2011 if x == 0 else 2012)
    hour_df['year_actual'] = hour_df['year'].apply(
        lambda x: 2011 if x == 0 else 2012)

    # Convert normalized temperature to real Celsius
    day_df['temp_c'] = day_df['temp'] * 41
    hour_df['temp_c'] = hour_df['temp'] * 41

    # Create weekday column for hour_df
    hour_df['weekday'] = hour_df['day_of_week'].apply(
        lambda day: 1 if day in ['Monday', 'Tuesday',
                                 'Wednesday', 'Thursday', 'Friday'] else 0
    )

    return day_df, hour_df


# Load the data
try:
    day_df, hour_df = load_data()
    data_load_state = st.success('Data successfully loaded!')
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.error(
        "Make sure to place 'day.csv' and 'hour.csv' in the same directory as this app.")
    st.stop()

# INTRODUCTION PAGE
if pages == 'Introduction':
    st.header('Introduction')
    st.write(
        'Dashboard untuk explores bike sharing data untuk menjawab two key business questions.')

    st.markdown("""
    ### Business Questions
    1. Apakah peningkatan penggunaan sepeda di tahun 2012 murni karena faktor musiman (cuaca) atau juga didorong oleh kebijakan/infrastruktur?
    2. Bagaimana dampak cuaca ekstrem (misalnya, hujan lebat/suhu sangat rendah) terhadap perilaku pengguna casual vs. registered?
    """)

    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/00_2141_Bicycle-sharing_systems_-_Sweden.jpg/1024px-00_2141_Bicycle-sharing_systems_-_Sweden.jpg",
             caption="Bike Sharing System")

# DATA OVERVIEW PAGE
elif pages == 'Data Overview':
    st.header('Data Overview')

    tab1, tab2 = st.tabs(["Daily Data", "Hourly Data"])

    with tab1:
        st.subheader("Daily Data Sample")
        st.dataframe(day_df.head())

        st.subheader("Daily Data Statistics")
        st.dataframe(day_df.describe())

        col1, col2 = st.columns(2)

        with col1:
            # Daily rentals distribution
            fig = plt.figure(figsize=(10, 6))
            plt.hist(day_df['total_rentals'], bins=20, edgecolor='black')
            plt.title('Distribution of Daily Total Rentals')
            plt.xlabel('Number of Rentals')
            plt.ylabel('Frequency')
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            # Temperature vs rentals
            fig = plt.figure(figsize=(10, 6))
            plt.scatter(day_df['temp_c'], day_df['total_rentals'], alpha=0.6)
            plt.title('Daily Rentals vs. Temperature')
            plt.xlabel('Temperature (Celsius)')
            plt.ylabel('Total Rentals')
            plt.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)

    with tab2:
        st.subheader("Hourly Data Sample")
        st.dataframe(hour_df.head())

        st.subheader("Hourly Data Statistics")
        st.dataframe(hour_df.describe())

        # Hourly rentals distribution
        fig = plt.figure(figsize=(10, 6))
        plt.hist(hour_df['total_rentals'], bins=50, edgecolor='black')
        plt.title('Distribution of Hourly Total Rentals')
        plt.xlabel('Number of Rentals')
        plt.ylabel('Frequency')
        plt.tight_layout()
        st.pyplot(fig)

        # Hourly trends by weekday/weekend
        hourly_trends_weekday = hour_df[hour_df['weekday'] == 1].groupby('hour')[
            'total_rentals'].mean()
        hourly_trends_weekend = hour_df[hour_df['weekday'] == 0].groupby('hour')[
            'total_rentals'].mean()

        fig = plt.figure(figsize=(12, 6))
        hourly_trends_weekday.plot(
            kind='bar', color='skyblue', label='Weekday')
        hourly_trends_weekend.plot(
            kind='bar', color='coral', label='Weekend', alpha=0.7)
        plt.title('Average Hourly Rentals by Weekday/Weekend')
        plt.xlabel('Hour of Day')
        plt.ylabel('Average Number of Rentals')
        plt.legend()
        plt.tight_layout()
        st.pyplot(fig)

# ANALYSIS Q1 PAGE
elif pages == 'Analysis Q1':
    st.header('Question 1: Analisis dari Tahun ke Tahun')
    st.subheader(
        'Apakah peningkatan penggunaan sepeda di tahun 2012 murni karena faktor musiman (cuaca) atau juga didorong oleh kebijakan/infrastruktur?')

    # Monthly comparison by year
    monthly_comparison = day_df.groupby(['year_actual', 'month'])[
        'total_rentals'].mean().reset_index()

    # Using Plotly for interactive chart with custom colors
    fig = px.line(monthly_comparison, x='month', y='total_rentals', color='year_actual',
                  labels={
                      'month': 'Month', 'total_rentals': 'Average Daily Rentals', 'year_actual': 'Year'},
                  title='Average Monthly Rentals by Year',
                  markers=True,
                  color_discrete_map={2011: 'blue', 2012: 'orange'})  # Set explicit colors

    fig.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### Key Insights:
    - Garis warna orange (2012) konsisten lebih tinggi dibanding garis biru (2011) di setiap bulan. Ini menunjukkan adanya pertumbuhan dalam penggunaan layanan bike sharing selama periode tersebut.
    - Keduanya punya pola musiman yang mirip (naik menuju puncak di musim panas, turun saat mendekati musim dingin). Terdapat peak penyewaan di sekitar bulan Juni-September (musim panas) dan penurunan di bulan-bulan musim dingin (Desember-Februari). Pola ini terlihat pada kedua tahun, menunjukkan bahwa cuaca dan musim memiliki pengaruh yang signifikan terhadap perilaku penyewaan sepeda.
    - Selisih 2012 vs. 2011 cukup konstan di seluruh bulan. Artinya, selisih antara kedua garis cenderung tetap stabil dari bulan ke bulan. Ini bisa menjadi indikasi bahwa ada faktor lain selain musim yang berkontribusi terhadap pertumbuhan penyewaan, seperti peningkatan popularitas layanan, perluasan infrastruktur, atau program promosi.
    
    ### Conclusion:
    Selama tahun 2012, terlihat ada peningkatan yang konsisten di semua bulan, dan ini nunjukkin kalau faktor selain cuaca juga punya pengaruh besar dalam naiknya penggunaan sepeda. Bisa jadi ini efek dari kebijakan atau peraturan baru yang lebih mendukung, infrastruktur yang makin oke, atau makin banyak orang yang mulai kenal dan terbiasa sama program sewa sepeda.
    """)

# ANALYSIS Q2 PAGE
elif pages == 'Analysis Q2':
    st.header('Question 2: Analisis Dampak Cuaca')
    st.subheader(
        'Bagaimana dampak cuaca ekstrem (misalnya, hujan lebat/suhu sangat rendah) terhadap perilaku pengguna casual vs. registered?')

    # Create the weather impact analysis
    weather_groups = day_df.groupby('weathersit').agg({
        'casual': 'mean',
        'registered': 'mean'
    }).reset_index()

    # Add weather descriptions
    weather_desc = {
        1: "Clear/Few clouds",
        2: "Mist/Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow/Fog"
    }

    weather_groups['weather_desc'] = weather_groups['weathersit'].map(
        weather_desc)

    # Create plotly chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=weather_groups['weather_desc'],
        y=weather_groups['casual'],
        name='Casual Users',
        marker_color='royalblue'
    ))

    fig.add_trace(go.Bar(
        x=weather_groups['weather_desc'],
        y=weather_groups['registered'],
        name='Registered Users',
        marker_color='darkorange'
    ))

    fig.update_layout(
        title='Average Rentals by Weather Situation',
        xaxis_title='Weather Situation',
        yaxis_title='Average Rentals',
        barmode='group'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Additional analysis - percentage decrease
    if st.checkbox("Show percentage decrease from optimal conditions"):
        weather_groups['casual_pct_drop'] = (
            1 - weather_groups['casual'] / weather_groups['casual'].iloc[0]) * 100
        weather_groups['registered_pct_drop'] = (
            1 - weather_groups['registered'] / weather_groups['registered'].iloc[0]) * 100

        fig = px.bar(weather_groups, x='weather_desc', y=['casual_pct_drop', 'registered_pct_drop'],
                     barmode='group',
                     labels={
                         'value': 'Percentage Decrease (%)', 'variable': 'User Type', 'weather_desc': 'Weather Situation'},
                     title='Percentage Decrease in Rentals (Compared to Clear Weather)')

        fig.update_layout(yaxis_title='Percentage Decrease (%)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### Key Insights:
    - Registered users consistently rent more bikes than casual users, regardless of the weather. Ini terlihat dari bar berwarna orange (registered) yang selalu lebih tinggi daripada bar berwarna biru (casual) di semua kategori cuaca.
    - Clear weather (weathersit=1) leads to the highest number of rentals for both user types. Bar chart menunjukkan bahwa baik casual maupun registered users paling banyak menyewa sepeda saat cuaca cerah.
    - Adverse weather conditions (Mist/Cloudy, Light Snow/Rain) negatively impact bike rentals, especially for casual users. Saat cuaca memburuk (kategori 2 dan 3), jumlah rental turun untuk kedua jenis pengguna, tapi penurunannya lebih signifikan pada casual users. Bisa dilihat dengan klick checkbox di bawah untuk melihat presentase penurunan.
    
    ### Conclusion:
   Pengguna registered kelihatan lebih konsisten nyewa sepeda, bahkan saat cuaca lagi nggak bagus—artinya mereka emang udah jadi pelanggan setia. Di sisi lain, pengguna casual lebih milih ngurangin aktivitas pas cuaca buruk. Tapi begitu cuaca cerah, dua-duanya langsung naik drastis jumlah rentalnya, jadi jelas cuaca bagus bisa jadi faktor pendorong utama.
    """)

# CONCLUSION PAGE
elif pages == 'Conclusion':
    st.header('Conclusion')

    st.markdown("""
    ### Key Findings
    
    #### Growth in Usage
    Tahun 2012 nunjukkin lonjakan penggunaan sepeda di semua bulan dibanding 2011. Artinya, ada faktor lain kayak kebijakan baru, promo, atau ekspansi program yang bikin orang makin sering pakai sepeda—nggak cuma karena cuaca walaupun cuaca bisa jadi salah satu faktor utamanya.
    
    #### Weather Effects
    Cuaca cerah jelas paling ngaruh ke peningkatan rental, sedangkan cuaca buruk bikin angka rental turun, terutama dari pengguna casual..
    
    ### Business Implications
    
    #### Weather Mitigation Strategies
    Biar penggunaan tetap stabil walau cuaca jelek, ada beberapa strategi yang di bisa coba : 
    - Diskon Berbasis Cuaca: Misalnya, diskon buat pengguna yang sewa sepeda saat cuaca buruk.
    - Infrastruktur yang tertutup(misalnya, tempat parkir sepeda di dalam gedung) untuk melindungi sepeda dari cuaca buruk.
    - Aksesoris perlindungan cuaca (misalnya, pelindung hujan) untuk sepeda atau jas hujan.
    
    #### Sustaining Growth
    Karena rental makin naik di 2012, artinya pasarnya terus berkembang. Supaya tren ini lanjut, bisa didukung dengan:
    - Infrastruktur yang lebih luas (menambah stasiun)
    - Jalur sepeda yang aman
    - Melanjutkan kegiatan promosi dan kolaborasi dengan pemerintah lokal untuk bikin program yang lebih menarik.
    - Penawaran khusus untuk pengguna baru (misalnya, diskon untuk pendaftaran pertama kali).
    
    #### User Segment Targeting
    - **Registered Users**: Fokus ke layanan yang stabil dan bisa di andalkan buat kebutuhan harian (commuter)
    - **Casual Users**: Kasih promo pas cuaca bagus buat narik mereka jadi pengguna tetap. Misalnya, diskon buat sewa sepeda di weekend atau saat cuaca cerah.
    """)


st.markdown("""---""")
st.markdown("© 2025 Bike Sharing Dashboard | by Aksal Abitahta Turipan")
