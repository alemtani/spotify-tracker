import base64
import json
import requests
import time

class Player(object):
    def __init__(self, data, detailed=False):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.artists = data['artists']
        self.detailed = detailed

        if self.type == 'album':
            self.image = data['images'][0] if data['images'] else None
            self.release_year = int(data['release_date'][:4])
        else:
            self.duration_ms = data['duration_ms']
            self.album = Player(data['album'])
        
        if detailed:
            self.popularity = data['popularity']

            if self.type == 'album':
                self.album_type = data['album_type']
                self.total_tracks = data['total_tracks']
                self.genres = data['genres']

                # Will calculate these separately
                self.tracks = []
                self.duration_ms = 0
    
    def load_tracks(self, tracks):
        if self.type == 'track': # Do nothing in this case
            return
        
        album = {
            'id': self.id,
            'name': self.name,
            'type': 'album',
            'artists': self.artists,
            'images': [self.image] if self.image else None,
            'release_date': str(self.release_year),
        }
        
        for track in tracks:
            # Need to add current album data
            track['album'] = album
            self.tracks.append(Player(track))
            self.duration_ms += track['duration_ms']
    
    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'artists': self.artists
        })
    
    def toJSON(self):
        if not self.detailed:
            return {
                'id': self.id,
                'name': self.name,
                'artists': list(map(lambda artist: artist['name'], self.artists)),
                'image': self.image if self.type == 'album' else self.album.image,
                'release_date': self.release_year if self.type == 'album' else None,
                'album': self.album.name if self.type == 'track' else None,
                'duration': self.duration_ms if self.type == 'track' else None
            }

class SpotifyClient(object):
    def __init__(self, client_id, client_secret):
        self.sess = requests.Session()
        self.client_id = client_id
        self.client_secret = client_secret
        self.expires_in = time.time()
    
    def refresh_token(self):
        now = time.time()
        if now < self.expires_in:
            return
        
        # Source: https://www.youtube.com/watch?v=WAmEZBEeNmg

        # Get the base64 auth string
        auth_str = f'{self.client_id}:{self.client_secret}'
        auth_bytes = auth_str.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

        # Build the parameters for the request
        url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = { 'grant_type': 'client_credentials' }
        resp = self.sess.post(url, headers=headers, data=data)
        data = resp.json()
        self.access_token = data['access_token']
        self.expires_in = now + data['expires_in']
    
    def get_auth_header(self):
        self.refresh_token()
        return { 'Authorization': f'Bearer {self.access_token}' }
    
    def get_request(self, url):
        headers = self.get_auth_header()
        resp = self.sess.get(url, headers=headers)

        if resp.status_code != 200:
            raise ValueError(f'Request failed with status code {resp.status_code}')
        
        data = resp.json()
        return data
    
    def search_for_item(self, q, item, offset=0):
        url = f'https://api.spotify.com/v1/search?q={q}&type={item}&offset={offset}'
        data = self.get_request(url)
        data = data[f'{item}s']

        result = {
            'type': item,
            'items': []
        }

        for item in data['items']:
            result['items'].append(Player(item))

        return result
    
    def get_player_by_id(self, item, spotify_id):
        url = f'https://api.spotify.com/v1/{item}s/{spotify_id}'
        data = self.get_request(url)

        player = Player(data, detailed=True)

        if item == 'album':
            url = f'https://api.spotify.com/v1/albums/{spotify_id}/tracks'

            while True:
                data = self.get_request(url)
                player.load_tracks(data['items'])
                if not data['next']:
                    break
                url = data['next']

        return player

""" *** Test usage *** """
if __name__ == '__main__':
    CLIENT_ID = '7dc4ccd94bfc45c7946f8d937867df4b'
    CLIENT_SECRET = '061d96a2988f4726a2f84ee62690854c'

    client = SpotifyClient(CLIENT_ID, CLIENT_SECRET)

    """ Test search functions """
    
    # Search for track
    # result = client.search_for_item('blank space', item='track')
    # print(result)

    # Search for album
    # result = client.search_for_item('red', item='album')
    # print(result)

    """ Test detail functions """

    # Get track detail
    # result = client.get_player_by_id('track', '1p80LdxRV74UKvL8gnD7ky')
    # print(result)

    # Get album detail
    # result = client.get_player_by_id('album', '6kZ42qRrzov54LcAk4onW9')
    # print(result)
    # print(result.tracks)

    