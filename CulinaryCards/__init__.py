import os
import psycopg2
from datetime import *
from flask import Flask
from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search",methods=['POST'])
def redirectToSearch():
    return render_template("test.html")

if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        app.run(debug=True)
    else:
        app.run()