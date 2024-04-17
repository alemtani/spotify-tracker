import base64
import json
import requests
import threading
import time

class SpotifyClient(object):
    def __init__(self, client_id, client_secret):
        self.sess = requests.Session()
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token()
        # thread = threading.Thread(target=self.refresh_token)
        # thread.start()
    
    def refresh_token(self):
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
        data = {
            'grant_type': 'client_credentials'
        }

        # Update just once for now
        result = requests.post(url, headers=headers, data=data)
        result_data = json.loads(result.content)
        self.access_token = result_data['access_token']

        # STRETCH GOAL: Refresh token after the expiry period using a background task
        # while True:
        #     result = requests.post(url, headers=headers, data=data)
        #     result_data = json.loads(result.content)
        #     self.access_token = result_data['access_token']
        #     print(f"New access token (expires in {result_data['expires_in']}): {self.access_token}")
        #     time.sleep(result_data['expires_in'])

""" *** Test usage *** """
if __name__ == '__main__':
    CLIENT_ID = '7dc4ccd94bfc45c7946f8d937867df4b'
    CLIENT_SECRET = '061d96a2988f4726a2f84ee62690854c'

    client = SpotifyClient(CLIENT_ID, CLIENT_SECRET)