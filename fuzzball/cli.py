import yaml
import os
import json
import base64
import random
import string

from pathlib import Path
from shutil import copyfile, move, rmtree
from subprocess import Popen, PIPE
import urllib.request


import click

PROJECT_NAME = "fuzzball"
version = '0.0.1'

context_settings = {"help_option_names": ["-h", "--help"]}

def file_read(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    file_obj = open(path, "rb")
    data = file_obj.read()
    file_obj.close()
    return data


def dir_create(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path)


def dir_exists(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    return os.path.isdir(path)

def init():
    dir_exists(".tmp")
    dir_create(".tmp/artifacts")


def get_artifacts(rec_artifacts):
    for file in rec_artifacts:
        urllib.request.urlretrieve(file, ".tmp/artifacts/" + file.split("/")[-1])


def get_dict_from_ymlfile(path):
    stream = open(path, 'r')
    dict = yaml.load(stream, Loader=yaml.SafeLoader)
    return dict


def renderstates():
    def _getname(line):
        return line.split(b" ")[-1].replace(b'"',b"")

    dir_exists(".tmp/rendering")
    dir_create(".tmp/rendering/jinja")
    dir_create(".tmp/rendering/yaml")
    content = file_read("z_tops/hypertop.fbt")
    lines = content.split(b"\n")

    names = []

    chunk = ""
    inblack = False
    for line in lines:
        if line.startswith(b"!! block"):
            inblack = True
            names.append(_getname(line))
            print("########")
        elif line.startswith(b"!! endblock"):
            inblack = False
        else:
            if not line.startswith(b"!! file"):
                print(line.decode("utf-8"))
            else:
                print("########")
                names.append(_getname(line))
                print(line.decode("utf-8"))
    print(names)


@click.group(context_settings=context_settings)
@click.version_option(prog_name=PROJECT_NAME.capitalize(), version=version)
@click.pass_context
def cli(ctx):
    pass


@cli.command(name="up")
def version_up():
    print("up")
    init()
    config = get_dict_from_ymlfile("z_fussball.fbc")
    artifacts = get_dict_from_ymlfile("z_artifacts/get.fbc")
    get_artifacts(artifacts["required"])
    renderstates()


@cli.command(name="down")
def version_down():
    print("down")


@click.group(name="system")
def system_group():
    return None


@system_group.command(name="version")
def version_command():
    print(version)


@system_group.command(name="selftest")
def selftest_command():
    print("not implemented")


@system_group.command(name="selfcoverage")
def selfcoverage_command():
    print("not implemented")


cli.add_command(system_group)
main = cli
