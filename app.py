import os
from flask import Flask
from flask_cors import CORS
import nltk
from controllers.__all__controller import user_blueprint, production_blueprint, collection_blueprint

nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))

if not os.path.exists(os.path.join(os.path.dirname(__file__), 'nltk_data/tokenizers/punkt')):
    nltk.download('punkt', download_dir='nltk_data')

app = Flask(__name__)
CORS(app)
app.register_blueprint(user_blueprint)
app.register_blueprint(production_blueprint)
app.register_blueprint(collection_blueprint)

if __name__ == '__main__':
    app.run(port=8000, use_reloader=True)
