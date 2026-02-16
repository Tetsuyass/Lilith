from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .lilith import lilith_process_answer
from .lilith.pushing_data import push_data
from .lilith.load_data import getting_data
from .lilith import lilith_core
from .lilith.auth import register_new_user
from .handle_errors import *

# Initialisation FastAPI
app = FastAPI()

# On aura besoin d'avoir l'username pour la session sûrement depuis une fenêtre de connexion
# On peut aussi implémenter un bouton "Reter connecté" pour garder le fichier de session.
# TODO : Penser à mettre ce bouton sur le frontend

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


class ChatInput(BaseModel):
    user_message: str


class UserCheck(BaseModel):
    password: str
    username: str


@app.get("/")  # Health Check
async def read_root():
    return {"status: horny"}


@app.on_event("startup")
async def load_model(data: UserCheck):
    if lilith_core.pipe is None:
        print("Loading lilith core...")
        lilith_core.__start__()
    print("Building session...")
    lilith_core.build_session_file(data.username)
    from backend.lilith.auth import current_session
    current_session.start()


@app.post("/newchat")
async def create_convo(data: UserCheck):
    """Endpoint to create convo"""
    id_user = getting_data(conn_db=lilith_core.conn_db, user_username=data.username, action="user_id")
    push_data(conn_db=lilith_core.conn_db, user_id=id_user, action="user_id")


@app.post("/chat")
async def chat_with_lilith(chat: ChatInput):
    """Endpoint to handle chat dialogues"""
    try:
        output = lilith_process_answer(chat.user_message, lilith_core.pipe)
        return {"reply": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history(data: UserCheck):
    output = getting_data(conn_db=lilith_core.conn_db, user_username=data.username, action="history")
    print(output)


@app.post("/create_account")
async def push_account(data: UserCheck):
    register_new_user(data.username, data.password)

