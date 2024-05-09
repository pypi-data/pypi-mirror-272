from csdb import api_base
import requests


def list_product_types():
    resp = requests.get(
        api_base.url("/csdb/v1/datatype/list"),
        headers={"X-AUTH-TOKEN": api_base.get_token()},
    )
    return resp.json()["data"]


def get_product_metadata(name) -> dict:
    resp = requests.get(
        api_base.url("/csdb/v1/datatype/" + name),
        headers={"X-AUTH-TOKEN": api_base.get_token()},
    )
    return resp.json()["data"]


def list_recent_file(filetype) -> list:
    resp = requests.get(
        api_base.url(
            f"/csdb/v1/storage/search?lo=and&metadata=0&pageIndex=1&pageSize=20&type={filetype}"
        ),
        headers={"X-AUTH-TOKEN": api_base.get_token()},
    )
    return resp.json()["data"]
