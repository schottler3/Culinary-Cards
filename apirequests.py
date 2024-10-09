import requests
from os import environ as env

def recipe_search(ingredient):
    app_id = env.get('EDAMAM_ID')  # Replace with your Edamam API app ID
    app_key = env.get('EDAMAM_KEY')  # Replace with your Edamam API app key
    result = requests.get(
        'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredient, app_id, app_key)
    )
    data = result.json()
    return data['hits']