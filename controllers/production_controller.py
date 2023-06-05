import uuid
from flask import request, jsonify, Blueprint
from models.production_model import Production
from models.collection_model import Collection
from models.user_model import User
from services.metrics import Metrics
from database import db_session

production_blueprint = Blueprint('production_blueprint', __name__)


@production_blueprint.route("/production", methods=["GET"])
def production_list():
    try:
        productions = Production.query.all()
        response = []
        for production in productions:
            response.append({
                'id': production.id,
                'title': production.title,
                'text': production.text,
                'collection_id': production.collection_id
            })
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@production_blueprint.route("/production/<string:id>", methods=["GET"])
def production_detail(id):
    try:
        production = Production.query.get(id)
        if production:
            response = {
                'id': production.id,
                'title': production.title,
                'text': production.text,
                'collection_id': production.collection_id
            }
            return jsonify(response)
        return {"message": "Production not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@production_blueprint.route("/production", methods=["POST"])
def production_create():
    try:
        collection_id = request.form.get("collection_id")
        collection = Collection.query.get(collection_id)
        if collection:
            production = Production(
                id=uuid.uuid4(),
                title=request.form["title"],
                text=request.form["text"],
                collection=collection
            )

            db_session.add(production)
            db_session.commit()
            response = {
                'id': production.id,
                'title': production.title,
                'text': production.text,
                'collection_id': production.collection_id
            }
            return jsonify(response)
        return {"message": "Collection not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@production_blueprint.route("/production/<string:id>", methods=["PUT"])
def production_update(id):
    try:
        production = Production.query.get(id)
        if production:
            production.title = request.form.get("title", production.title)
            production.text = request.form.get("text", production.text)
            collection_id = request.form.get("collection_id")
            collection = Collection.query.get(collection_id)
            if collection:
                production.collection = collection

            db_session.commit()

            response = {
                'id': production.id,
                'title': production.title,
                'text': production.text,
                'collection_id': production.collection_id
            }
            return jsonify(response)
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


@production_blueprint.route("/production/analyze", methods=["POST"])
def production_analyze():
    try:
        text = request.form["text"]
        metric = Metrics(text)
        subs, verbs, adj, adv = metric.countLexicalItems()
        pro, art, others = metric.countNonLexicalItems()

        response = {
            "word_frequency": metric.wordFrequency(text),
            "word_tagged": metric.tagger_words,
            "n_lines": metric.numberOfLines(),
            "n_tokens": metric.numberOfTokens(),
            "n_types": metric.numberOfTypes(),
            "ure_density": metric.calculateUre(),
            "halliday_density": metric.calculateHalliday(),
            "lexical_items": {
                "subs": subs,
                "verbs": verbs,
                "adj": adj,
                "adv": adv,
            },
            "non_lexical_items": {
                "pro": pro,
                "art": art,
                "others": others,
            },
            "ttr_diversity": metric.calculateTTR(),
            "rttr_diversity": metric.calculateRTTR(),
            "cttr_diversity": metric.calculateCTTR(),
            "msttr_diversity": metric.calculateMSTTR(),
            "mattr_diversity": metric.calculateMATTR(),
            "mtld_diversity": metric.calculateMTLD(),
            "hdd_diversity": metric.calculateHDD(),
            "vocd_diversity": metric.calculateVOCD(),
            "herdan_diversity": metric.calculateHerdan(),
            "summer_diversity": metric.calculateSummer(),
            "dugast_diversity": metric.calculateDugast(),
            "maas_diversity": metric.calculateMaas()
        }

        return response
    except Exception as e:
        return jsonify({"message": str(e)}), 500
