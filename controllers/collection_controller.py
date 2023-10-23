import uuid
from flask import request, jsonify, Blueprint
from models.__all__models import Production, Collection, User
from database import db_session
import numpy as np
from scipy import stats as st

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
        if collection:
            data = {
                "n_lines":[],
                "n_tokens":[],
                "n_types":[], 
                "ure_density": [],
                "halliday_density": [],
                "ttr_diversity": [],
                "rttr_diversity": [],
                "cttr_diversity": [],
                "msttr_diversity": [],
                "mattr_diversity": [],
                "mtld_diversity": [],
                "hdd_diversity": [],
                "vocd_diversity": [],
                "herdan_diversity": [],
                "summer_diversity": [],
                "dugast_diversity": [],
                "maas_diversity": [],
                "subs": [],
                "verbs": [],
                "adj": [],
                "adv": [],
                "pro": [],
                "art": [],
                "others": []
                }
            productions = []
            for production in collection.productions:
                productions.append(production.to_dict())
                
                data["n_lines"].append(production.n_lines)
                data["n_tokens"].append(production.n_tokens)
                data["n_types"].append(production.n_types)
                
                data["ure_density"].append(production.ure_density)
                data["halliday_density"].append(production.halliday_density)
                
                data["ttr_diversity"].append(production.ttr_diversity)
                data["rttr_diversity"].append(production.rttr_diversity)
                data["cttr_diversity"].append(production.cttr_diversity)
                data["msttr_diversity"].append(production.msttr_diversity)
                data["mattr_diversity"].append(production.mattr_diversity)
                data["mtld_diversity"].append(production.mtld_diversity)
                data["hdd_diversity"].append(production.hdd_diversity)
                data["vocd_diversity"].append(production.vocd_diversity)
                data["herdan_diversity"].append(production.herdan_diversity)
                data["summer_diversity"].append(production.summer_diversity)
                data["dugast_diversity"].append(production.dugast_diversity)
                data["maas_diversity"].append(production.maas_diversity)
                
                data["subs"].append(production.lexical_items["subs"])
                data["verbs"].append(production.lexical_items["verbs"])
                data["adj"].append(production.lexical_items["adj"])
                data["adv"].append(production.lexical_items["adv"])
                
                data["pro"].append(production.non_lexical_items["pro"])
                data["art"].append(production.non_lexical_items["art"])
                data["others"].append(production.non_lexical_items["others"])

            general_statistics = {
                "productions": productions,
                "mean": {
                        "n_lines": np.mean(data["n_lines"]),
                        "n_tokens": np.mean(data["n_tokens"]),
                        "n_types": np.mean(data["n_types"]),
                    
                        "ure_density": np.mean(data["ure_density"]),
                        "halliday_density": np.mean(data["halliday_density"]),
                        
                        "ttr_diversity": np.mean(data["ttr_diversity"]),
                        "rttr_diversity": np.mean(data["rttr_diversity"]),
                        "cttr_diversity": np.mean(data["cttr_diversity"]),
                        "msttr_diversity": np.mean(data["msttr_diversity"]),
                        "mattr_diversity": np.mean(data["mattr_diversity"]),
                        "mtld_diversity": np.mean(data["mtld_diversity"]),
                        "hdd_diversity": np.mean(data["hdd_diversity"]),
                        "vocd_diversity": np.mean(data["vocd_diversity"]),
                        "herdan_diversity": np.mean(data["herdan_diversity"]),
                        "summer_diversity": np.mean(data["summer_diversity"]),
                        "dugast_diversity": np.mean(data["dugast_diversity"]),
                        "maas_diversity": np.mean(data["maas_diversity"]),
                        
                        "subs": np.mean(data["subs"]),
                        "verbs": np.mean(data["verbs"]),
                        "adj": np.mean(data["adj"]),
                        "adv": np.mean(data["adv"]),
                        
                        "pro": np.mean(data["pro"]),
                        "art": np.mean(data["art"]),
                        "others": np.mean(data["others"]),
                        },
                        
                "median": {
                        "n_lines": float(st.mode(data["n_lines"]).mode),
                        "n_tokens": float(st.mode(data["n_tokens"]).mode),
                        "n_types": float(st.mode(data["n_types"]).mode),
                    
                        "ure_density": float(st.mode(data["ure_density"]).mode),
                        "halliday_density": float(st.mode(data["halliday_density"]).mode),
                        
                        "ttr_diversity": float(st.mode(data["ttr_diversity"]).mode),
                        "rttr_diversity": float(st.mode(data["rttr_diversity"]).mode),
                        "cttr_diversity": float(st.mode(data["cttr_diversity"]).mode),
                        "msttr_diversity": float(st.mode(data["msttr_diversity"]).mode),
                        "mattr_diversity": float(st.mode(data["mattr_diversity"]).mode),
                        "mtld_diversity": float(st.mode(data["mtld_diversity"]).mode),
                        "hdd_diversity": float(st.mode(data["hdd_diversity"]).mode),
                        "vocd_diversity": float(st.mode(data["vocd_diversity"]).mode),
                        "herdan_diversity": float(st.mode(data["herdan_diversity"]).mode),
                        "summer_diversity": float(st.mode(data["summer_diversity"]).mode),
                        "dugast_diversity": float(st.mode(data["dugast_diversity"]).mode),
                        "maas_diversity": float(st.mode(data["maas_diversity"]).mode),
                        
                        "subs": float(st.mode(data["subs"]).mode),
                        "verbs": float(st.mode(data["verbs"]).mode),
                        "adj": float(st.mode(data["adj"]).mode),
                        "adv": float(st.mode(data["adv"]).mode),
                        
                        "pro": float(st.mode(data["pro"]).mode),
                        "art": float(st.mode(data["art"]).mode),
                        "others": float(st.mode(data["others"]).mode),
                        },
                
                "mode": {
                        "n_lines": np.median(data["n_lines"]),
                        "n_tokens": np.median(data["n_tokens"]),
                        "n_types": np.median(data["n_types"]),
                    
                        "ure_density": np.median(data["ure_density"]),
                        "halliday_density": np.median(data["halliday_density"]),
                        
                        "ttr_diversity": np.median(data["ttr_diversity"]),
                        "rttr_diversity": np.median(data["rttr_diversity"]),
                        "cttr_diversity": np.median(data["cttr_diversity"]),
                        "msttr_diversity": np.median(data["msttr_diversity"]),
                        "mattr_diversity": np.median(data["mattr_diversity"]),
                        "mtld_diversity": np.median(data["mtld_diversity"]),
                        "hdd_diversity": np.median(data["hdd_diversity"]),
                        "vocd_diversity": np.median(data["vocd_diversity"]),
                        "herdan_diversity": np.median(data["herdan_diversity"]),
                        "summer_diversity": np.median(data["summer_diversity"]),
                        "dugast_diversity": np.median(data["dugast_diversity"]),
                        "maas_diversity": np.median(data["maas_diversity"]),
                        
                        "subs": np.median(data["subs"]),
                        "verbs": np.median(data["verbs"]),
                        "adj": np.median(data["adj"]),
                        "adv": np.median(data["adv"]),
                        
                        "pro": np.median(data["pro"]),
                        "art": np.median(data["art"]),
                        "others": np.median(data["others"]),
                        },

                "standard_deviation": {
                        "n_lines": np.std(data["n_lines"]),
                        "n_tokens": np.std(data["n_tokens"]),
                        "n_types": np.std(data["n_types"]),
                    
                        "ure_density": np.std(data["ure_density"]),
                        "halliday_density": np.std(data["halliday_density"]),
                        
                        "ttr_diversity": np.std(data["ttr_diversity"]),
                        "rttr_diversity": np.std(data["rttr_diversity"]),
                        "cttr_diversity": np.std(data["cttr_diversity"]),
                        "msttr_diversity": np.std(data["msttr_diversity"]),
                        "mattr_diversity": np.std(data["mattr_diversity"]),
                        "mtld_diversity": np.std(data["mtld_diversity"]),
                        "hdd_diversity": np.std(data["hdd_diversity"]),
                        "vocd_diversity": np.std(data["vocd_diversity"]),
                        "herdan_diversity": np.std(data["herdan_diversity"]),
                        "summer_diversity": np.std(data["summer_diversity"]),
                        "dugast_diversity": np.std(data["dugast_diversity"]),
                        "maas_diversity": np.std(data["maas_diversity"]),
                        
                        "subs": np.std(data["subs"]),
                        "verbs": np.std(data["verbs"]),
                        "adj": np.std(data["adj"]),
                        "adv": np.std(data["adv"]),
                        
                        "pro": np.std(data["pro"]),
                        "art": np.std(data["art"]),
                        "others": np.std(data["others"]),
                        },
                        
                "minimum": {
                        "n_lines": min(data["n_lines"]),
                        "n_tokens": min(data["n_tokens"]),
                        "n_types": min(data["n_types"]),
                    
                        "ure_density": min(data["ure_density"]),
                        "halliday_density": min(data["halliday_density"]),
                        
                        "ttr_diversity": min(data["ttr_diversity"]),
                        "rttr_diversity": min(data["rttr_diversity"]),
                        "cttr_diversity": min(data["cttr_diversity"]),
                        "msttr_diversity": min(data["msttr_diversity"]),
                        "mattr_diversity": min(data["mattr_diversity"]),
                        "mtld_diversity": min(data["mtld_diversity"]),
                        "hdd_diversity": min(data["hdd_diversity"]),
                        "vocd_diversity": min(data["vocd_diversity"]),
                        "herdan_diversity": min(data["herdan_diversity"]),
                        "summer_diversity": min(data["summer_diversity"]),
                        "dugast_diversity": min(data["dugast_diversity"]),
                        "maas_diversity": min(data["maas_diversity"]),
                        
                        "subs": min(data["subs"]),
                        "verbs": min(data["verbs"]),
                        "adj": min(data["adj"]),
                        "adv": min(data["adv"]),
                        
                        "pro": min(data["pro"]),
                        "art": min(data["art"]),
                        "others": min(data["others"]),
                        },
                
                "maximum": {
                        "n_lines": max(data["n_lines"]),
                        "n_tokens": max(data["n_tokens"]),
                        "n_types": max(data["n_types"]),
                    
                        "ure_density": max(data["ure_density"]),
                        "halliday_density": max(data["halliday_density"]),
                        
                        "ttr_diversity": max(data["ttr_diversity"]),
                        "rttr_diversity": max(data["rttr_diversity"]),
                        "cttr_diversity": max(data["cttr_diversity"]),
                        "msttr_diversity": max(data["msttr_diversity"]),
                        "mattr_diversity": max(data["mattr_diversity"]),
                        "mtld_diversity": max(data["mtld_diversity"]),
                        "hdd_diversity": max(data["hdd_diversity"]),
                        "vocd_diversity": max(data["vocd_diversity"]),
                        "herdan_diversity": max(data["herdan_diversity"]),
                        "summer_diversity": max(data["summer_diversity"]),
                        "dugast_diversity": max(data["dugast_diversity"]),
                        "maas_diversity": max(data["maas_diversity"]),
                        
                        "subs": max(data["subs"]),
                        "verbs": max(data["verbs"]),
                        "adj": max(data["adj"]),
                        "adv": max(data["adv"]),
                        
                        "pro": max(data["pro"]),
                        "art": max(data["art"]),
                        "others": max(data["others"]),
                        },
            }
            return general_statistics
        return {"message": "Collection not found"}, 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500