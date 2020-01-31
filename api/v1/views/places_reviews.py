#!/usr/bin/python3
"""
Review file for APi project
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def list_reviews(place_id):
    """lists all reviews"""
    r_list = []
    find_place = storage.get("Place", place_id)
    if find_place is None:
        abort(404)
    reviews = storage.all("Review")
    for review in reviews.values():
        if place_id == getattr(review, 'place_id'):
            r_list.append(review.to_dict())
    return jsonify(r_list), 200


@app_views.route("reviews/<review_id>", methods=['GET'], strict_slashes=False)
def GetReview(review_id):
    """Retrieves review based on its id for GET HTTP method"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def DeleteReview(review_id):
    """Deletes an state based on its id for DELETE HTTP method"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("places/<place_id>/reviews",
                 methods=['POST'], strict_slashes=False)
def CreateReview(place_id):
    """Post a Review"""
    info = request.get_json()
    if info is None:
        abort(400, 'Not a JSON')
    elif info.get('user_id') is None:
        abort(400, 'Missing user_id')
    elif info.get('text') is None:
        abort(400, 'Missing text')
    find_state = storage.get("Place", place_id)
    if find_state is None:
        abort(404)
    find_state = storage.get("User", info.get('user_id'))
    if find_state is None:
        abort(404)
    info['place_id'] = place_id
    new_review = Review(**info)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 methods=['PUT'], strict_slashes=False)
def UpdatesReview(review_id):
    """Updates a review uses PUT HTTP method"""
    no_changes = ['id', 'created_at',
                        'updated_at', 'state_id',
                        'user_id', 'place_id']
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    info = request.get_json()
    if info is None:
        abort(400, 'Not a JSON')
    for key, value in info.items():
        if key in no_changes:
            pass
        else:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
