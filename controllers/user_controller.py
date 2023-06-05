from flask import request, jsonify, Blueprint
from models.user_model import User
from models.collection_model import Collection
from werkzeug.security import generate_password_hash, check_password_hash
from database import db_session
import uuid

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route("/auth", methods=["POST"])
def auth_user():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter(User.email == email).first()
        if user:
            if check_password_hash(user.password, password):
                return jsonify({"message": "Authenticated"})
            else:
                return jsonify({"message": "Passwords do not match"})
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@user_blueprint.route("/user", methods=["GET"])
def user_list():
    try:
        users = User.query.all()
        response = []
        for user in users:
            collections = [collection.id for collection in user.collections]
            response.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'collections': collections
            })
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@user_blueprint.route("/user/<string:id>", methods=["GET"])
def user_detail(id):
    try:
        user = User.query.filter(User.id == id).first()
        if user:
            collections = [collection.id for collection in user.collections]
            response = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'collections': collections
            }
            return jsonify(response)
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@user_blueprint.route("/user", methods=["POST"])
def user_create():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        user_exists = User.query.filter(User.email == email).first()
        if user_exists:
            return jsonify({"message": "User already exists"})
        else:
            user = User(
                id=uuid.uuid4(),
                name=name,
                email=email,
                password=generate_password_hash(password)
            )
            db_session.add(user)
            db_session.commit()
            response = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
            return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@user_blueprint.route("/user/<string:id>", methods=["PUT"])
def user_update(id):
    try:
        user = User.query.filter(User.id == id).first()
        if user:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            user.name = name
            user.email = email
            user.password = generate_password_hash(password)

            db_session.commit()

            response = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
            return jsonify(response)
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@user_blueprint.route("/user/<string:id>", methods=["DELETE"])
def user_delete(id):
    try:
        user = User.query.filter(User.id == id).first()
        if user:
            db_session.delete(user)
            db_session.commit()
            return jsonify({"message": "User deleted"})
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
