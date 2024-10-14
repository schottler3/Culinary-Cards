import os
from os import environ as env
import requests

def getImgUrl(query):
    access_key = env.get("UNSPLASH_KEY")

    url = f"https://api.unsplash.com/photos/random?client_id={access_key}&query={query}"
    response = requests.get(url)

    if response.status_code == 200:
        jsonObject = response.json()
        img_url = jsonObject['urls']['regular']
        return img_url
    else:
        print("Couldn't find IMG, using default img")
        return "" #use default url



