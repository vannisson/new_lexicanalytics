# nico
import string
import random

random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range (12))
DEBUG = True

SQLALCHEMY_DATABASE_URI = f"{os.getenv('DB_TYPE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = key
