import string
import random
from random import randrange
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from model_mongodb import User


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


users = {
    'users_list':[]
}


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        if search_username and search_job:
            users = User().find_by_name_job(search_username, search_job)
        elif search_username:
            users = User().find_by_name(search_username)
        elif search_job:
            users = User().find_by_job(search_job)
        else:
            users = User().find_all()
        return {"users_list": users}
    elif request.method == 'POST':
        userToAdd = request.get_json()
        # userWithID = userToAdd
        # id = generateID()
        # userWithID['id'] = id
        # users['users_list'].append(userWithID)
        newUser = User(userToAdd)
        newUser.save()
        resp = jsonify(newUser), 201
        print(newUser)
        print(resp)
        return resp


@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
       # update for db access
        user = User({"_id": id})
        if user.reload():
            return user
        else:
            return jsonify({"error": "User not found"}), 404
    elif request.method == 'DELETE':
        user = User({"_id": id})
        if user.remove():
            # 204 is the default code for a normal response, no other input returned
            resp = jsonify({}), 204
            return resp
        else:
            return jsonify({"error": "User not found"}), 404


# def generateID():
#     id = ""
#     for i in range(3):
#         char = random.choice(string.ascii_letters)
#         id = id + char.lower()
#     for i in range(3):
#         num = randrange(10)
#         id = id + str(num)
#     return id
