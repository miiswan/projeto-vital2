import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


class SpotifyService:
    def __init__(self):
        self.oauth = self._create_spotify_oauth()
        self.sp = None  # será configurado depois com o access_token

    def _create_spotify_oauth(self):
        # cria e configura a autenticação OAuth do spotify
        return SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="user-read-private user-read-email user-top-read"
        )

    def set_access_token(self, access_token: str):
        # instancia o cliente autenticado do Spotipy
        self.sp = spotipy.Spotify(auth=access_token)

    def get_user_data(self):
        if not self.sp:
            raise RuntimeError("Spotify client não inicializado. Chame set_access_token() antes.")
        return self.sp.current_user()

    def get_user_top_artists(self, time_range: str, limit: int, offset: int):
        if not self.sp:
            raise RuntimeError("Spotify client não inicializado. Chame set_access_token() antes.")
        return self.sp.current_user_top_artists(
            limit=limit,
            offset=offset,
            time_range=time_range
        )

    def get_user_top_musics(self, time_range: str, limit: int, offset: int):
        if not self.sp:
            raise RuntimeError("Spotify client não inicializado. Chame set_access_token() antes.")
        return self.sp.current_user_top_tracks(
            limit=limit,
            offset=offset,
            time_range=time_range
        )
    
    def get_playlist_tracks(self, playlist_id: str, limit: int =50, offset: int=0):
        if not self.sp:
            raise RuntimeError("Spotify client não inicializado. Chame set_access_token() antes.")
        return self.sp.playlist_items(playlist_id, limit=limit, offset=offset)

    @staticmethod
    def get_top_artist_by_genre(top_artists, top_genres):
        target_genres = [g[0].lower() for g in top_genres]
        artists_by_genre = {}
        seen_artist_ids = set()

        for artist in top_artists["items"]:
            artist_id = artist["id"]
            if artist_id in seen_artist_ids:
                continue

            for genre in artist["genres"]:
                if genre in target_genres and genre not in artists_by_genre:
                    artists_by_genre[genre] = artist
                    seen_artist_ids.add(artist_id)
                    break

            if len(artists_by_genre) == len(top_genres):
                break

        return artists_by_genre
    

