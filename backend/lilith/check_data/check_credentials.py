import sqlalchemy as db


def check_username(username: str, conn_db) -> bool:
    query = db.text(
        "SELECT 1 FROM users WHERE username=:username"
    )
    result = conn_db.execute(query, {"username": username})
    return result.fetchone() is not None

