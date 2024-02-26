import uuid
from flask import request, jsonify, Blueprint
from models.__all__models import Production, Collection, User
from collections import defaultdict
from database import db_session
import numpy as np
from scipy import stats as st

from services.metrics import Metrics

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
    
@collection_blueprint.route("/collection/analyze/<string:id>", methods=["GET"])
def collection_analyze(id):
    try:
        collection = Collection.query.get(id)

        if not collection:
            return {"message": "Collection not found"}, 404

        results = calculateMetricsFromProductions(collection.productions)
        
        return results
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def calculateMetricsFromProductions(productions):
    all_productions = defaultdict(list)
    single_productions = defaultdict(list)
    tokens_statistics = defaultdict(list)
    types_statistics = defaultdict(list)
    draws = 42
    
    for production in productions:
        metric = Metrics(production.text)
        if metric.numberOfTokens() < draws:
            draws = metric.numberOfTokens() // 2

    for production in productions:
        metric = Metrics(production.text)
        POSTokens = metric.countPOSTokens()
        POSTypes = metric.countPOSTypes()
        
        n_lines = metric.numberOfLines()
        n_tokens = metric.numberOfTokens()
        n_types = metric.numberOfTypes()
        diversity = metric.calculateHDD(draws)
        density = metric.calculateNewUre()
        richness = metric.calculateRichness(density, diversity)

        tokens_count = {label: count for label, count in zip(["subs", "verb", "adj", "adv", "pro", "art", "others"], POSTokens)}
        types_count = {label: count for label, count in zip(["subs", "verb", "adj", "adv", "pro", "art", "others"], POSTypes)}

        for label, count in tokens_count.items():
            tokens_statistics[label].append(count)

        for label, count in types_count.items():
            types_statistics[label].append(count)

        all_productions["n_lines"].append(n_lines)
        all_productions["n_tokens"].append(n_tokens)
        all_productions["n_types"].append(n_types)
        all_productions["density"].append(density)
        all_productions["diversity"].append(diversity)
        all_productions["richness"].append(richness)
        
        single_productions["title"].append(production.title)
        single_productions["text"].append(production.text)
        single_productions["tagged_words"].append(metric.tagged_words)
        single_productions["n_lines"].append(n_lines)
        single_productions["n_tokens"].append(n_tokens)
        single_productions["n_types"].append(n_types)
        single_productions["density"].append(density)
        single_productions["diversity"].append(diversity)
        single_productions["richness"].append(richness)
        single_productions["tokens_count"].append(tokens_count)
        single_productions["types_count"].append(types_count)

    general_statistics_summary = {
        "mean": {key: np.mean(values) for key, values in all_productions.items()},
        "median": {key: float(st.mode(values).mode) for key, values in all_productions.items()},
        "mode": {key: np.median(values) for key, values in all_productions.items()},
        "standard_deviation": {key: np.std(values) for key, values in all_productions.items()},
        "minimum": {key: min(values) for key, values in all_productions.items()},
        "maximum": {key: max(values) for key, values in all_productions.items()},
        "tokens": {
            "mean": {label: np.mean(values) for label, values in tokens_statistics.items()},
            "median": {label: float(st.mode(values).mode) for label, values in tokens_statistics.items()},
            "mode": {label: np.median(values) for label, values in tokens_statistics.items()},
            "standard_deviation": {label: np.std(values) for label, values in tokens_statistics.items()},
            "minimum": {label: min(values) for label, values in tokens_statistics.items()},
            "maximum": {label: max(values) for label, values in tokens_statistics.items()},
        },
        "types": {
            "mean": {label: np.mean(values) for label, values in types_statistics.items()},
            "median": {label: float(st.mode(values).mode) for label, values in types_statistics.items()},
            "mode": {label: np.median(values) for label, values in types_statistics.items()},
            "standard_deviation": {label: np.std(values) for label, values in types_statistics.items()},
            "minimum": {label: min(values) for label, values in types_statistics.items()},
            "maximum": {label: max(values) for label, values in types_statistics.items()},
        },
    }

    return {"general": general_statistics_summary, "single": single_productions}