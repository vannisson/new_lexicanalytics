import uuid
from flask import request, jsonify, Blueprint
from models.production_model import Production
from models.collection_model import Collection
from models.user_model import User
from database import db_session

collection_blueprint = Blueprint('collection_blueprint', __name__)


@collection_blueprint.route("/collection", methods=["GET"])
def collection_list():
    try:
        collections = Collection.query.all()
        response = []
        for collection in collections:
            productions = [
                {'id': production.id, 'title': production.title, 'text': production.text} for production in collection.productions]
            response.append({
                'id': collection.id,
                'name': collection.name,
                'density': collection.density,
                'diversity': collection.diversity,
                'description': collection.description,
                'created_at': collection.created_at,
                'user_id': collection.user_id,
                'text_quantity': len(productions),
                'productions': productions
            })
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@collection_blueprint.route("/collection/<string:id>", methods=["GET"])
def collection_detail(id):
    try:
        collection = Collection.query.get(id)
        if collection:
            productions = [
                {'id': production.id, 'title': production.title, 'text': production.text} for production in collection.productions]
            response = {
                'id': collection.id,
                'name': collection.name,
                'density': collection.density,
                'diversity': collection.diversity,
                'description': collection.description,
                'created_at': collection.created_at,
                'user_id': collection.user_id,
                'text_quantity': len(productions),
                'productions': productions
            }
            return jsonify(response)
        return {"message": "Collection not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@collection_blueprint.route("/collection/user/<string:user_id>", methods=["GET"])
def collection_by_user(user_id):
    try:
        collections = Collection.query.filter_by(user_id=user_id).all()
        response = []

        for collection in collections:
            productions = [
                {'id': production.id, 'title': production.title, 'text': production.text} for production in collection.productions]
            collection_data = {
                'id': collection.id,
                'name': collection.name,
                'density': collection.density,
                'diversity': collection.diversity,
                'description': collection.description,
                'created_at': collection.created_at,
                'user_id': collection.user_id,
                'text_quantity': len(productions),
                'productions': productions
            }
            response.append(collection_data)

        return jsonify(response)
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
                name=request.form["name"],
                density=request.form.get("density"),
                diversity=request.form.get("diversity"),
                description=request.form.get("description"),
                user=user
            )

            db_session.add(collection)
            db_session.commit()
            response = {
                'id': collection.id,
                'name': collection.name,
                'user_id': collection.user_id
            }
            return jsonify(response)
        return {"message": "User not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@collection_blueprint.route("/collection/<string:id>", methods=["PUT"])
def collection_update(id):
    try:
        collection = Collection.query.get(id)
        if collection:
            collection.name = request.form.get("name", collection.name)
            collection.density = request.form.get(
                "density", collection.density)
            collection.diversity = request.form.get(
                "diversity", collection.diversity)
            collection.description = request.form.get(
                "description", collection.description)

            db_session.commit()

            response = {
                'id': collection.id,
                'name': collection.name,
                'density': collection.density,
                'diversity': collection.diversity,
                'description': collection.description,
                'created_at': collection.created_at,
                'user_id': collection.user_id
            }
            return jsonify(response)
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
