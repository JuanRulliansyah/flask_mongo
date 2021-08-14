import bcrypt

from flask import request
from flask_restful import Resource
from pymongo import MongoClient


def db():
    client = MongoClient("mongodb://localhost:27017")
    db = client.flask_db
    return db


class Register(Resource):
    def post(self):
        # Data Collection
        data = request.get_json()
        username = data['username']
        password = data['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db().users.insert({
            'username': username,
            'password': hashed_password,
            'sentence': "",
            'token': 6
        })

        return {
            "message": "Sucessfully registered"
        }


def verify_auth(username, password):
    hashed_password = db().users.find({'username': username})[0]['password']
    if bcrypt.hashpw(password.encode('utf-8'), hashed_password) == hashed_password:
        return True


def count_tokens(username):
    token = db().users.find({
        'username': username
    })[0]['token']
    return token


class Store(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        sentence = data['sentence']

        # Verify the username & password match
        correct_auth = verify_auth(username, password)
        if not correct_auth:
            return {
                       "message": "Not authorized"
                   }, 401

        # Verify Token Availability
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            return {
                       "message": "Num tokens"
                   }, 400

        db().users.update(
            {'username': username},
            {
                "$set": {
                    "sentence": sentence,
                    "token": num_tokens - 1
                }
            }
        )

        return {
            "message": "Sentence saved successfully"
        }



class Sentence(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Verify the username & password match
        correct_auth = verify_auth(username, password)
        if not correct_auth:
            return {
                       "message": "Not authorized"
                   }, 401

        # Verify Token Availability
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            return {
                       "message": "Num tokens"
                   }, 400

        # Make the user pay!
        db().users.update(
            {'username': username},
            {
                "$set": {
                    "token": num_tokens - 1
                }
            }
        )

        sentence = db().users.find({'username': username})[0]['sentence']
        return {
            'detail': {
                'sentence': sentence
            }
        }

