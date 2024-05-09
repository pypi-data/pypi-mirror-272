import requests

from csdb import session

_auth = {"token": ""}


def auth() -> tuple:
    cur_config = session.get_current_config()
    if cur_config:
        return cur_config["username"], cur_config["password"]


def url(path: str) -> str:
    BASE_URL = session.get_current_config()["url"]

    return BASE_URL + path


def get_token():
    if not _auth["token"]:
        cur_config = session.get_current_config()
        resp = requests.post(
            url("/user/auth/token"),
            json={
                # "aesFlag": True,
                "password": cur_config["password"],
                "username": cur_config["username"],
            },
            headers={"Content-Type": "application/json", "accept": "*/*"},
        )
        _auth["token"] = resp.json()["data"]["token"]
    return _auth["token"]
