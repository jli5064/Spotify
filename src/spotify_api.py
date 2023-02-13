import requests
import json

def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    data = {
    'grant_type': 'client_credentials',
    'client_id': "8ac5bd4f29854a4abb37648a5b7833d8",
    'client_secret': "c9f1281a0f774d97ae7d002139e53049",
    }
    auth_response = requests.post(auth_url, data=data)
    access_token = auth_response.json().get('access_token')
    ACCESS_TOKEN_LINE = "Bearer " + access_token
    return ACCESS_TOKEN_LINE

def get_artist_genres(access, artist_names):
    # Set up the API endpoint and headers
    endpoint = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": access
    }

    # Create an empty list to store the genres
    artist_genres = {}

    # Iterate over the list of artists
    for artist_name in artist_names:
        # Specify the search parameters
        params = {
            "q": artist_name,
            "type": "artist"
        }
        # print(params)
        # Send a GET request to the API endpoint
        response = requests.get(endpoint, headers=headers, params=params)
        print(response)
        # Parse the response as JSON
        data = json.loads(response.text)
        # Append the artist's genres to the list of genres
        result = data["artists"]["items"]
        if len(result) > 0:
            artist_genres[artist_name] = result[0]['genres']
    return artist_genres

def get_spotify_genres(access_token, artists):
    genres = get_artist_genres(access_token, artists)
    return genres
