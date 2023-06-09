from flask import Flask, request
from flask_cors import CORS
from os.path import join, dirname
from dotenv import load_dotenv
import os

import json
from pymongo import MongoClient
from google.oauth2 import id_token
from google.auth.transport import requests
import deepl
import re
from  string import punctuation
from bson import json_util, ObjectId

# EC2 setup
'''

import boto3
from botocore.exceptions import ClientError

# AWS Secrets Manager
def get_secret():

    secret_name = "languageAppSecrets"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secrets = get_secret_value_response['SecretString']
    return secrets


# Environment Variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Secrets
secrets = json.loads(get_secret())

# Database
# cluster = MongoClient(os.getenv("MONGO_URI"))
cluster = MongoClient(secrets['MONGO_URI'])
db = cluster["languageApp"]
user_collection = db["user"]
lesson_collection = db["lesson"]
word_collection = db["word"]
sentence_collection = db["sentence"]

# Google Client Configuration
# GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
# GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL =  "https://accounts.google.com/.well-known/openid-configuration"

GOOGLE_CLIENT_ID = secrets['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = secrets['GOOGLE_CLIENT_SECRET']


# DeepL Translation API
# DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_KEY = secrets['DEEPL_API_KEY']
translator = deepl.Translator(DEEPL_API_KEY)

# result = translator.translate_text("Hello, world!", target_lang="FR")
# print(result.text)  # "Bonjour, le monde !"

'''

# local setup
'''

# Environment Variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Database
cluster = MongoClient(os.getenv("MONGO_URI"))
db = cluster["languageApp"]
user_collection = db["user"]
lesson_collection = db["lesson"]
word_collection = db["word"]
sentence_collection = db["sentence"]

# Google Client Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL =  "https://accounts.google.com/.well-known/openid-configuration"



# DeepL Translation API
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(DEEPL_API_KEY)

# result = translator.translate_text("Hello, world!", target_lang="FR")
# print(result.text)  # "Bonjour, le monde !"

'''




# Environment Variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Database
cluster = MongoClient(os.getenv("MONGO_URI"))
db = cluster["languageApp"]
user_collection = db["user"]
lesson_collection = db["lesson"]
word_collection = db["word"]
sentence_collection = db["sentence"]

# Google Client Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL =  "https://accounts.google.com/.well-known/openid-configuration"



# DeepL Translation API
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(DEEPL_API_KEY)

# result = translator.translate_text("Hello, world!", target_lang="FR")
# print(result.text)  # "Bonjour, le monde !"

# App
app = Flask(__name__)
CORS(app)

# Routes
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

        # create user if not exist
        if user_collection.find_one({"email": email}) is None:
            # print ("New User Created")
            user_collection.insert_one({"email": email, "lessons": []})

        return json.dumps(user_info)
    
'''
post:
    posts a new lesson to lesson collection, and links the lesson to the user

get:
    gets all lessons from lesson collection for the user.

delete:
    deletes a lesson from lesson collection, and removes the lesson from the user
'''
@app.route('/lesson', methods=['GET', 'POST'])
def lesson_list():
    if request.method == 'GET':
        token = request.headers.get('Authorization').strip("\"")
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo['email']
        user_id = user_collection.find_one({"email": email})['_id']

        lessons_data = lesson_collection.find({"user_id": user_id})
        lessons = []

        for lesson in lessons_data:
            lessons.append({
                "id": lesson['_id'],
                "language": lesson['language'],
                "description": lesson['description'],
                "title": lesson['title'],
            })

        return json_util.dumps(lessons)
    
    elif request.method == 'POST':
        token = request.headers.get('Authorization').strip("\"") 
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo['email']
        user_id = user_collection.find_one({"email": email})['_id']

        (language, description, title, text) = (
            request.json['language'], 
            request.json['description'], 
            request.json['title'], 
            request.json['text']
            )

        # split text into words, leading and trailing remove punctuation
        words = text.split()
        words = [word.lstrip(punctuation).rstrip(punctuation).lower() for word in words]

        word_ids = []

        # create words if not exist, and get word ids
        for word in words:
            find_word = word_collection.find_one({"value": word, "language": language, "user": user_id})
            if find_word is None:
                # print ("New Word Created")
                word_id = word_collection.insert_one({
                    "value": word, 
                    "language": language, 
                    "translations": ["test translation"], 
                    "user_id": user_id,
                    "knowledge": 0
                    }).inserted_id
            else:
                word_id = find_word['_id']

            word_ids.append(word_id)

        # create lesson
        lesson_id = lesson_collection.insert_one({
            "language": language,
            "description": description,
            "title": title,
            "word_ids": word_ids,
            "user_id": user_id
        }).inserted_id

        # split text into sentences
        sentences = re.split('(?<=[.!?]) +',text)
        
        # create sentences
        for sentence in sentences:
            sentence_collection.insert_one({
                "value": sentence,
                "language": language,
                "lesson_id": lesson_id,
                "translations": ["test translation"]
            })

        # link lesson to user
        user_collection.update_one({"_id": user_id}, {"$push": {"lessons": lesson_id}})

        return json.dumps({'success':True})
    
@app.route('/lesson/<lesson_id>', methods=['DELETE'])
def lesson(lesson_id = None):
    if request.method == 'DELETE':
        token = request.headers.get('Authorization').strip("\"") 
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo['email']
        user_id = user_collection.find_one({"email": email})['_id']

        if lesson_id is not None:

            # delete sentences
            sentence_collection.delete_many({"lesson_id": lesson_id})

            # delete lesson
            lesson_collection.delete_one({"_id": ObjectId(lesson_id)})
            # remove lesson from user
            user_collection.update_one({"_id": user_id}, {"$pull": {"lessons": lesson_id}})
            return json.dumps({'success':True})
        else:
            return json.dumps({'success':False})


if __name__ == '__main__':
   app.run(debug=True)