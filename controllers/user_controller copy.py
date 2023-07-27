import json
from flask import request, jsonify, Blueprint
from models.user_model import User
from models.collection_model import Collection
from models.production_model import Production
from werkzeug.security import generate_password_hash, check_password_hash
from database import db_session
import uuid

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route("/auth", methods=["POST"])
def auth_user():
    user = User.query.filter(User.email == request.form["email"]).first()
    if user:
        if check_password_hash(user.password, request.form["password"]):
            return jsonify({"message": "Authenticated"})
        else:
            return jsonify({"message": "Passwords not Match"})

    else:
        return "Not Found", 404


@user_blueprint.route("/user", methods=["GET"])
def user_list():
    users = User.query.all()
    response = []
    for user in users:
        response.append({'id': user.id, 'password': user.password,
                        'name': user.name, 'email': user.email})
    return response


@user_blueprint.route("/user/<string:id>", methods=["GET"])
def user_detail(id):
    user = User.query.filter(User.id == id).first()
    if user:
        response = {'id': user.id, 'password': user.password,
                    'name': user.name, 'email': user.email}
        return response
    else:
        return {"message": "User not found"}, 404


@user_blueprint.route("/user", methods=["POST"])
def user_create():
    user_exists = User.query.filter(
        User.email == request.form["email"]).first()
    if user_exists:
        return {"message": "User already exists"}
    else:
        user = User(
            id=uuid.uuid4(),
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"])
        )
        db_session.add(user)
        db_session.commit()
        response = {'id': user.id, 'password': user.password,
                    'name': user.name, 'email': user.email}
        return response


@user_blueprint.route("/user/<string:id>", methods=["PUT"])
def user_update(id):
    user = User.query.filter(User.id == id).first()
    if user:
        db_session.delete(user)
        db_session.commit()

        new_user = User(
            id=id,
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"])
        )
        db_session.add(new_user)
        db_session.commit()
        response = {'id': new_user.id, 'password': new_user.password,
                    'name': new_user.name, 'email': new_user.email}
        return response
    else:
        return {"message": "User not found"}, 404


@user_blueprint.route("/user/<string:id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.filter(User.id == id).first()
    if user:
        db_session.delete(user)
        db_session.commit()
        return {"message": "User Deleted"}
    else:
        return {"message": "User not found"}, 404
