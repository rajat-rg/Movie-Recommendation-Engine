# from django.http.response import HttpResponse
from django.shortcuts import render
from recomm.models import movies_model
import pickle
import requests as req
# Create your views here.
movies = movies_model.objects.all()
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = req.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data= response.json()
    return "http://image.tmdb.org/t/p/w500"+data['poster_path']


def recommend(selected_movie):
    movie = movies_model.objects.all().filter(title = selected_movie)[0]
    movie_index = movie.id -1 
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse= True, key = lambda x: x[1])[1:6]
    poster = list()
    movie_recommended = list()
    for i in movie_list:
        x =movies_model.objects.get(id= i[0]+1)
        poster.append(x.movie_id)
        movie_recommended.append(x)
    return poster, movie_recommended 

def index(request):
    selected_movie=""
    recommended_movies = list()
    poster = list()
    inone = []
    recommended_movies_posters = list()
    if request.method== 'POST':
        selected_movie = request.POST.get('movie-select')
        poster, recommended_movies  = recommend(selected_movie)
    for i in poster:
        recommended_movies_posters.append(fetch_poster(i))
    for i in range(len(recommended_movies)):
        inone.append([recommended_movies[i], recommended_movies_posters[i]])
    context = {"movies": movies, "name": selected_movie, "recommended_list":inone}
    return render(request, 'index.html', context)
    # 8265bd1679663a7ea12ac168da84d2e8
    # API key