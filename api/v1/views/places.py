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
    u_id = "User." + user_id
    if all_users.get(u_id) is None:
        abort(404)
    user = all_users.get(u_id).to_dict()
    return user


@app_views.route('/users/<user_id>', methods=['DELETE'])
def DeleteUserById(user_id):
    """Deletes an user based on its id for DELETE HTTP method"""
    all_users = storage.all(User)
    u_id = "User." + user_id
    to_del = all_users.get(u_id)
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
    elif "email" not in info:
        abort(400, 'Missing email')
    elif "password" not in info:
        abort(400, 'Missing password')
    user = User()
    user.email = info['email']
    user.password = info['password']
    user.save()
    user = user.to_dict()
    return jsonify(user), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def PutUser(user_id):
    """ Updates a User, uses PUT HTTP method"""
    info = request.get_json()
    all_users = storage.all(User)
    pair = 'User.' + user_id
    if all_users.get(pair) is None:
        abort(404)
    if not info:
        abort(400, 'Not a JSON')
    else:
        user = all_users.get(pair)
        for key, value in info.items():
            if key != "id" and key != "created_at" \
                    and key != "updated_at" and key != 'email':
                setattr(user, key, value)
        user.save()
        user = user.to_dict()
    return jsonify(user), 200


if __name__ == '__main__':
    pass