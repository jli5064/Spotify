import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_artist_genres(artist_names):
    fp = 'data/spotify/temp'
    if os.path.isfile(fp):
        artist_dict = json.load(open(fp,"r"))
    else:
        artist_dict = {}

    client_id = '8ac5bd4f29854a4abb37648a5b7833d8'
    client_secret = 'c9f1281a0f774d97ae7d002139e53049'
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    for artist in artist_names:
        if artist not in artist_dict.values():
            result = sp.search(artist, type='artist')['artists']['items']
            if len(result) > 0:
                artist_dict[artist] = result[0]['genres']
        else:
            continue
    return artist_dict
