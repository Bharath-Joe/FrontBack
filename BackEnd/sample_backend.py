import string
import random
from random import randrange
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


users = {
    'users_list':
    [
        {
            'id': 'xyz789',
            'name': 'Charlie',
            'job': 'Janitor',
        },
        {
            'id': 'abc123',
            'name': 'Mac',
            'job': 'Bouncer',
        },
        {
            'id': 'ppp222',
            'name': 'Mac',
            'job': 'Professor',
        },
        {
            'id': 'yat999',
            'name': 'Dee',
            'job': 'Aspring actress',
        },
        {
            'id': 'zap555',
            'name': 'Dennis',
            'job': 'Bartender',
        }
    ]
}


@app.route('/users', methods=['GET', 'POST', 'DELETE'])
# GET: retrives and shows the information
# POST: adds the information
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        if search_username and search_job:
            subdict = {'users_list': []}
            for user in users['users_list']:
                if user['name'] == search_username and user['job'] == search_job:
                    subdict['users_list'].append(user)
            return subdict
        elif search_username:
            subdict = {'users_list': []}
            for user in users['users_list']:
                if user['name'] == search_username:
                    subdict['users_list'].append(user)
            return subdict
        return users
    elif request.method == 'POST':
        userToAdd = request.get_json()
        userWithID = userToAdd
        id = generateID()
        userWithID['id'] = id
        users['users_list'].append(userWithID)
        resp = jsonify(success=True)
        resp.status_code = 201 #optionally, you can always set a response code.
        # 200 is the default code for a normal response
        return resp
    elif request.method == 'DELETE':
        userToremove = request.get_json()
        users['users_list'].remove(userToremove)
        resp = jsonify(success=True)
        return resp


@app.route('/users/<id>')
def get_user(id):
    if id:
        for user in users['users_list']:
            if user['id'] == id:
                return user
        return ({})
    return users

def generateID():
    id = ""
    for i in range(3):
        char = random.choice(string.ascii_letters)
        id = id + char.lower()
    for i in range(3):
        num = randrange(10)
        id = id + str(num)
    return id
    