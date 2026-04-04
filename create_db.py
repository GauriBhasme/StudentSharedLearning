#after executing this file the DB will be created by models
from app import app
from db import db

with app.app_context():
    #Delete DB
    # db.drop_all()
    db.create_all()
    print("Database created successfully!")