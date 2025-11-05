# responsavel por lidar com o spotify
import os # acessa as varoáveis do sistema
import spotipy # acessa a api do spotify
from spotipy.oauth2 import SpotifyOAuth # cuida do login com conta
from dotenv import load_dotenv # carrega o conteudo do .env

# carrega variveis do .env
load_dotenv()

def create_spotify_oauth():
   
    #cria e configura a autenticação OAuth do spotify
   
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"), #credenciais
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-read-private user-read-email user-top-read"
    )

def get_user_data(access_token):

    #usa o token de acesso para pegar dados do ususrio
   
    sp = spotipy.Spotify(auth=access_token)
    user_info = sp.current_user()
    return user_info

def get_user_top_artists(access_token, time_range, limit, offset):
    sp = spotipy.Spotify(auth=access_token)
    top_artists = sp.current_user_top_artists(limit=limit, offset=offset, time_range=time_range)

    return top_artists

def get_user_top_musics(access_token, time_range, limit, offset):
    sp = spotipy.Spotify(auth= access_token)
    top_tracks = sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)

    return top_tracks


