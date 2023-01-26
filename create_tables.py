from database import init_db

# def create_tables() -> None:
#   import models.__all_models
#   print("Creating Tables")
#   with app.app_context():
#     db.create_all()
#   print('Tables created successfully...')

if __name__ == '__main__':
    init_db()