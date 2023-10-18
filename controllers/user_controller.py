from flask import request, jsonify, Blueprint
from models.__all__models import Production, Collection, User
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
            response.append(user.to_dict())
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@user_blueprint.route("/user/<string:id>", methods=["GET"])
def user_detail(id):
    try:
        user = User.query.filter(User.id == id).first()
        if user:
            collections = [collection.to_dict() for collection in user.collections]
            response = {
                'user': user.to_dict(),
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
        city = request.form.get("city")
        state = request.form.get("state")
        country = request.form.get("country")
        user_exists = User.query.filter(User.email == email).first()
        if user_exists:
            return jsonify({"message": "User already exists"}), 409
        else:
            user = User(
                id=uuid.uuid4(),
                name=name,
                email=email,
                password=generate_password_hash(password),
                city=city,
                state=state,
                country=country
            )
            db_session.add(user)
            db_session.commit()
            return jsonify(user.to_dict())
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
            city = request.form.get("city")
            state = request.form.get("state")
            country = request.form.get("country")

            user.name = name
            user.email = email
            user.password = generate_password_hash(password)
            user.city = city
            user.state = state
            user.country = country

            db_session.commit()

            return jsonify(user.to_dict())
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
