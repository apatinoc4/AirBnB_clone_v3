#!/usr/bin/python3
"""
States file for APi project
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def list_users():
    """lists all users"""
    s_list = []
    users = storage.all("User")
    for user in users.values():
        s_list.append(user.to_dict())
    return jsonify(s_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def GetUserById(user_id):
    """Retrieves user based on its id for GET HTTP method"""
    all_users = storage.all("User")
    for user in all_users.values():
        print(user.name, user.id)
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def DeleteUserById(user_id):
    """Deletes an user based on its id for DELETE HTTP method"""
    users = storage.all('User')
    s_id = "User." + user_id
    to_del = users.get(s_id)
    if to_del is None:
        abort(404)
    storage.delete(to_del)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def PostUser():
    """Posts a User"""
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    elif "name" not in info:
        abort(400, 'Missing name')
    user = User()
    user.name = info['name']
    user.save()
    user = user.to_dict()
    return jsonify(user), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def PutUser(user_id):
    """ Updates a User, uses PUT HTTP method"""
    exists = False
    all_users = storage.all("User")
    for user in all_users.values():
        if user.id == user_id:
            exists = True
    if not exists:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    user_update = all_users['{}.{}'.format('User', user_id)]
    user_update.name = info['name']
    user_update.save()
    user_update = user_update.to_dict()
    return jsonify(user_update), 200


if __name__ == '__main__':
    pass
