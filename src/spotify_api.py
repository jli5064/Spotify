import requests



def get_spotify_genres(*JSON IMPORTS):
    get_artist_genres(access, artist_names)



#HELPER FUNCTION FOR ABOVE
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

        # Send a GET request to the API endpoint
        response = requests.get(endpoint, headers=headers, params=params)

        # Parse the response as JSON
        data = json.loads(response.text)
        # Append the artist's genres to the list of genres
        result = data["artists"]["items"]
        if len(result) > 0:
            artist_genres[artist_name] = result[0]['genres']
    return artist_genres