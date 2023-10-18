import uuid
from flask import request, jsonify, Blueprint
from models.__all__models import Production, Collection, User
from database import db_session

collection_blueprint = Blueprint('collection_blueprint', __name__)

@collection_blueprint.route("/collection", methods=["GET"])
def collection_list():
    try:
        collections = Collection.query.all()
        response = []
        for collection in collections:
            response.append(collection.to_dict())
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@collection_blueprint.route("/collection/<string:id>", methods=["GET"])
def collection_detail(id):
    try:
        collection = Collection.query.get(id)
        if collection:
            productions = [production.to_dict() for production in collection.productions]
            response = {
                'collection': collection.to_dict(),
                'productions': productions
            }
            return jsonify(response)
        return {"message": "Collection not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@collection_blueprint.route("/collection", methods=["POST"])
def collection_create():
    try:
        user_id = request.form.get("user_id")
        user = User.query.get(user_id)
        if user:
            collection = Collection(
                id=uuid.uuid4(),
                name=request.form.get("name"),
                description=request.form.get("description"),
                user=user
            )
            db_session.add(collection)
            db_session.commit()
            return jsonify(collection.to_dict())
        return {"message": "User not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@collection_blueprint.route("/collection/<string:id>", methods=["PUT"])
def collection_update(id):
    try:
        collection = Collection.query.get(id)
        if collection:
            name = request.form.get("name")
            description = request.form.get("description")
            
            collection.name = name
            collection.description = description

            db_session.commit()
            return jsonify(collection.to_dict())
        return {"message": "Collection not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@collection_blueprint.route("/collection/<string:id>", methods=["DELETE"])
def collection_delete(id):
    try:
        collection = Collection.query.get(id)
        if collection:
            db_session.delete(collection)
            db_session.commit()
            return {"message": "Collection Deleted!"}
        return {"message": "Collection not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
