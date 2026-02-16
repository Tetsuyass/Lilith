from .session_handler import Session

current_session = Session()


def set_current_session():
    global current_session
    current_session.start()
