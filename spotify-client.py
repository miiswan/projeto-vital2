# arquivo de conexao e api
import spotipy # com ela nao sera necessario usar get e post, apenas o nome das funcoes
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

# minhas credenciais (necessarias para q o servidor identifique qm esta pedindo)
CLIENT_ID = "62ed88194fe2413fa8b3f278c08e7570"
CLIENT_SECRET = "87be1073a6aa42529bd7c265631ad4a8"

# objeto de autenticacao (a lib spotipy q criou)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

print("to consumindo a api porraaaa")
