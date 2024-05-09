import requests
import json
from functools import wraps


BASE_URL = "https://apis.travelrealindia.in"


class ApiKeyConfig:
    API_KEY = None

    @classmethod
    def set_api_key(cls, api_key):
        cls.API_KEY = api_key

def set_api_key(api_key):
    ApiKeyConfig.set_api_key(api_key)
    
def get_api_key():
    return ApiKeyConfig.API_KEY

def requires_api_key(func):
    @wraps(func)    # to preserve metadata of the original 'func'
    def wrapper(*args, **kwargs):
        if get_api_key():
            return func(*args, **kwargs)
        return {"error": "Please set api_key"}
    return wrapper


class Base:
    def __init__(self, var, code=None):
        self.code = code 
        self.var = var

    @requires_api_key
    def fetch(self) -> dict:
        if not self.code:
            return {"error": "CODE is required"}
        try:
            payload = {"api_key": get_api_key()}
            endpoint = f'{BASE_URL}/{self.var}/{self.code}/retrieve'
            response = requests.get(endpoint, json=payload).text
            return json.loads(response)
        except:
            return {"error": "Failed to connect to host"}


class City(Base):
    def __init__(self, code=None):
        var = 'cities'
        super().__init__(var, code) 
        

class StateUT(Base):
    def __init__(self, var, code=None):
        super().__init__(var, code)

    @requires_api_key
    def fetch_cities(self) -> dict:
        if not self.code:
            return {"error": "CODE is required"}
        try:
            payload = {"api_key": get_api_key()}
            response =  requests.get(f'{BASE_URL}/{self.var}/{self.code}/retrieve/all/cities', json=payload).text 
            print(response)
            return json.loads(response)
        except:
            return {"error": "Failed to connect to host"}
    

class State(StateUT):
    def __init__(self, code=None):
        var = 'states'
        super().__init__(var, code)


class UT(StateUT):
    def __init__(self, code=None):
        var = 'ut'
        super().__init__(var, code)