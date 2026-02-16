import sqlalchemy as sa
from sqlalchemy.orm import Session
from routes import CONFIG_PATH
import json


class Database:
    def __init__(self):
        self.engine = None
        self.session = None

    def __start__(self):
        with open(CONFIG_PATH, 'r') as f:
            db_credentials = json.load(f)
        db_adress = db_credentials["tokens"]['adress_bdd']
        self.engine = sa.create_engine(db_adress)
        self.session = Session(self.engine)

