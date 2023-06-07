from flask import Flask, request
from flask_cors import CORS
import json
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from os.path import join, dirname
import jwt
from oauthlib.oauth2 import WebApplicationClient
from google.oauth2 import id_token
from google.auth.transport import requests

# environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Database
cluster = MongoClient(os.getenv("MONGO_URI"))
db = cluster["languageApp"]
user = db["user"]
lesson = db["lesson"]
word = db["word"]

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL =  "https://accounts.google.com/.well-known/openid-configuration"

# app
app = Flask(__name__)
CORS(app)

'''
login auth and user creation
'''
@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        token = request.headers.get('Authorization').strip("\"") 
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo['email']
        user_info = { "email": idinfo['email'], "name": idinfo['name']}

        if user.find_one({"email": email}) is None:
            print ("New User Created")
            user.insert_one({"email": email, "lessons": []})

        return json.dumps(user_info)

@app.route('/lesson', methods=['GET', 'POST'])
def lesson():
    if request.method == 'GET':
        return json.dumps({'success':True})
    elif request.method == 'POST':
        return json.dumps({'success':True})


if __name__ == '__main__':
   app.run(debug=True)