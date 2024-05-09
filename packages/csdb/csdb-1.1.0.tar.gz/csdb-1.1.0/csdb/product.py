from csdb import api_base
import requests
import datetime
from typing import List, Dict, TypedDict
import logging


class TimeoutError(Exception):
    pass


def get_metadata(urn: str) -> dict:
    """
    Get the metadata for a given urn
    :param urn: the urn to get the metadata for
    :return: a dictionary with the metadata
    """
    data = requests.get(
        # flake8: noqa: E501
        api_base.url(
            f"/csdb/v1/storage/search?lo=and&metadata=1&pageIndex=1&pageSize=1000&urn="
            + urn
        ),
        headers={"X-AUTH-TOKEN": api_base.get_token()},
    ).json()["data"][0]["metadata"]

    return data


def download(urn: str, output_file: str) -> None:
    """
    Download a file from the CSDB
    :param urn: the urn to download
    :param output_file: the file to save the data to
    """
    resp = requests.get(
        api_base.url("/csdb/v1/storage/get?urn=" + urn),
        headers={"X-AUTH-TOKEN": api_base.get_token()},
        stream=True,
    )
    logging.debug(f"csdb resp status: {resp.status_code}")

    with open(output_file, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)


def upload(upload_file: str, metadata: dict, upload_path: str, timeout=60):
    """
    Upload a file with metadate to `upload_path` in CSDB
    :param upload_file: the file to upload
    :param metadata: the file's metadata file
    :param upload_path: the file path in CSDB
    """
    data = metadata
    files = {"file": open(upload_file, "rb")}
    headers = {
        "X-CSDB-AUTOINDEX": "1",
        "X-CSDB-HASHCOMPARE": "0",
        "X-AUTH-TOKEN": api_base.get_token(),
    }
    try:

        resp = requests.post(
            api_base.url("/csdb/v1/storage/upload?path=" + upload_path),
            headers=headers,
            files=files,
            data=data,
            timeout=timeout,
        )
        if resp.status_code == 200:
            print("Upload successful!")
            print(resp.text)
        else:
            print("Upload failed:", resp.text)
    except requests.exceptions.ReadTimeout as e:
        logging.critical(f"Upload {upload_file} to {upload_path} Timeout!")
        raise e


class SearchCondition(TypedDict):
    name: str
    value: str
    co: str


def adsearch(product_type: str, conditions: List[SearchCondition]) -> List[dict]:
    """
    Search for a product in the CSDB
    :param product_type: the type of product to search for
    :param conditions: the conditions to search for
    :return: a list of products that match the search
    """
    req_body = {
        "lo": "and",
        "group": conditions,
    }
    data = requests.post(
        api_base.url(
            f"/csdb/v1/storage/adsearch?pageIndex=1&pageSize=1000&type={product_type}"
        ),
        json=req_body,
        headers={"X-AUTH-TOKEN": api_base.get_token()},
    ).json()["data"]
    return data
