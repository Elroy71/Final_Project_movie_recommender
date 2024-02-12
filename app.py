import streamlit as st 
import pickle
import requests
from pathlib import Path 
import streamlit as st 
from PIL import Image
#tambahkan nanti top 10 movie
# --- PATH SETTING --- 
current_dir = Path(__file__).parent if '__file__' in locals() else path.cwd()
# css_file = current_dir / 'styles' / 'style.css'
resume_file = current_dir / 'assets' / 'Proposal_tugas_akhir_sanbercode.pdf'
profile_pic = current_dir / 'assets' / 'profile-pic.jpeg'


# --- GENERAL SETTINGS ---
page_title = 'Final Project | Elia Roysandi M'
page_icon = ':wave:'
name = 'Elia Roysandi M'
description = '''
Sanbercampus final training project.
Application of machine learning to film recommendations
'''
email = 'eliaroysandimanurun@gmail.com'
social_media = {
    'YouTube': 'https://www.youtube.com/channel/UCXJAIKpMldpOrgRq0qiy5pA',
    'LinkedIn': 'https://www.linkedin.com/in/elia-roysandi-manurun-6bba93253/',
    'GitHub': 'https://github.com/Elroy71',
    'Instagram': 'https://www.instagram.com/eliaroysandi.m/'
}

st.set_page_config(page_title=page_title, page_icon=page_icon)



# --- LOAD CSS, PDF & PROFILE PIC --- 
# with open(css_file)as f:
#     st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
with open(resume_file,'rb') as pdf_file:
    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)


# -- HERO SECTION -- 
col1, col2 = st.columns(2, gap='small')
with col1:
    st.image(profile_pic, width=230)
with col2:
    st.title(name)
    st.write(description)
    st.download_button(
        label='📃Download Requirement',
        data=PDFbyte,
        file_name = resume_file.name,
        mime='application/octet-stream'
    )
    st.write('📨',email)


@st.cache_resource
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path


movies = joblib.load('movies_list.joblib')
similarity = joblib.load('similarity.joblib')
genre_similarity = joblib.load('genre_similarity.joblib')
movies_list = movies['title'].values
movies_description = movies['overview'].values
movies_vote_average = movies['vote_average'].values
movies_vote_count = movies['vote_count'].values
movies_release_date = movies['release_date'].values


st.header('tmdb Movie Recommendation System')

import streamlit.components.v1 as components

def banner():
    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

    imageUrls = [
        fetch_poster(1632),
        fetch_poster(299536),
        fetch_poster(17455),
        fetch_poster(2830),
        fetch_poster(429422),
        fetch_poster(9722),
        fetch_poster(13972),
        fetch_poster(240),
        fetch_poster(155),
        fetch_poster(598),
        fetch_poster(914),
        fetch_poster(255709),
        fetch_poster(572154)
        ]

    selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)
    if selectedImageUrl is not None:
        gambar= st.image(selectedImageUrl,width=250)

if __name__ == '__main__':
    banner()

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^-----------------------------Fungsi Utama-----------------------------^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
selectvalue = st.selectbox('Select movie from dropdown', movies_list)

