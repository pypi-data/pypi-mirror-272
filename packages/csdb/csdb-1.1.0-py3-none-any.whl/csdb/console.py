import click
from csdb import session as session_exec
from csdb import productType as productType_exec
from csdb import product as product_exec
import getpass
import datetime
import json
import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def get_env_vars(ctx, args, incomplete):
    return [k for k in os.environ.keys() if incomplete in k]


@click.group()
@click.version_option(version="1.0.0")
def csdb():
    """EP CSDB CLI"""
    pass


@csdb.group()
def session():
    """Session Command"""
    pass


# region session


@session.command()
@click.option("--config-name", prompt="Config Name")
@click.option("--url", prompt="URL")
@click.option("--username", prompt="Username")
def add(config_name, url, username):
    password = getpass.getpass(prompt="Password")
    session_exec.add(config_name, url, username, password)
    click.echo("Config added successfully.")


@session.command()
@click.argument("config_name")
def delete(config_name):
    session_exec.delete(config_name)
    click.echo(f"Config '{config_name}' deleted successfully.")


@session.command()
def list():
    configs = session_exec.list()
    current_config = session_exec.get_current_config()
    for config in configs["config_list"]:
        click.echo(f"Config Name: {config['config_name']}")
        click.echo(f"URL: {config['url']}")
        click.echo(f"Username: {config['username']}")
        click.echo("-----------")

    if current_config:
        click.echo("CUrrent Use: " + current_config["config_name"], color=True)
    else:
        click.echo("no config activated", color=True)


@session.command()
@click.option("--config-name", prompt="Config Name")
@click.option("--url", prompt="URL")
@click.option("--username", prompt="Username")
def update(config_name, url, username):
    password = getpass.getpass(prompt="Password")
    session_exec.modify(config_name, url, username, password)
    click.echo(f"Config '{config_name}' modified successfully.")


@session.command()
@click.argument("config_name")
def use(config_name):
    config = session_exec.use(config_name)
    click.echo(f"Using Config: {config['config_name']}")
    click.echo(f"URL: {config['url']}")
    click.echo(f"Username: {config['username']}")
    click.echo("-----------")


# endregion session


# region product_type
@csdb.group()
def product_type():
    """Product Type Command"""
    # 处理 productType 命令的逻辑
    click.echo("Handling 'productType' command")


@product_type.command()
# flake8: noqa: F811
def list():
    for p in productType_exec.list_product_types():
        click.echo(p)


@product_type.command()
@click.argument("name")
def info(name):
    p = productType_exec.get_product_metadata(name)
    if p:
        click.echo(json.dumps(p, indent=4))

        # Add more details if needed
    else:
        click.echo(f"Product Type {name} does not exist.")


@product_type.command()
@click.argument("name")
def files(name):
    p = productType_exec.list_recent_file(name)
    if len(p) == 0:
        print("No files found")
    for item in p:
        click.echo(item["urn"])


@product_type.command()
@click.argument("product_type_v")
@click.option("-f", "--filter", multiple=True)
def search(product_type_v, filter):
    filters = []
    for f in filter:
        co = None
        name = None
        value = None

        if "=" in f:
            co = "="
            name, value = f.split("=")
        elif ">" in f:
            co = ">"
            name, value = f.split(">")
        elif "<" in f:
            co = "<"
            name, value = f.split("<")
        else:
            raise click.BadParameter(f"Invalid filter format: {f}")

        filters.append({"co": co, "name": name.strip(), "value": value.strip()})

    logging.debug(json.dumps(filters, indent=4))
    logging.debug(product_type_v)

    result = product_exec.adsearch(product_type_v, filters)
    if len(result) == 0:
        print("No result found")
    for item in result:
        print(item["urn"])


# endregion product_type


# region product
@csdb.group
def product():
    pass


@product.command()
@click.argument("urn")
def metadata(urn):
    data = product_exec.get_metadata(urn)
    if data:
        # 日期转化为易读格式
        if "_csdb_upload_time" in data:
            data["_csdb_upload_time_"] = datetime.datetime.fromtimestamp(
                data["_csdb_upload_time"]
            ).strftime("%Y-%m-%d %H:%M:%S")
        if "date" in data and isinstance(data["date"], int):
            # flake8: noqa: E501
            data["date_"] = datetime.datetime.fromtimestamp(
                data["date"] / 1000
            ).strftime("%Y-%m-%d %H:%M:%S")
        click.echo(json.dumps(data, indent=4))
    else:
        click.echo("No files found")


@product.command()
@click.argument("urn")
@click.argument("output")
def download(urn, output):
    product_exec.download(urn, output)


# endregion


def get_command_tree(command):
    if isinstance(command, click.Group):
        command_dict = {"name": command.name, "help": command.help, "subcommands": {}}
        for subcommand_name, subcommand in command.commands.items():
            command_dict["subcommands"][subcommand_name] = get_command_tree(subcommand)
        return command_dict
    elif isinstance(command, click.Command):
        return {"name": command.name, "help": command.help}


@csdb.command
@click.argument("prev", required=False)
@click.argument("cur", required=False)
def autocomp(prev: str, cur: str):
    # 在这里实现根据 `prev` 和 `cur` 生成补全列表的逻辑
    cmd_tree = get_command_tree(csdb)
    prevs = prev.strip().split(" ")[1:]  # 第一项是csdb
    cmd_cursor = cmd_tree

    for cmd in prevs:
        cmd_cursor = cmd_cursor["subcommands"][cmd]
    if "subcommands" in cmd_cursor:
        click.echo("\n".join([cmd for cmd in cmd_cursor["subcommands"]]))
    else:
        pass


if __name__ == "__main__":
    csdb()
