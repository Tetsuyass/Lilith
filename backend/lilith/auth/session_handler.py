"""
Handle current user's session.
"""

import json
from routes import ROUTES

json_path = ROUTES["cache"] + "/user_session.json"
with open(json_path, "r") as f:
    data = json.load(f)


class Session:
    """
    Json file should be :
    {
        "user": {
            "username": "",
            ""...: "",
        },
    }
    """
    def __init__(self):
        self.user = None

    def start(self):
        self.user = data["user"]

    def get_username(self):
        return self.user["username"]


