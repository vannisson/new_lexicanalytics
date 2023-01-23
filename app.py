import os
from flask import Flask
from dotenv import load_dotenv
from database import db
from controllers.user_controller import user_blueprint
from controllers.production_controller import production_blueprint

load_dotenv()

app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(production_blueprint)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")

db.init_app(app)

if __name__ == '__main__':
    app.run(port=8000, use_reloader=True)