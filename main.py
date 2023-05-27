import pandas as pd
import streamlit as st
import pickle
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies=[]
    for i in movie_list:
        movie_id=i[0]
        #fectch poster in api
        recommend_movies.append(movies.iloc[i[0]].title)

    return recommend_movies
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommedion')
selected_movie_name=st.selectbox('how would to connect?',movies['title'].values)
if st.button('Recommend'):
    recommendations=recommend(selected_movie_name)
    for i in recommendations:
       st.write(i)
