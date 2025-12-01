import sqlalchemy as db
from typing import Any


def getting_data(conn_db: Any, user_username: str, action: str = "history") -> Any:
    def getting_history() -> Any:
        query = db.text("""
            SELECT *
            FROM users
            JOIN conversations ON users.id_user = conversations.user_id
            JOIN messages ON conversations.id_conversation = messages.conversation_id
            WHERE users.username = :username;
        """)

        result = conn_db.execute(query, {"username": user_username})
        return result.fetchall()

    def getting_user_id() -> Any:
        query = db.text("""
        SELECT users.id_user FROM users WHERE users.username = :username;
        """)
        result = conn_db.execute(query, {"username": user_username})
        return result.fetchall()

    def getting_conversation_id():
        """Chercher comment avoir l'id de la conversation en cours."""
        query = db.text("""
            
        """)

    def get_session_data():
        query = db.text("""
        SELECT
        users.id_user,
        users.username,
        users.role
        FROM users WHERE users.username = :username;
        """)

        result = conn_db.execute(query, {"username": user_username})
        data = [dict(row._mapping) for row in result.fetchall()]
        return data

    match action:
        case "history":
            getting_history()
        case "user_id":
            getting_user_id()
        case "session_data":
            get_session_data()
