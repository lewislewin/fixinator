import requests

class RestEngine:

    def __init__(self, base_url) -> None:
        self.base_url = base_url
        self.headers = {}

    def setHeaders(self, headers):
        self.headers.update(headers)

    def setAuth(self, auth):
        self.headers.update({'Authorization': 'Token ' + auth})

    def get(self, url, params=None):
        return requests.get(self.base_url + url, params=params, headers=self.headers)
    
    def post(self, url, data=None):
        return requests.post(self.base_url + url, json=data, headers=self.headers)
    
    def patch(self, url, data=None):
        return requests.patch(self.base_url + url, json=data, headers=self.headers)