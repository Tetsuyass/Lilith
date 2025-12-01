from .load_data import load_model_discussion, bnb_config
import sqlalchemy as db
import json
from routes import CONFIG_PATH, ROUTES

models = {
    "llama-3.1-8b-ins": "meta-llama/Llama-3.1-8B-Instruct",
    "llama-3.1-8b": "meta-llama/Llama-3.1-8B"
}


class Core:
    def __init__(self):
        self.pipe = None
        self.conn_db = None
        self.session_file = ROUTES["cache"] + "/user_session.json"

    def __start__(self):
        self.pipe = load_model_discussion(models["llama-3.1-8b"], bnb_config)
        with open(CONFIG_PATH, 'r') as f:
            db_credentials = json.load(f)
        db_adress = db_credentials["tokens"]['adress_bdd']
        engine = db.create_engine(db_adress)
        self.conn_db = engine.connect()

    def build_session_file(self, username):
        from .load_data import getting_data
        session_data = getting_data(conn_db=self.conn_db, user_username=username, action="session_data")
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f)
