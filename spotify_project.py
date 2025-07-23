# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 06:38:59 2025

@author: KIIT0001
"""

import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from PIL import Image

st.title("Spotify Data Analytics Dashboard")
logo = Image.open(r"C:\Users\KIIT0001\Desktop\Work")
st.image(logo, width=30)

st.set_page_config(
    page_title="Spotify Data Analytics Dashboard",
    page_icon=r"C:\Users\KIIT0001\Desktop\Work", 
)

#@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\KIIT0001\Desktop\TU Berlin\Work\high_popularity_spotify_data.csv")


# function call
df = load_data()

# Sidebar – Grouped filters
st.sidebar.title("🎛️ Interactive Filters")

# Group 1: General Data Filters
st.sidebar.subheader("🎧 Data Range Filters")
popularity_range = st.sidebar.slider(
    "Select Popularity Range:",
    int(df['track_popularity'].min()),
    int(df['track_popularity'].max()),
    (20, 80)
)

# Group 2: Genre Analysis
st.sidebar.subheader("🎼 Genre Analysis")
selected_genre = st.sidebar.selectbox(
    "Choose a Genre:",
    options=df['playlist_genre'].unique()
)

# Group 3: Artist Radar
st.sidebar.subheader("🎤 Artist Profile")
artist_list = df['track_artist'].dropna().unique()
selected_artist = st.sidebar.selectbox(
    "Select an Artist:",
    options=artist_list
)

# Group 4: Time Trends
st.sidebar.subheader("⏳ Time Series")
show_time_series = st.sidebar.checkbox("Show Time-Based Audio Features", value=True)

# Filtered Data based on popularity
filtered_df = df[df['track_popularity'].between(*popularity_range)]


# adding a pandas dataframe head with a title
# Section: Raw Data Sample + Key Metrics
st.header("📄 Sample of Filtered Data")

# Show filtered data
st.dataframe(
    filtered_df[['track_album_name', 'track_artist', 'track_popularity', 'danceability', 'playlist_genre']],
    use_container_width=True
)


# --- Section: Metrics ---
avg_danceability = filtered_df["danceability"].mean()
avg_energy = filtered_df["energy"].mean()
top_genre = filtered_df["playlist_genre"].mode()[0] if not filtered_df.empty else "N/A"
top_artist = filtered_df["track_artist"].mode().iloc[0] if not filtered_df.empty else "N/A"

st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Avg. Danceability", value=f"{avg_danceability:.2f}")
col2.metric(label="Avg. Energy", value=f"{avg_energy:.2f}")
col3.metric(label="Most Common Genre", value=top_genre)
col4.metric(label="🎙️ Top Artist", value=top_artist)


# ----------- Fig 1: Correlation Matrix -------------------
features = ['track_popularity', 'danceability', 'energy', 'tempo']
corr_matrix = df[features].corr().round(2)

fig1 = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale='viridis',
    zmin=-1, zmax=1,
    labels=dict(x="Feature", y="Feature", color="Correlation"),
    title="Correlation Matrix: Popularity vs Danceability, Energy, Tempo"
)
fig1.update_layout(width=800, height=600, margin=dict(l=50, r=50, t=80, b=50))
st.plotly_chart(fig1, use_container_width=True)

# ----------- Fig 2a: Average Popularity by Genre --------
genre_df = df[df['playlist_genre'] == selected_genre]
track_agg = genre_df.groupby('playlist_genre')[['track_popularity']].mean().reset_index()

fig2a = px.bar(track_agg, x='playlist_genre', y='track_popularity',
             title=f'Average Popularity for Genre: {selected_genre}',
             labels={'playlist_genre': 'Genre', 'track_popularity':'Popularity'},
             color_discrete_sequence=['#640D5F'],
             width=1000, height=500)
st.plotly_chart(fig2a, use_container_width=True)

# ----------- Fig 2b: Popularity Distribution ------------
fig2b = px.histogram(filtered_df, x='track_popularity', nbins=30,
             title='Distribution of Popularity Scores',
             labels={'track_popularity': 'Popularity Score'},
             width=800)
st.plotly_chart(fig2b)

# ----------- Fig 3: Popularity vs Danceability ----------
fig3 = px.scatter(filtered_df, x='danceability', y='track_popularity',
             title='Popularity vs Danceability')
fig3.update_layout(width=800, height=500)
st.plotly_chart(fig3, key="fig3_chart")

# ----------- Fig 4: Popularity vs Energy ----------------
fig4 = px.scatter(filtered_df, x='energy', y='track_popularity',
             title='Popularity vs Energy')
fig4.update_layout(width=800, height=500)
st.plotly_chart(fig4, key="fig4_chart")

# ----------- Fig 5: Popularity vs Tempo -----------------
fig5 = px.scatter(filtered_df, x='tempo', y='track_popularity',
             title='Popularity vs Tempo')
fig5.update_layout(width=800, height=500)
st.plotly_chart(fig5, key="fig5_chart")

# ----------- Fig 6: Radar Chart for Artist Features -----
radar_features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']
mean_features = df[df['track_artist'] == selected_artist][radar_features].mean().reset_index()
mean_features.columns = ['feature', 'value']

fig6 = px.line_polar(mean_features, r='value', theta='feature', line_close=True,
             title=f"Audio Feature Profile: {selected_artist}")
st.plotly_chart(fig6, key="fig6_chart")

# ----------- Fig 7: Time-Based Analysis ------------------
if show_time_series:
    df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], errors='coerce')
    df_sorted = df.sort_values('track_album_release_date')

    col1, col2 = st.columns(2)

    fig7a = px.line(df_sorted, x='track_album_release_date', y='acousticness',
                  title='Acousticness Over Time',
                  color_discrete_sequence=['#636EFA'])
    col1.plotly_chart(fig7a, key="fig7a_chart")

    fig7b = px.line(df_sorted, x='track_album_release_date', y='instrumentalness',
                   title='Instrumentalness Over Time',
                   color_discrete_sequence=['#EF553B'])
    col2.plotly_chart(fig7b, key="fig7b_chart")
