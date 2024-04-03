"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Planets ,Character, Favorite
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# User Routes

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = []
    for user in users:
        serialized_users.append(user.serialize())
    response_body = {
        "message": "Here are all your users", "users" : serialized_users
    }

    return jsonify(response_body), 200
    
# Character Routes

@api.route('/people', methods=['GET'])
def get_character():
    characters = Character.query.all()
    serialized_characters = []
    for x in characters:
        serialized_characters.append(x.serialize())
    response_body = {
        "message": "Here are all the characters", "characters" : serialized_characters
    }

    return jsonify(response_body), 200

# Routes of Planets

@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    serialized_planets = []
    for planet in planets:
        serialized_planets.append(planet.serialize())

    response_body = {
        "message": "Here are all the planets",
        "planets": serialized_planets
    }

    return jsonify(response_body), 200

# Get One Planet

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id = planet_id).first()

    if planet is None:
        return jsonify("Planet not found"), 404
    
    response_body = {
        "message": "Here is the planet",
        "planet": planet.serialize()
    }

    return jsonify(response_body), 200

# Getting One Character 

@api.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    person = Character.query.filter_by(id = people_id).first()

    if person is None:
        return jsonify("Character not found"), 404
    
    response_body = {
        "message": "Here is the Character",
        "person": person.serialize()
    }

    return jsonify(response_body), 200

# Getting Favorites

@api.route('/users/favorites', methods=['POST'])
def get_users_favorites():
    user_id = request.json.get("user_id")
    favorites = Favorite.query.all()
    serialized_favorites = []
    for favorite in favorites:
        if favorite.user_id == user_id:
            serialized_favorites.append(favorite.serialize())
    response_body = {
        "message": "Here are all your favorites", "favorites" : serialized_favorites
    }

    return jsonify(response_body), 200

# Posting New Planets

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_new_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    user = User.query.filter_by(id = user_id)
    if user is None:
        return jsonify({"message" : "User doesn't exist :( "}), 404
    planet = Planets.query.filter_by(id = planet_id)
    if planet is None:
        return jsonify({"message" : "Planet doesn't exist :( "}), 404
    favorite = Favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if favorite:
        return jsonify({"message" : "Planet already added"}), 409
    new_favorite = Favorite(user_id = user_id, planet_id = planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    favorites = Favorite.query.all()
    serialized_favorites = []
    for favorite in favorites:
        if favorite.user_id == user_id:
            serialized_favorites.append(favorite.serialize())
    response_body = {
        "message": "Planet successfully added to your favorites, here is the new list", "favorites" : serialized_favorites
        
    }

    return jsonify(response_body), 200

# Posting New Characters 

@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_new_favorite_character(people_id):
    user_id = request.json.get("user_id")
    user = User.query.filter_by(id = user_id)
    if user is None:
        return jsonify({"message" : "User doesn't exist :( "}), 404
    character = Character.query.filter_by(id = people_id)
    if character is None:
        return jsonify({"message" : "Character doesn't exist :( "}), 404
    favorite = Favorite.query.filter_by(user_id = user_id, character_id = people_id).first()
    if favorite:
        return jsonify({"message" : "Character already added"}), 409
    new_favorite = Favorite(user_id = user_id, character_id = people_id)
    db.session.add(new_favorite)
    db.session.commit()
    favorites = Favorite.query.all()
    serialized_favorites = []
    for favorite in favorites:
        if favorite.user_id == user_id:
            serialized_favorites.append(favorite.serialize())
    response_body = {
        "message": "Character successfully added to your favorites, here is the new list", "favorites" : serialized_favorites
    }

    return jsonify(response_body), 200

# Deleting Favorite Planet 

@api.route('/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    user = User.query.filter_by(id = user_id)
    if user is None:
        return jsonify({"message" : "User doesn't exist :( "}), 404
    favorite = Favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if favorite is None:
        return jsonify({"message" : "This planet is not part of favorites"}), 409
    db.session.delete(favorite)
    db.session.commit()
    favorites = Favorite.query.all()
    serialized_favorites = []
    for favorite in favorites:
        if favorite.user_id == user_id:
            serialized_favorites.append(favorite.serialize())
    response_body = {
        "message": "Planet succesfully deleted from your favorites, here is the new list", "favorites" : serialized_favorites
    }

    return jsonify(response_body), 200

# delete favorite character

@api.route('/favorite/people/<int:people_id>', methods = ['DELETE'])
def delete_favorite_character(people_id):
    user_id = request.json.get("user_id")
    user = User.query.filter_by(id = user_id)
    if user is None:
        return jsonify({"message" : "User doesn't exist :( "}), 404
    favorite = Favorite.query.filter_by(user_id = user_id, character_id = people_id).first()
    if favorite is None:
        return jsonify({"message" : "This character is not part of favorites"}), 409
    db.session.delete(favorite)
    db.session.commit()
    favorites = Favorite.query.all()
    serialized_favorites = []
    for favorite in favorites:
        if favorite.user_id == user_id:
            serialized_favorites.append(favorite.serialize())
    response_body = {
        "message": "Character succesfully deleted from your favorites, here is the new list ", "favorites" : serialized_favorites
    }

    return jsonify(response_body), 200