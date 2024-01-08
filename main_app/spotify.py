from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}

def search_for_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']

    if len(json_result) == 0:
        print('No artist with this name exists...')
        return None
    
    return json_result[0]
    

def get_songs_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_albums_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']

    albums = []
    for album_info in json_result:
        album = {
            'name': album_info['name'],
            'artist': album_info['artists'][0]['name'],
            'tracks': get_tracks_in_album(token, album_info['id'])
        }
        albums.append(album)

    return albums

def get_tracks_in_album(token, album_id):
    url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']

    tracks = []
    for track_info in json_result:
        tracks.append(track_info['name'])

    return tracks

def get_album_info(token, album_id):
    url = f'https://api.spotify.com/v1/albums/{album_id}'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    album_info = json.loads(result.content)

    # Extracting song names from the tracklist
    if 'tracks' in album_info and 'items' in album_info['tracks']:
        songs = [track['name'] for track in album_info['tracks']['items']]
        album_info['songs'] = songs

    return album_info

def get_related_artists(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['artists']
    return json_result

def search_for_track(token, track_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['tracks']['items']

    if not json_result:
        print(f'No tracks with the name "{track_name}" found...')
        return None
    
    track_info = json_result[0]
    track_info['album']['artists'] = get_albums_by_artist(token, track_info['album']['artists'][0]['id'])
    return track_info

def get_single_track(token, track_id):
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def search_for_album(token, album_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f"?q={album_name}&type=album&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['albums']['items']

    if not json_result:
        print(f'No albums with the name "{album_name}" found...')
        return None
    
    return json_result[0]  # Return the first album found


def get_spotify_data(search_query, search_type):
    token = get_token()

    if search_type == 'artist':
        result = search_for_artist(token, search_query)
        if result:
            artist_id = result['id']
            top_tracks = get_songs_by_artist(token, artist_id)
            albums = get_albums_by_artist(token, artist_id)
            related_artists = get_related_artists(token, artist_id)
            return {
                'top_tracks': top_tracks,
                'albums': albums,
                'related_artists': related_artists,
            }

    elif search_type == 'track':
        result = search_for_track(token, search_query)
        if result:
            track_id = result['id']
            track = get_single_track(token, track_id)
            return {'top_tracks': [track]}
    
    return None

token = get_token()
result = search_for_album(token, 'Country Grammar')

print(result)