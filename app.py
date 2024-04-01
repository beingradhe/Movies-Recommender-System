import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
  url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
      movie_id)
  data = requests.get(url)
  data = data.json()
  poster_path = data['poster_path']
  full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
  return full_path


def recommend(movie):
  index = movie[movie['title'] == movie_list].index[0]
  distances = sorted(list(enumerate(similarity[index])),
                     reverse=True,
                     key=lambda x: x[1])
  recommended_movies = []
  recommended_movie_posters = []
  for i in distances[1:6]:
    movie_id = movie.iloc[i[0]].movie_id
    recommended_movies.append((movie.iloc[i[0]].title))
    recommended_movie_posters.append(fetch_poster(movie_id))
  return recommended_movies, recommended_movie_posters


with open('movies_dict.pkl', 'rb') as file:
  movies_dict = pickle.load(file)

with open('similarity.pkl', 'rb') as file:
  similarity = pickle.load(file)

movie = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

movie_list = st.selectbox('Select your favorite movie', movie['title'].values)

if st.button('Recommend'):
  recommended_movies, recommended_movie_posters = recommend(movie)
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    st.text(recommended_movies[0])
    st.image(recommended_movie_posters[0])
  with col2:
    st.text(recommended_movies[1])
    st.image(recommended_movie_posters[1])
  with col3:
    st.text(recommended_movies[2])
    st.image(recommended_movie_posters[2])
  with col4:
    st.text(recommended_movies[3])
    st.image(recommended_movie_posters[3])
  with col5:
    st.text(recommended_movies[4])
    st.image(recommended_movie_posters[4])
