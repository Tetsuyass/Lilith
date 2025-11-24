from .load_data import load_model_discussion, bnb_config
import sqlalchemy as db
import json
from routes import CONFIG_PATH

models = {
    "llama-3.1-8b-ins": "meta-llama/Llama-3.1-8B-Instruct",
    "llama-3.1-8b": "meta-llama/Llama-3.1-8B"
}


class Core:
    def __init__(self):
        self.pipe = None
        self.conn_db = None

    def __start__(self):
        self.pipe = load_model_discussion(models["llama-3.1-8b"], bnb_config)
        with open(CONFIG_PATH, 'r') as f:
            db_credentials = json.load(f)
        db_adress = db_credentials["tokens"]['adress_bdd']
        engine = db.create_engine(db_adress)
        self.conn_db = engine.connect()
