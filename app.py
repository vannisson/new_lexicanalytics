import os
from flask import Flask
import nltk
from controllers.user_controller import user_blueprint
from controllers.production_controller import production_blueprint
from controllers.collection_controller import collection_blueprint

nltk.download('punkt')

app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(production_blueprint)
app.register_blueprint(collection_blueprint)

if __name__ == '__main__':
    app.run(port=8000, use_reloader=True)
