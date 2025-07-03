import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# import csv file.
movies_data = pd.read_csv("movies.csv")


# select the gener and the budget columns group by gener.
movies_data.dropna()
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']

# create a movies violation bar
fig = plt.figure(figsize = (19, 10))
plt.bar(genre, avg_bud, color = 'maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing the Average \
Budget of Movies in Each Genre')
# st.pyplot(fig)


score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()
year_list = movies_data['year'].unique().tolist()
with st.sidebar:
    st.write("### Select a range on the slider\
       to view the total number of movies in a genre that falls \
       within that range ")
    # create a slider to hold user scores
    new_score_rating = st.slider(label="# rating range:",
                                 min_value=1.0,
                                 max_value=10.0,
                                 value=(0.0, 0.0))

    # create a multiselect widget to display genre
    new_genre_list = st.multiselect('Choose Genre:',
                                    genre_list)
    # create a selectbox option that holds all unique years
    year = st.selectbox('Choose a Year',
                        year_list, 0)