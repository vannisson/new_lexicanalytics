from database import db
from flask import request, Blueprint
from models.production_model import Production
from services.metrics import Metrics

production_blueprint = Blueprint('production_blueprint',__name__)

@production_blueprint.route("/production", methods=["GET"])
def production_list():
    productions = db.session.execute(db.select(Production).order_by(Production.name)).scalars()
    return productions

@production_blueprint.route("/production/<string:id>", methods=["GET"])
def production_detail(id):
    production = db.get_or_404(Production, id)
    return production
    
@production_blueprint.route("/production", methods=["POST"])
def production_create():
    production = Production(
        text=request.form["text"],
        user_id=request.form["user_id"],
    )
    db.session.add(production)
    db.session.commit()
    return production

@production_blueprint.route("/production/<string:id>", methods=["PUT"])
def production_update(id):
    production = db.get_or_404(Production, id)

    db.session.delete(production)
    db.session.commit()

    new_production = Production(
        id= id,
        text=request.form["text"],
        user_id=request.form["user_id"],
    )
    db.session.add(new_production)
    db.session.commit()
    return new_production

@production_blueprint.route("/production/<string:id>", methods=["DELETE"])
def production_delete(id):
    production = db.get_or_404(Production, id)
    db.session.delete(production)
    db.session.commit()
    return "Done!"

@production_blueprint.route("/production/analyze", methods=["POST"])
def production_analyze():
    text = request.form["text"]
    # density_method = request.form["density_method"]
    # diversity_method = request.form["diversity_method"]
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
        "lexical_items":{
           "subs": subs,
           "verbs": verbs,
           "adj": adj,
           "adv": adv,
        },
        "non_lexical_items":{
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
