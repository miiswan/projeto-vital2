# arquivo de conexao e api
import spotipy # com ela nao sera necessario usar get e post, apenas o nome das funcoes
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

# pegando as credenciais no .env
caminho_base = Path(__file__).resolve().parent
load_dotenv(dotenv_path=caminho_base / '.env') 

#credenciais  (necessarias para q o servidor identifique qm esta pedindo)
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID") 
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# objeto de autenticacao (a lib spotipy q criou)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

print("to consumindo a api porraaaa")
