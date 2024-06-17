import streamlit as st
import pickle
import pandas as pd

# Load the data
df = pd.read_csv('top10K-TMDB-movies.csv')

movies = pickle.load(open('movies_list.pkl', 'rb'))
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #1c1c3c;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
    }
    .main {
        background-color: #1c1c3c;
        padding: 2rem;
    }
    h1 {
        color: #FFD700;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0.5em;
    }
    h2 {
        color: #FFC500;
        font-size: 2em;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    h3 {
        color: #EE82EE;
        font-size: 1.5em;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    p {
        color: #98FF0B;
        font-size: 1.2em;
        margin-bottom: 0.5em;
    }
    .recommendation {
        background: #2e2e4d;
        padding: 1em;
        margin: 1em 0;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(238, 130, 238, 0.2);
    }
    .stSelectbox {
        background-color: #333366;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #8F00FF; /* Change button color to vibrant yellow */
        color: #1c1c3c; /* Change text color to dark violet */
        border: none;
        padding: 0.5em 1em;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #D06EF8;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit header
st.markdown("<h1>Movie Recommender System</h1>", unsafe_allow_html=True)

# Dropdown for selecting a movie
selected_movie = st.selectbox("Select movie from dropdown or Type", movies_list)

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index
    if len(index) == 0:
        st.error("Selected movie not found in database.")
        return []

    index = index[0]
    try:     
        dis = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        recommend_movies = []
        for i in dis[1:6]:
            recommend_movies.append(movies.iloc[i[0]].title)
        return recommend_movies
    except KeyError as e:
        st.error(f"KeyError occurred: {e}")
        return []

# Button for getting recommendations
if st.button("Recommend"):
    recommended_movies = recommend(selected_movie)
    if recommended_movies:
        st.markdown("<h2>Recommended Movies</h2>", unsafe_allow_html=True)
        for i, movie in enumerate(recommended_movies, start=1):
            movie_info = df[df['title'] == movie].iloc[0]
            st.markdown(f"<div class='recommendation'>", unsafe_allow_html=True)
            st.markdown(f"<h3>{i}. {movie}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Release Date:</b> {movie_info['release_date']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Genre:</b> {movie_info['genre']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Overview:</b> {movie_info['overview']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
st.markdown("<h2>About This Project</h2>", unsafe_allow_html=True)
st.markdown("""
    <div style='background-color: #2e2e4d; padding: 1em; border-radius: 10px;'>
        <p>This Movie Recommender System is designed to help users find movies similar to their favorite ones. 
        It uses machine learning techniques to analyze the similarities between movies based on their genres and overviews.</p>
        <p><h3>Machine Learning:</h3> Machine learning is a branch of artificial intelligence (AI) that focuses on building systems 
        that can learn from and make decisions based on data. This project utilizes machine learning to compare movies and recommend 
        those that are most similar to a selected movie.</p>
        <p><h3>Cosine Similarity:</h3> Cosine similarity is a metric used to measure how similar two items are. It calculates the cosine of 
        the angle between two vectors in a multi-dimensional space. In this project, the movie overviews and genres are converted into vectors, 
        and cosine similarity is used to find movies that have similar content.</p>
    </div>
    """, unsafe_allow_html=True)

# uplodedfile = st.file_uploader("Upload a CSV file", type=["csv"])
# st.button("Submit")
# if uplodedfile is not None:
    # df = pd.read_csv(uplodedfile)
    # st.write(df)
    # st.write(df.columns)
    # st.write(df.dtypes)
    # st.write(df.describe())
# 