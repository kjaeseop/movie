import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '5ad18f8eb8ecc4361611fb25886a1c9f'
tmdb.language = 'ko-KR'

def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0] #제목을 통해 index 값 얻기
    sim_scores = list(enumerate(cosine_sim[idx])) # cosine_sim에서 (idx, 유사도)형태로 얻기
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) #내림차순 정렬
    sim_scores = sim_scores[1:11] ## 자신을 제외한 10개의 추천 영화를 슬라이싱
    movie_indices = [i[0] for i in sim_scores] # 추천 10개의 인덱스 정보 추출
    # 인덱스 정보를 통해 영화 제목 추출
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id)
        image_path = details['poster_path']
        
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'

        images.append(image_path)
        titles.append(details['title'])

    return images, titles
    
movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout='wide')
st.header('JS_CINEMA')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)
if st.button('Recommend'):
    with st.spinner('Please wait...'):
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0, 2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1