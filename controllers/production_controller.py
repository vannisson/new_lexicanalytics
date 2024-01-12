import uuid
from flask import request, jsonify, Blueprint
from models.__all__models import Production, Collection, User
from services.metrics import Metrics
from database import db_session

production_blueprint = Blueprint('production_blueprint', __name__)

@production_blueprint.route("/production", methods=["GET"])
def production_list():
    try:
        productions = Production.query.all()
        response = []
        for production in productions:
            response.append(production.to_dict())
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@production_blueprint.route("/production/<string:id>", methods=["GET"])
def production_detail(id):
    try:
        production = Production.query.get(id)
        if production:
            return jsonify(production.to_dict())
        return {"message": "Production not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@production_blueprint.route("/production", methods=["POST"])
def production_create():
    try:
        collection_id = request.form.get("collection_id")
        collection = Collection.query.get(collection_id)
        if collection:
            title = request.form.get("title")
            text = request.form.get("text")
            
            production = Production(
                            id = uuid.uuid4(),
                            title = title,
                            text = text,
                            collection_id = collection_id
                        )

            db_session.add(production)
            db_session.commit()
            return jsonify(production.to_dict())
        return {"message": "Collection not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@production_blueprint.route("/production/<string:id>", methods=["PUT"])
def production_update(id):
    try:
        production = Production.query.get(id)
        if production:
            title = request.form.get("title")
            text = request.form.get("text")
            
            production.title = title
            production.text = text

            db_session.commit()

            return jsonify(production.to_dict())
        return {"message": "Production not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@production_blueprint.route("/production/<string:id>", methods=["DELETE"])
def production_delete(id):
    try:
        production = Production.query.get(id)
        if production:
            db_session.delete(production)
            db_session.commit()
            return {"message": "Production Deleted!"}
        return {"message": "Production not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
