# arquivo de conexao e api
import spotipy # com ela nao sera necessario usar get e post, apenas o nome das funcoes
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

# minhas credenciais (necessarias para q o servidor identifique qm esta pedindo)
CLIENT_ID = "cred"
CLIENT_SECRET = "secret"

# objeto de autenticacao (a lib spotipy q criou)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

print("to consumindo a api porraaaa")
