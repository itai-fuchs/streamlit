import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Set up page configuration
st.set_page_config(
    page_title="Cinema Dashboard",
    page_icon="🎬",
    layout="wide"
)

# Apply custom CSS styling for background and layout
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524985069026-dd778a71c7b4");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }

    .main {
        background-color: rgba(255, 255, 255, 0.85); 
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
    }

    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-right: 1px solid #ccc;
    }

    h1, h2, h3 {
        color: #222;
        font-family: "Segoe UI", sans-serif;
    }

    .dataframe {
        background-color: rgba(240, 240, 240, 0.9) !important;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 10px;
        color: #111;
    }
    
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown("<h1 style='text-align: center; color: red;'>Movie Dashboard</h1>", unsafe_allow_html=True)


# Load movie dataset
movies_data = pd.read_csv("movies.csv")

# Drop missing values
movies_data.dropna(inplace=True)

# Sidebar filters
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()
year_list = sorted(movies_data['year'].unique().tolist())

with st.sidebar:
    st.write("### Filter Options")
    new_score_rating = st.slider("Score Range:", 1.0, 10.0, (1.0, 2.0), step=0.1)
    new_genre_list = st.multiselect("Choose Genre:", genre_list)
    year = st.selectbox("Choose a Year", year_list)

# Filtering data according to user selections
score_info = movies_data['score'].between(*new_score_rating)
genre_year = (movies_data['genre'].isin(new_genre_list)) & (movies_data["year"] == year)

# Filtered table of movies by year and genre
st.divider()
st.markdown("<h4 style='color: red;'>Filtered Movies by Year and Genre</h4>", unsafe_allow_html=True)
dataframe_genre_year = movies_data[genre_year].groupby(['name', 'genre'])['year'].sum().reset_index()
st.dataframe(dataframe_genre_year, use_container_width=True)

# Line chart: Number of movies per genre (within score range)
st.divider()
st.markdown("<h4 style='color: red;'>Number of Movies by Genre (Filtered by Score)</h4>", unsafe_allow_html=True)
rating_count_year = movies_data[score_info].groupby('genre')['score'].count().reset_index()
figpx = px.line(rating_count_year, x='genre', y='score')
st.plotly_chart(figpx, use_container_width=True)

# Pie chart: Genre distribution
st.divider()
st.markdown(f"<h4 style='color: red;'>Genre Distribution in {year}</h4>", unsafe_allow_html=True)

# סינון לפי השנה שנבחרה
filtered_by_year = movies_data[movies_data['year'] == year]

# חישוב התפלגות ז'אנרים לפי השנה
genre_counts = filtered_by_year['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# יצירת תרשים עוגה
fig_genre_pie = px.pie(
    genre_counts,
    names='genre',
    values='count',
    title=f"Distribution of Genres in {year}",
    color_discrete_sequence=px.colors.sequential.RdBu
)

# הצגת התרשים
st.plotly_chart(fig_genre_pie, use_container_width=True)


# Bar chart: Average budget per year
st.divider()
st.markdown("<h4 style='color: red;'>Average Budget by Year</h4>", unsafe_allow_html=True)
avg_budget_year = movies_data.groupby('year')['budget'].mean().reset_index()
fig_budget_year = px.bar(avg_budget_year, x='year', y='budget',
                         labels={'year': 'Year', 'budget': 'Average Budget'},
                         title="Average Movie Budget by Year",
                         color='budget', color_continuous_scale='Blues')
st.plotly_chart(fig_budget_year, use_container_width=True)

# Bar chart: Distribution of scores (based on user selection)
st.divider()
st.markdown("<h4 style='color: red;'>Score Distribution (Based on Selection)</h4>", unsafe_allow_html=True)

filtered_movies = movies_data[
    (movies_data['score'].between(*new_score_rating)) &
    (movies_data['genre'].isin(new_genre_list)) &
    (movies_data['year'] == year)
]

if filtered_movies.empty:
    st.warning("No movies found matching the selected filters. Try adjusting the score range, year, or genre.")
else:
    score_distribution = (
        filtered_movies['score']
        .value_counts()
        .sort_index()
        .reset_index()
    )
    score_distribution.columns = ['score', 'count']

    fig_score_dist = px.bar(
        score_distribution,
        x='score',
        y='count',
        labels={'score': 'User Score', 'count': 'Number of Movies'},
        title=f"Score Distribution for Selected Genre(s) in {year}",
        color='count',
        color_continuous_scale='Plasma'
    )

    st.plotly_chart(fig_score_dist, use_container_width=True)
