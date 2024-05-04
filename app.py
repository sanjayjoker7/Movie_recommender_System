import streamlit as st
import pickle

# Function to recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['id']
        recommended_movie = {
            'title': movies.iloc[i[0]]['title'],
            'genre': movies.iloc[i[0]]['genre'],
            'year': movies.iloc[i[0]]['year'],
            'overview': movies.iloc[i[0]]['overview']
        }
        recommended_movies.append(recommended_movie)
    return recommended_movies

# Main function to run the app
def main():
    st.title('Movie Recommender System')
    
    # Select a movie from the dropdown
    selected_movie = st.selectbox(
        "Select a movie",
        movie_list
    )

    # Button to trigger recommendation
    if st.button('Show Recommendations'):
        st.subheader('Recommended Movies')
        recommended_movies = recommend(selected_movie)
        for movie in recommended_movies:
            st.write(f"**{movie['title']}**")
            st.write(f"*Genre:* {movie['genre']}, *Year:* {movie['year']}")
            st.write(f"*Overview:* {movie['overview']}")
            st.write('---')  # Add a horizontal line between movies

# Load movie data and similarity matrix
movies = pickle.load(open('movies_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title'].values

# Run the app
if __name__ == '__main__':
    main()
