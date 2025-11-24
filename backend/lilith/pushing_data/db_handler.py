import sqlalchemy as db


def push_data(conn_db, action: str, user_id: int, data: dict | None = None):
    """
    Push les messages de la conversation contenus dans data.

    data doit être :
    {
        "messages": [
            {"context": "...", "sender": "lilith/user", "timestamp": "..."},
            ...
        ],
        "conversation_id": X
    }

    action = "create_conversation" ou "push_conversation"
    """

    if data is None:
        data = {}

    def push_conversation():
        query = db.text("""
            INSERT INTO conversations (user_id)
            VALUES (:user_id);
        """)

        result = conn_db.execute(query, {"user_id": user_id})
        new_id = result.scalar()  # Récupère l'id de la conversation créée

        conn_db.commit()
        return new_id

    def push_conversation_messages():
        if "messages" not in data or "conversation_id" not in data:
            raise ValueError("data doit contenir 'messages' et 'conversation_id'.")

        query = db.text("""
            INSERT INTO messages (conversation_id, sender, context, created_at)
            VALUES (:conversation_id, :sender, :context, :time)
        """)

        payload = [
            {
                "conversation_id": data["conversation_id"],
                "sender": msg["sender"],
                "context": msg["context"],
                "time": msg["timestamp"]
            }
            for msg in data["messages"]
        ]

        conn_db.execute(query, payload)
        conn_db.commit()

    match action:
        case "create_conversation":
            conv_id = push_conversation()
            return {"status": "db_committed", "conversation_id": conv_id}

        case "push_conversation":
            push_conversation_messages()
            return {"status": "db_committed"}

        case _:
            raise ValueError("Action inconnue.")
