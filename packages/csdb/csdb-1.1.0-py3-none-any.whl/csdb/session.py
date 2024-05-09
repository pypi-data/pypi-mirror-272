import json
from typing import TypedDict, List
import pathlib
import os

HOME = pathlib.Path(os.environ.get("HOME"))
file_path = HOME / ".config/csdb.conf"


class CSDBConfigItem(TypedDict):
    config_name: str
    url: str
    username: str
    password: str


class CSDBConfig(TypedDict):
    config_list: List[CSDBConfigItem]
    using: str


def load_config() -> CSDBConfig:
    
    try:
        with open(file_path, "r") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        config_data = {"config_list": [], "using": ""}
    return config_data


def save_config(config_data: CSDBConfig):
    with open(file_path, "w") as f:
        json.dump(config_data, f)


def add(config_name: str, url: str, username: str, password: str) -> CSDBConfigItem:
    config_data = load_config()
    new_config = {
        "config_name": config_name,
        "url": url,
        "username": username,
        "password": password,
    }
    config_data["config_list"].append(new_config)
    save_config(config_data)
    return new_config


def delete(config_name: str):
    config_data = load_config()
    config_data["config_list"] = [
        config for config in config_data if config["config_name"] != config_name
    ]
    save_config(config_data)


def list() -> CSDBConfig:
    return load_config()


def modify(config_name: str, url: str, username: str, password: str) -> CSDBConfigItem:
    config_data = load_config()
    for config in config_data["config_list"]:
        if config["config_name"] == config_name:
            config["url"] = url
            config["username"] = username
            config["password"] = password
            save_config(config_data)
            return config


def use(config_name: str) -> CSDBConfigItem:
    config_data = load_config()
    config_data["using"] = config_name
    save_config(config_data)
    for config in config_data["config_list"]:
        if config["config_name"] == config_name:
            return config


def get_current_config() -> CSDBConfigItem:
    """获取配置，环境变量优先"""
    if os.environ.get("CSDB_CONFIG_URL"):
        return {
            "config_name": "environ", 
            "url": os.environ.get("CSDB_CONFIG_URL"),
            "username": os.environ.get("CSDB_CONFIG_USERNAME"),
            "password": os.environ.get("CSDB_CONFIG_PASSWORD"),
        }
            
    config_data = load_config()
    config_name = config_data["using"]
    for config in config_data["config_list"]:
        if config["config_name"] == config_name:
            return config
    return None
