import bcrypt


def register_new_user(username: str, password: str):
    """
    Push new user data to database.

    :param username:
    :param password:
    :return:
    """
    from ..pushing_data import push_data
    from ...lilith import lilith_core
    payload = {"username": username, "password": password}
    if push_data(lilith_core.conn_db, action="push_new_user",data=payload) == {"status": "db_committed"}:
        return "success"
    else:
        return "fail"


def check_if_username_exists(conn_db, username: str):
    from ..check_data import check_username
    if not check_username(username, conn_db=conn_db):
        return False
    else :
        return True
