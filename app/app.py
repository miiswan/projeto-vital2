# servidor flask
#importa o flask, e as funcoes do arquivo spotify_service
from os import access

from flask import Flask, redirect, url_for, request, session, render_template, jsonify
from spotify_service import SpotifyService 
import os
from collections import Counter
import random


# cria a aplicação flask
app = Flask(__name__)


app.secret_key = os.urandom(64)


spotify_service = SpotifyService()


 # as rotas @app.route sao enderecos do site
 # redirect serve pra redirecionar o navegador
 # request pega dados vindos da URL
# pagina inicial
@app.route('/')
def index():
    if 'user_data' in session:
        return redirect(url_for('user_profile'))
    return render_template('login.html') # carrega o html

# rota para fazer login no Spotify
@app.route('/login')
def login():
    auth_url = spotify_service.oauth.get_authorize_url()
    return redirect(auth_url)

# rota de callback — é pra onde o Spotify manda o usuário depois do login
@app.route('/callback')
def callback():
    # pega o código que o Spotify envia
    code = request.args.get('code')

    # troca o código pelo token de acesso
    token_info = spotify_service.oauth.get_access_token(code)

    session['token_info'] = token_info

    #configura o client atenticado
    spotify_service.set_access_token(token_info['access_token'])


    # pega os dados do usuário logado
    user_data = spotify_service.get_user_data()

    session['user_data'] = user_data
    
    # Retorna a página do usuário
    return redirect(url_for('user_profile'))

@app.route('/user')
def user_profile():
    genre_counts = Counter()
    user_data = session.get('user_data')
    token_info = session.get('token_info')

    if not user_data or not token_info:
        return redirect(url_for('index'))
    
    access_token = token_info['access_token']
    spotify_service.set_access_token(access_token)

    top5_tracks = spotify_service.get_user_top_musics(time_range='medium_term', limit=5, offset=0)

    top_artists = spotify_service.get_user_top_artists(time_range='medium_term', limit=5, offset=0)

    top_artists_to_format = spotify_service.get_user_top_artists(time_range='medium_term', limit=50, offset=0)


    # Analisando os dados dos 50 artistas mais escutados para saber os gêneros mais escutados
    for artist in top_artists_to_format['items']:
        for genre in artist['genres']:
            genre_counts[genre.capitalize()] += 1

    genres = genre_counts.most_common(5)
    genres_to_lower_case = []
    
    for genre in genres:
        genre_lower = genre[0].lower()
        genres_to_lower_case.append(genre_lower)

    #Buscando artista mais escutado de cada gênero
    most_listend_artist_by_genre = spotify_service.get_top_artist_by_genre(top_artists_to_format, genres)

    #Sorteando os linear-gradients para background do gênero
    #Soretando cor
    def draw_color_rgba(opacity=0.9):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'rgba({r}, {g}, {b}, {opacity})'
    #Sorteando gradientes
    def sort_linear_gradient():
        final_color = draw_color_rgba()
        return f'linear-gradient(0deg, rgba(0,0,0,0.6) 0%, {final_color} 100%)'
    #Sorteando as 5 cores
    def generate_gradients(size=5):
        gradients = []
        for i in range(size):
            gradient = sort_linear_gradient()
            gradients.append(gradient)
        return gradients
    
    #Coletando apenas os ids do top5 músicas mais escutadas
    top5_tracks_ids = []
    for track in top5_tracks['items']:
        url = track['external_urls']['spotify']
        idTrack = url.split('/')[-1]
        top5_tracks_ids.append(idTrack)

    #retornando a página user.html com os dados do usuário, dos artistas mais escutaso, gêneros mais escutados
    user_image = user_data['images'][0]['url'] if user_data.get('images') else url_for('static', filename='default_user.png')

    return render_template(
    'user.html',
        user=user_data,
        user_image=user_image,
        artists=top_artists,
        genres=genres_to_lower_case,
        musics=top5_tracks_ids,
        artist_by_genre=most_listend_artist_by_genre,
        genre_background_colors=generate_gradients()
)


@app.route("/top-genres")
def top_genres():
    token_info = session.get("token_info")

    if not token_info:
        return jsonify({"error": "Usuário não autenticado"}), 401

    access_token = token_info["access_token"]
    spotify_service.set_access_token(access_token)

    # pega 50 artistas mais escutados 
    top_artists = spotify_service.get_user_top_artists(
        time_range="medium_term",
        limit=50,
        offset=0
    )

    genre_counts = {}

    for artist in top_artists.get("items", []):
        for genre in artist.get("genres", []):
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    # ordena do maior pro menor
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

    # pega apenas top 10
    top10 = dict(sorted_genres[:10])

    return jsonify(top10)


BR_TOP50_ID = "3g3WzU7ST7QKj7dXjntT0t"

@app.route('/brasil')
def brasil():
    token_info = session.get('token_info')
    user_data = session.get('user_data')

    if not token_info or not user_data:
        return redirect(url_for('index'))
    

    access_token = token_info['access_token']
    spotify_service.set_access_token(access_token)

    session['user_data'] = user_data

    musics_id = []
    playlist = spotify_service.get_playlist_tracks(BR_TOP50_ID, limit=50)
    for item in playlist["items"]:
        musics_id.append(item["track"]["id"])


    return render_template('brasil.html', user=user_data, musics=musics_id)


GLOBAL_TOP50_ID = "2fJNE3A7q5M2htYItgNTbo"

@app.route('/global')
def Global():
    token_info = session.get('token_info')
    user_data = session.get('user_data')

    if not token_info or not user_data:
        return redirect(url_for('index'))
    

    access_token = token_info['access_token']
    spotify_service.set_access_token(access_token)

    session['user_data'] = user_data

    musics_id = []
    playlist = spotify_service.get_playlist_tracks(GLOBAL_TOP50_ID, limit=50)
    for item in playlist["items"]:
        musics_id.append(item["track"]["id"])

    return render_template('global.html', user=user_data, musics=musics_id)

@app.route('/logout')
def logout():
    session.clear() # Limpa todos os dados da sessão
    return redirect(url_for('index'))


# roda o servidor
if __name__ == '__main__':
    app.run(debug=True)
