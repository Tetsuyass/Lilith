from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .lilith import lilith_process_answer
from .lilith import Core
from .lilith.pushing_data import push_data
from .lilith.load_data import getting_data
from routes import LILITH_CONFIG_PATH
import json

# Initialisation de Lilith
lilith_core = Core()

# Initialisation FastAPI
app = FastAPI()

origins = [
    "http://localhost:5173",  # Default Vite React dev server
    "http://localhost:3000",  # Common Create React App dev server
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


@app.get("/")  # Health Check
async def read_root():
    return {"status: horny"}


@app.on_event("startup")
async def load_model():
    global lilith_core
    if lilith_core.pipe is None:
        print("Loading lilith core")
        lilith_core.__start__()


with open(LILITH_CONFIG_PATH, "r") as f:
    config_lilith = json.load(f)
    user_username = config_lilith["basic-config"]["user"]


@app.post("/newchat")
async def create_convo():
    """Endpoint to create convo"""
    id_user = getting_data(conn_db=lilith_core.conn_db, user_username=user_username, action="user_id")
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
async def get_history():
    output = getting_data(conn_db=lilith_core.conn_db, user_username=user_username)
    print(output)