@st.cache_data
def choice(judul):
    index = movies[movies['title']==judul].index[0]
    distance = sorted(list(enumerate(genre_similarity[index])),reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    recommend_movie_descripion =[]
    recommend_movie_vote_average =[]
    recommend_movie_vote_count =[]
    recommend_movie_release_date =[]
    akurasi = []
    
    for i in distance[2:12]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
        recommend_movie_descripion.append(movies.iloc[i[0]].overview)
        recommend_movie_vote_average.append(movies.iloc[i[0]].vote_average)
        recommend_movie_vote_count.append(movies.iloc[i[0]].vote_count)
        recommend_movie_release_date.append(movies.iloc[i[0]].release_date)
        akurasi.append({i[1]})
    return recommend_movie, recommend_poster,recommend_movie_descripion,recommend_movie_vote_average,recommend_movie_vote_count,recommend_movie_release_date,akurasi


@st.cache_data
def recommand(movie):
    index = movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    recommend_movie_descripion =[]
    recommend_movie_vote_average =[]
    recommend_movie_vote_count =[]
    recommend_movie_release_date =[]
    akurasi = []
    
    for i in distance[0:10]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
        recommend_movie_descripion.append(movies.iloc[i[0]].overview)
        recommend_movie_vote_average.append(movies.iloc[i[0]].vote_average)
        recommend_movie_vote_count.append(movies.iloc[i[0]].vote_count)
        recommend_movie_release_date.append(movies.iloc[i[0]].release_date)
        akurasi.append({i[1]})
    return recommend_movie, recommend_poster,recommend_movie_descripion,recommend_movie_vote_average,recommend_movie_vote_count,recommend_movie_release_date,akurasi


@st.cache_data
def genre_recommand(movie):
    index = movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(genre_similarity[index])),reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    recommend_movie_descripion =[]
    recommend_movie_vote_average =[]
    recommend_movie_vote_count =[]
    recommend_movie_release_date =[]
    akurasi = []
    
    for i in distance[2:12]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
        recommend_movie_descripion.append(movies.iloc[i[0]].overview)
        recommend_movie_vote_average.append(movies.iloc[i[0]].vote_average)
        recommend_movie_vote_count.append(movies.iloc[i[0]].vote_count)
        recommend_movie_release_date.append(movies.iloc[i[0]].release_date)
        akurasi.append({i[1]})
    return recommend_movie, recommend_poster,recommend_movie_descripion,recommend_movie_vote_average,recommend_movie_vote_count,recommend_movie_release_date,akurasi
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^-----------------------------Fungsi Utama-----------------------------^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# @st.cache_data(experimental_allow_widgets=True)
def search():
    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
    movie_name, movie_poster, movie_description, movie_vote_average, movie_vote_count, movie_release_date,akurasi = recommand(selectvalue)

    imageUrls = [
        movie_poster[0],
        movie_poster[1],
        movie_poster[2],
        movie_poster[3],
        movie_poster[4],
        movie_poster[5],
        movie_poster[6],
        movie_poster[7],
        movie_poster[8],
        movie_poster[9],
        ]

    selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)
    if selectedImageUrl is not None:
        col1, col2 = st.columns(2)

        with col2:
            if selectedImageUrl == imageUrls[0]:
                judul= st.subheader(movie_name[0])
                tanggal_release = st.markdown(f"{movie_release_date[0]} akurasi: {akurasi[0]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[0], 0))+ f"({float(round(movie_vote_average[0], 1))})"+ f" {movie_vote_count[0]:,} Voted")
                deskripsi = st.markdown(movie_description[0])
                

            elif selectedImageUrl == imageUrls[1]:
                judul= st.subheader(movie_name[1])
                tanggal_release = st.markdown(f"{movie_release_date[1]} akurasi: {akurasi[1]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[1], 0))+ f"({float(round(movie_vote_average[1], 1))})"+ f" {movie_vote_count[1]:,} Voted")
                deskripsi = st.markdown(movie_description[1])

            elif selectedImageUrl == imageUrls[2]:
                judul= st.subheader(movie_name[2])
                tanggal_release = st.markdown(f"{movie_release_date[2]} akurasi: {akurasi[2]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[2], 0))+ f"({float(round(movie_vote_average[2], 1))})"+ f" {movie_vote_count[2]:,} Voted")
                deskripsi = st.markdown(movie_description[2])

            elif selectedImageUrl == imageUrls[3]:
                judul= st.subheader(movie_name[3])
                tanggal_release = st.markdown(f"{movie_release_date[3]} akurasi: {akurasi[3]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[3], 0))+ f"({float(round(movie_vote_average[3], 1))})"+ f" {movie_vote_count[3]:,} Voted")
                deskripsi = st.markdown(movie_description[3])

            elif selectedImageUrl == imageUrls[4]:
                judul= st.subheader(movie_name[4])
                tanggal_release = st.markdown(f"{movie_release_date[4]} akurasi: {akurasi[4]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[4], 0))+ f"({float(round(movie_vote_average[4], 1))})"+ f" {movie_vote_count[4]:,} Voted")
                deskripsi = st.markdown(movie_description[4])

            elif selectedImageUrl == imageUrls[5]:
                judul= st.subheader(movie_name[5])
                tanggal_release = st.markdown(f"{movie_release_date[5]} akurasi: {akurasi[5]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[5], 0))+ f"({float(round(movie_vote_average[5], 1))})"+ f" {movie_vote_count[5]:,} Voted")
                deskripsi = st.markdown(movie_description[5])

            elif selectedImageUrl == imageUrls[6]:
                judul= st.subheader(movie_name[6])
                tanggal_release = st.markdown(f"{movie_release_date[6]} akurasi: {akurasi[6]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[6], 0))+ f"({float(round(movie_vote_average[6], 1))})"+ f" {movie_vote_count[6]:,} Voted")
                deskripsi = st.markdown(movie_description[6])

            elif selectedImageUrl == imageUrls[7]:
                judul= st.subheader(movie_name[7])
                tanggal_release = st.markdown(f"{movie_release_date[7]} akurasi: {akurasi[7]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[7], 0))+ f"({float(round(movie_vote_average[7], 1))})"+ f" {movie_vote_count[7]:,} Voted")
                deskripsi = st.markdown(movie_description[7])

            elif selectedImageUrl == imageUrls[8]:
                judul= st.subheader(movie_name[8])
                tanggal_release = st.markdown(f"{movie_release_date[8]} akurasi: {akurasi[8]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[8], 0))+ f"({float(round(movie_vote_average[8], 1))})"+ f" {movie_vote_count[8]:,} Voted")
                deskripsi = st.markdown(movie_description[8])

            elif selectedImageUrl == imageUrls[9]:
                judul= st.subheader(movie_name[9])
                tanggal_release = st.markdown(f"{movie_release_date[9]} akurasi: {akurasi[9]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[9], 0))+ f"({float(round(movie_vote_average[9], 1))})"+ f" {movie_vote_count[9]:,} Voted")
                deskripsi = st.markdown(movie_description[9])

        with col1:
            gambar= st.image(selectedImageUrl, width=250)
            if st.button('Bersihkan...', key=f'hapus_button_{judul}'):
                gambar.empty()
                judul.empty()
                tanggal_release.empty()
                rating_bintang.empty()
                deskripsi.empty()
            

def genre_search_recommand():
    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
    movie_name, movie_poster, movie_description, movie_vote_average, movie_vote_count, movie_release_date,akurasi = genre_recommand(selectvalue)

    imageUrls = [
        movie_poster[0],
        movie_poster[1],
        movie_poster[2],
        movie_poster[3],
        movie_poster[4],
        movie_poster[5],
        movie_poster[6],
        movie_poster[7],
        movie_poster[8],
        movie_poster[9],
        ]

    selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)
    if selectedImageUrl is not None:
        col1, col2 = st.columns(2)

        with col2:
            if selectedImageUrl == imageUrls[0]:
                judul= st.subheader(movie_name[0])
                tanggal_release = st.markdown(f"{movie_release_date[0]} akurasi: {akurasi[0]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[0], 0))+ f"({float(round(movie_vote_average[0], 1))})"+ f" {movie_vote_count[0]:,} Voted")
                deskripsi = st.markdown(movie_description[0])
                

            elif selectedImageUrl == imageUrls[1]:
                judul= st.subheader(movie_name[1])
                tanggal_release = st.markdown(f"{movie_release_date[1]} akurasi: {akurasi[1]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[1], 0))+ f"({float(round(movie_vote_average[1], 1))})"+ f" {movie_vote_count[1]:,} Voted")
                deskripsi = st.markdown(movie_description[1])

            elif selectedImageUrl == imageUrls[2]:
                judul= st.subheader(movie_name[2])
                tanggal_release = st.markdown(f"{movie_release_date[2]} akurasi: {akurasi[2]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[2], 0))+ f"({float(round(movie_vote_average[2], 1))})"+ f" {movie_vote_count[2]:,} Voted")
                deskripsi = st.markdown(movie_description[2])

            elif selectedImageUrl == imageUrls[3]:
                judul= st.subheader(movie_name[3])
                tanggal_release = st.markdown(f"{movie_release_date[3]} akurasi: {akurasi[3]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[3], 0))+ f"({float(round(movie_vote_average[3], 1))})"+ f" {movie_vote_count[3]:,} Voted")
                deskripsi = st.markdown(movie_description[3])

            elif selectedImageUrl == imageUrls[4]:
                judul= st.subheader(movie_name[4])
                tanggal_release = st.markdown(f"{movie_release_date[4]} akurasi: {akurasi[4]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[4], 0))+ f"({float(round(movie_vote_average[4], 1))})"+ f" {movie_vote_count[4]:,} Voted")
                deskripsi = st.markdown(movie_description[4])

            elif selectedImageUrl == imageUrls[5]:
                judul= st.subheader(movie_name[5])
                tanggal_release = st.markdown(f"{movie_release_date[5]} akurasi: {akurasi[5]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[5], 0))+ f"({float(round(movie_vote_average[5], 1))})"+ f" {movie_vote_count[5]:,} Voted")
                deskripsi = st.markdown(movie_description[5])

            elif selectedImageUrl == imageUrls[6]:
                judul= st.subheader(movie_name[6])
                tanggal_release = st.markdown(f"{movie_release_date[6]} akurasi: {akurasi[6]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[6], 0))+ f"({float(round(movie_vote_average[6], 1))})"+ f" {movie_vote_count[6]:,} Voted")
                deskripsi = st.markdown(movie_description[6])

            elif selectedImageUrl == imageUrls[7]:
                judul= st.subheader(movie_name[7])
                tanggal_release = st.markdown(f"{movie_release_date[7]} akurasi: {akurasi[7]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[7], 0))+ f"({float(round(movie_vote_average[7], 1))})"+ f" {movie_vote_count[7]:,} Voted")
                deskripsi = st.markdown(movie_description[7])

            elif selectedImageUrl == imageUrls[8]:
                judul= st.subheader(movie_name[8])
                tanggal_release = st.markdown(f"{movie_release_date[8]} akurasi: {akurasi[8]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[8], 0))+ f"({float(round(movie_vote_average[8], 1))})"+ f" {movie_vote_count[8]:,} Voted")
                deskripsi = st.markdown(movie_description[8])

            elif selectedImageUrl == imageUrls[9]:
                judul= st.subheader(movie_name[9])
                tanggal_release = st.markdown(f"{movie_release_date[9]} akurasi: {akurasi[9]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[9], 0))+ f"({float(round(movie_vote_average[9], 1))})"+ f" {movie_vote_count[9]:,} Voted")
                deskripsi = st.markdown(movie_description[9])

        with col1:
            gambar= st.image(selectedImageUrl, width=250)
            if st.button('Bersihkan...', key=f'hapus_button_{judul}'):
                gambar.empty()
                judul.empty()
                tanggal_release.empty()
                rating_bintang.empty()
                deskripsi.empty()



def anime():
    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
    movie_name, movie_poster, movie_description, movie_vote_average, movie_vote_count, movie_release_date,akurasi = choice('Dragon Ball Z: Bio-Broly')

    imageUrls = [
        movie_poster[0],
        movie_poster[1],
        movie_poster[2],
        movie_poster[3],
        movie_poster[4],
        movie_poster[5],
        movie_poster[6],
        movie_poster[7],
        movie_poster[8],
        movie_poster[9],
        ]

    selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=205)
    if selectedImageUrl is not None:
        col1, col2 = st.columns(2)

        with col2:
            if selectedImageUrl == imageUrls[0]:
                judul= st.subheader(movie_name[0])
                tanggal_release = st.markdown(f"{movie_release_date[0]} akurasi: {akurasi[0]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[0], 0))+ f"({float(round(movie_vote_average[0], 1))})"+ f" {movie_vote_count[0]:,} Voted")
                deskripsi = st.markdown(movie_description[0])
                

            elif selectedImageUrl == imageUrls[1]:
                judul= st.subheader(movie_name[1])
                tanggal_release = st.markdown(f"{movie_release_date[1]} akurasi: {akurasi[1]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[1], 0))+ f"({float(round(movie_vote_average[1], 1))})"+ f" {movie_vote_count[1]:,} Voted")
                deskripsi = st.markdown(movie_description[1])

            elif selectedImageUrl == imageUrls[2]:
                judul= st.subheader(movie_name[2])
                tanggal_release = st.markdown(f"{movie_release_date[2]} akurasi: {akurasi[2]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[2], 0))+ f"({float(round(movie_vote_average[2], 1))})"+ f" {movie_vote_count[2]:,} Voted")
                deskripsi = st.markdown(movie_description[2])

            elif selectedImageUrl == imageUrls[3]:
                judul= st.subheader(movie_name[3])
                tanggal_release = st.markdown(f"{movie_release_date[3]} akurasi: {akurasi[3]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[3], 0))+ f"({float(round(movie_vote_average[3], 1))})"+ f" {movie_vote_count[3]:,} Voted")
                deskripsi = st.markdown(movie_description[3])

            elif selectedImageUrl == imageUrls[4]:
                judul= st.subheader(movie_name[4])
                tanggal_release = st.markdown(f"{movie_release_date[4]} akurasi: {akurasi[4]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[4], 0))+ f"({float(round(movie_vote_average[4], 1))})"+ f" {movie_vote_count[4]:,} Voted")
                deskripsi = st.markdown(movie_description[4])

            elif selectedImageUrl == imageUrls[5]:
                judul= st.subheader(movie_name[5])
                tanggal_release = st.markdown(f"{movie_release_date[5]} akurasi: {akurasi[5]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[5], 0))+ f"({float(round(movie_vote_average[5], 1))})"+ f" {movie_vote_count[5]:,} Voted")
                deskripsi = st.markdown(movie_description[5])

            elif selectedImageUrl == imageUrls[6]:
                judul= st.subheader(movie_name[6])
                tanggal_release = st.markdown(f"{movie_release_date[6]} akurasi: {akurasi[6]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[6], 0))+ f"({float(round(movie_vote_average[6], 1))})"+ f" {movie_vote_count[6]:,} Voted")
                deskripsi = st.markdown(movie_description[6])

            elif selectedImageUrl == imageUrls[7]:
                judul= st.subheader(movie_name[7])
                tanggal_release = st.markdown(f"{movie_release_date[7]} akurasi: {akurasi[7]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[7], 0))+ f"({float(round(movie_vote_average[7], 1))})"+ f" {movie_vote_count[7]:,} Voted")
                deskripsi = st.markdown(movie_description[7])

            elif selectedImageUrl == imageUrls[8]:
                judul= st.subheader(movie_name[8])
                tanggal_release = st.markdown(f"{movie_release_date[8]} akurasi: {akurasi[8]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[8], 0))+ f"({float(round(movie_vote_average[8], 1))})"+ f" {movie_vote_count[8]:,} Voted")
                deskripsi = st.markdown(movie_description[8])

            elif selectedImageUrl == imageUrls[9]:
                judul= st.subheader(movie_name[9])
                tanggal_release = st.markdown(f"{movie_release_date[9]} akurasi: {akurasi[9]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[9], 0))+ f"({float(round(movie_vote_average[9], 1))})"+ f" {movie_vote_count[9]:,} Voted")
                deskripsi = st.markdown(movie_description[9])

        with col1:
            gambar= st.image(selectedImageUrl, width=250)
            if st.button('Bersihkan...', key=f'hapus_button_{judul}'):
                gambar.empty()
                judul.empty()
                tanggal_release.empty()
                rating_bintang.empty()
                deskripsi.empty()


def special_christmas():
    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
    movie_name, movie_poster, movie_description, movie_vote_average, movie_vote_count, movie_release_date,akurasi = recommand('Christmas Holidays')

    imageUrls = [
        movie_poster[0],
        movie_poster[1],
        movie_poster[2],
        movie_poster[3],
        movie_poster[4],
        movie_poster[5],
        movie_poster[6],
        movie_poster[7],
        movie_poster[8],
        movie_poster[9],
        ]

    selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=205)
    if selectedImageUrl is not None:
        col1, col2 = st.columns(2)

        with col2:
            if selectedImageUrl == imageUrls[0]:
                judul= st.subheader(movie_name[0])
                tanggal_release = st.markdown(f"{movie_release_date[0]} akurasi: {akurasi[0]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[0], 0))+ f"({float(round(movie_vote_average[0], 1))})"+ f" {movie_vote_count[0]:,} Voted")
                deskripsi = st.markdown(movie_description[0])
                

            elif selectedImageUrl == imageUrls[1]:
                judul= st.subheader(movie_name[1])
                tanggal_release = st.markdown(f"{movie_release_date[1]} akurasi: {akurasi[1]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[1], 0))+ f"({float(round(movie_vote_average[1], 1))})"+ f" {movie_vote_count[1]:,} Voted")
                deskripsi = st.markdown(movie_description[1])

            elif selectedImageUrl == imageUrls[2]:
                judul= st.subheader(movie_name[2])
                tanggal_release = st.markdown(f"{movie_release_date[2]} akurasi: {akurasi[2]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[2], 0))+ f"({float(round(movie_vote_average[2], 1))})"+ f" {movie_vote_count[2]:,} Voted")
                deskripsi = st.markdown(movie_description[2])

            elif selectedImageUrl == imageUrls[3]:
                judul= st.subheader(movie_name[3])
                tanggal_release = st.markdown(f"{movie_release_date[3]} akurasi: {akurasi[3]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[3], 0))+ f"({float(round(movie_vote_average[3], 1))})"+ f" {movie_vote_count[3]:,} Voted")
                deskripsi = st.markdown(movie_description[3])

            elif selectedImageUrl == imageUrls[4]:
                judul= st.subheader(movie_name[4])
                tanggal_release = st.markdown(f"{movie_release_date[4]} akurasi: {akurasi[4]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[4], 0))+ f"({float(round(movie_vote_average[4], 1))})"+ f" {movie_vote_count[4]:,} Voted")
                deskripsi = st.markdown(movie_description[4])

            elif selectedImageUrl == imageUrls[5]:
                judul= st.subheader(movie_name[5])
                tanggal_release = st.markdown(f"{movie_release_date[5]} akurasi: {akurasi[5]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[5], 0))+ f"({float(round(movie_vote_average[5], 1))})"+ f" {movie_vote_count[5]:,} Voted")
                deskripsi = st.markdown(movie_description[5])

            elif selectedImageUrl == imageUrls[6]:
                judul= st.subheader(movie_name[6])
                tanggal_release = st.markdown(f"{movie_release_date[6]} akurasi: {akurasi[6]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[6], 0))+ f"({float(round(movie_vote_average[6], 1))})"+ f" {movie_vote_count[6]:,} Voted")
                deskripsi = st.markdown(movie_description[6])

            elif selectedImageUrl == imageUrls[7]:
                judul= st.subheader(movie_name[7])
                tanggal_release = st.markdown(f"{movie_release_date[7]} akurasi: {akurasi[7]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[7], 0))+ f"({float(round(movie_vote_average[7], 1))})"+ f" {movie_vote_count[7]:,} Voted")
                deskripsi = st.markdown(movie_description[7])

            elif selectedImageUrl == imageUrls[8]:
                judul= st.subheader(movie_name[8])
                tanggal_release = st.markdown(f"{movie_release_date[8]} akurasi: {akurasi[8]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[8], 0))+ f"({float(round(movie_vote_average[8], 1))})"+ f" {movie_vote_count[8]:,} Voted")
                deskripsi = st.markdown(movie_description[8])

            elif selectedImageUrl == imageUrls[9]:
                judul= st.subheader(movie_name[9])
                tanggal_release = st.markdown(f"{movie_release_date[9]} akurasi: {akurasi[9]}")
                rating_bintang = st.markdown(':star:'* int(round(movie_vote_average[9], 0))+ f"({float(round(movie_vote_average[9], 1))})"+ f" {movie_vote_count[9]:,} Voted")
                deskripsi = st.markdown(movie_description[9])

        with col1:
            gambar= st.image(selectedImageUrl, width=250)
            if st.button('Bersihkan...', key=f'hapus_button_{judul}'):
                gambar.empty()
                judul.empty()
                tanggal_release.empty()
                rating_bintang.empty()
                deskripsi.empty()

if __name__ == '__main__':
    st.subheader(f'Result search of \'{selectvalue}\'')
    search()
    st.markdown('## ')
    st.write(f"#### Because you search '{selectvalue}'")
    genre_search_recommand()
    st.markdown('## ')
    st.write("#### Action animation Movie")
    anime()
    st.markdown('## ')
    st.write("#### Special For Christmas Movie")
    special_christmas()




