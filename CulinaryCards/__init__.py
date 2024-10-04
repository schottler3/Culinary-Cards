import os
import psycopg2
import requests
from datetime import *
from flask import Flask
from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search",methods=['POST'])
def redirectToSearch():
    user_query = request.form["queryhome"]
    api_url = f"https://api.edamam.com/search?q={user_query}&app_id={os.environ.get('EDAMAM_APP_ID')}&app_key={os.environ.get('EDAMAM_APP_KEY')}"
    
    api_response = requests.get(api_url)

    api_json = api_response.json()
    print(api_json)

    return render_template("test.html")

if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        app.run(debug=True)
    else:
        app.run()