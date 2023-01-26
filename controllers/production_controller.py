import uuid
from database import db_session
from flask import request, Blueprint
from models.production_model import Production
from models.user_model import User
from services.metrics import Metrics

production_blueprint = Blueprint('production_blueprint',__name__)

@production_blueprint.route("/production", methods=["GET"])
def production_list():
    productions = Production.query.all()
    response = []
    for production in productions:
        response.append({'id': production.id, 'title':production.title, "text":production.text, 'user_id': production.user_id})
    return response

@production_blueprint.route("/production/<string:id>", methods=["GET"])
def production_detail(id):
    production = Production.query.filter(Production.id == id).first()
    if production:
        response = {'id': production.id, 'text': production.text, 'user_id':production.user_id}
        return response
    return {"message":"Production not found"}, 404
    
@production_blueprint.route("/production", methods=["POST"])
def production_create():
    user = User.query.filter(User.id == request.form["user_id"]).first()
    if user:
        production = Production(
            id = uuid.uuid4(),
            title=request.form["title"],
            text=request.form["text"],
            user_id=request.form["user_id"],
        )
        db_session.add(production)
        db_session.commit()
        response = {'id': production.id, 'title':production.title, "text":production.text, 'user_id': production.user_id}
        return response
    return {"message":"User not found"}, 404

@production_blueprint.route("/production/<string:id>", methods=["PUT"])
def production_update(id):
    production = Production.query.filter(Production.id == id).first()
    if production:
        db_session.delete(production)
        db_session.commit()

        new_production = Production(
            id= id,
            title=request.form["title"],
            text=request.form["text"],
            user_id=request.form["user_id"],
        )
        db_session.add(new_production)
        db_session.commit()
        response = {'id': new_production.id, 'title':new_production.title, "text":new_production.text, 'user_id': new_production.user_id}
        return response
    else:
        return {"message":"Production not found"}, 404

@production_blueprint.route("/production/<string:id>", methods=["DELETE"])
def production_delete(id):
    production = Production.query.filter(Production.id == id).first()
    db_session.delete(production)
    db_session.commit()
    return {"message":"Production Deleted!"}

@production_blueprint.route("/production/analyze", methods=["POST"])
def production_analyze():
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
