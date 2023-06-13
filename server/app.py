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
cluster = MongoClient(secrets['MONGO_URI'])
db = cluster["languageApp"]
user_collection = db["user"]
lesson_collection = db["lesson"]
word_collection = db["word"]
sentence_collection = db["sentence"]

# Google Client Configuration
GOOGLE_DISCOVERY_URL =  "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_CLIENT_ID = secrets['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = secrets['GOOGLE_CLIENT_SECRET']


# DeepL Translation API
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


# Setup
# --------------------------------------------


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

# result = translator.translate_text("Bonjour, le monde !", target_lang="EN-US")
# print(result.text)  # "Bonjour, le monde !"


#--------------------------------------------

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

        # split text into words
        words = re.findall(r"[\w']+|[.,!?;]", text)

        word_ids = []
        # create words if not exist, and get word ids
        for word in words:
            find_word = word_collection.find_one({"value": word, "language": language, "user_id": ObjectId(user_id)})
            if find_word is None:
                word_id = word_collection.insert_one({
                    "value": word, 
                    "language": language, 
                    "translations": [translator.translate_text(word, target_lang="EN-US", source_lang="FR").text], 
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
                "translations": [translator.translate_text(sentence, target_lang="EN-US", source_lang="FR").text]
            })

        # link lesson to user
        user_collection.update_one({"_id": user_id}, {"$push": {"lessons": lesson_id}})

        return json.dumps({'success':True})
    
'''
Note: the lesson id is a string
'''
@app.route('/lesson/<lesson_id>', methods=['DELETE', 'GET'])
def lesson(lesson_id = None):
    if request.method == 'DELETE':
        token = request.headers.get('Authorization').strip("\"") 
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo['email']
        user_id = user_collection.find_one({"email": email})['_id']

        if lesson_id is not None:

            # delete sentences
            sentence_collection.delete_many({"lesson_id": ObjectId(lesson_id)})

            # delete lesson
            lesson_collection.delete_one({"_id": ObjectId(lesson_id)})
            # remove lesson from user
            user_collection.update_one({"_id": user_id}, {"$pull": {"lessons": lesson_id}})
            return json.dumps({'success':True})
        else:
            return json.dumps({'success':False})
        
    elif request.method == 'GET':
        token = request.headers.get('Authorization').strip("\"") 
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo['email']
        user_id = user_collection.find_one({"email": email})['_id']

        if lesson_id is not None:
            lesson = lesson_collection.find_one({"_id": ObjectId(lesson_id)})

            # get words
            words = []
            for word_id in lesson['word_ids']:
                word = word_collection.find_one({"_id": word_id})
                words.append({
                    "id": word_id,
                    "value": word['value'],
                    "translations": word['translations'],
                    "knowledge": word['knowledge']
                })

            # get sentences
            sentences = []
            for sentence in sentence_collection.find({"lesson_id": ObjectId(lesson_id)}):
                sentences.append({
                    "id": sentence['_id'],
                    "value": sentence['value'],
                    "translations": sentence['translations']
                })

            lesson_data = {
                "id": lesson['_id'],
                "language": lesson['language'],
                "description": lesson['description'],
                "title": lesson['title'],
                "words": words,
                "sentences": sentences
            }

            return json_util.dumps(lesson_data)
        else:
            return json.dumps({'success':False})
        

@app.route('/word/knowledge/<word_id>', methods=['PUT'])
def word_knowledge(word_id = None):
    if request.method == 'PUT':

        if word_id is not None:
            word = word_collection.find_one({"_id": ObjectId(word_id)})
            word_collection.update_one({"_id": ObjectId(word_id)}, {"$set": {"knowledge": request.json['knowledge']}})
            return json.dumps({'success':True})
        else:
            return json.dumps({'success':False})

'''
The put call is actually a delete call, but I used put because I didn't want to deal with the body
'''
@app.route('/word/translation/<word_id>', methods=['POST', 'PUT'])
def word_translation(word_id = None):
    if request.method == 'POST':

        if word_id is not None:
            word_collection.update_one({"_id": ObjectId(word_id)}, {"$push": {"translations": request.json['translation']}})
            word = word_collection.find_one({"_id": ObjectId(word_id)})
            return json_util.dumps({
                "id": word['_id'],
                "value": word['value'],
                "translations": word['translations'],
                "knowledge": word['knowledge']
            })
        else:
            return json.dumps({'success':False})
    elif request.method == 'PUT':
            
            if word_id is not None:
                word_collection.update_one({"_id": ObjectId(word_id)}, {"$pull": {"translations": request.json['translation']}})
                word = word_collection.find_one({"_id": ObjectId(word_id)})
                return json_util.dumps({
                    "id": word['_id'],
                    "value": word['value'],
                    "translations": word['translations'],
                    "knowledge": word['knowledge']
                })
            else:
                return json.dumps({'success':False})

if __name__ == '__main__':
   app.run(debug=True)