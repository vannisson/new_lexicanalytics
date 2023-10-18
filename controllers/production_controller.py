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
            
            metric = Metrics(text)
            subs, verbs, adj, adv = metric.countLexicalItems()
            pro, art, others = metric.countNonLexicalItems()
            lexical_items = {"subs": subs, "verbs": verbs, "adj": adj, "adv": adv}
            non_lexical_items = {"pro": pro, "art": art, "others": others}
            
            production = Production(
                            id = uuid.uuid4(),
                            title = title,
                            text = text,
                            n_lines = metric.numberOfLines(),
                            n_tokens = metric.numberOfTokens(),
                            n_types = metric.numberOfTypes(),
                            ure_density = metric.calculateUre(),
                            halliday_density = metric.calculateHalliday(),
                            ttr_diversity = metric.calculateTTR(),
                            rttr_diversity = metric.calculateRTTR(),
                            cttr_diversity = metric.calculateCTTR(),
                            msttr_diversity = metric.calculateMSTTR(),
                            mattr_diversity = metric.calculateMATTR(),
                            mtld_diversity = metric.calculateMTLD(),
                            hdd_diversity = metric.calculateHDD(),
                            vocd_diversity = metric.calculateVOCD(),
                            herdan_diversity = metric.calculateHerdan(),
                            summer_diversity = metric.calculateSummer(),
                            dugast_diversity = metric.calculateDugast(),
                            maas_diversity = metric.calculateMaas(),
                            word_frequency = metric.wordFrequency(text),
                            word_tagged = metric.tagger_words,
                            lexical_items = lexical_items,
                            non_lexical_items = non_lexical_items,
                            collection = collection
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
            metric = Metrics(text)
            subs, verbs, adj, adv = metric.countLexicalItems()
            pro, art, others = metric.countNonLexicalItems()
            
            production.title = title
            production.text = text
            production.n_lines = metric.numberOfLines(),
            production.n_tokens = metric.numberOfTokens(),
            production.n_types = metric.numberOfTypes(),
            production.ure_density = metric.calculateUre(),
            production.halliday_density = metric.calculateHalliday(),
            production.ttr_diversity = metric.calculateTTR(),
            production.rttr_diversity = metric.calculateRTTR(),
            production.cttr_diversity = metric.calculateCTTR(),
            production.msttr_diversity = metric.calculateMSTTR(),
            production.mattr_diversity = metric.calculateMATTR(),
            production.mtld_diversity = metric.calculateMTLD(),
            production.hdd_diversity = metric.calculateHDD(),
            production.vocd_diversity = metric.calculateVOCD(),
            production.herdan_diversity = metric.calculateHerdan(),
            production.summer_diversity = metric.calculateSummer(),
            production.dugast_diversity = metric.calculateDugast(),
            production.maas_diversity = metric.calculateMaas(),
            production.word_frequency = metric.wordFrequency(text),
            production.word_tagged = metric.tagger_words,
            production.lexical_items = {"subs": subs, "verbs": verbs, "adj": adj, "adv": adv}
            production.non_lexical_items = {"pro": pro, "art": art, "others": others}

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
