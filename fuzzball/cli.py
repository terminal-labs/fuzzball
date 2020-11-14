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
    dir_exists(".tmp/rendering")
    dir_create(".tmp/rendering/jinja")
    dir_create(".tmp/rendering/yaml")


@click.group(context_settings=context_settings)
@click.version_option(prog_name=PROJECT_NAME.capitalize(), version=version)
@click.pass_context
def cli(ctx):
    pass


@cli.command(name="up")
def version_up():
    print("up")
    init()
    config = get_dict_from_ymlfile("z_fussball.yml")
    artifacts = get_dict_from_ymlfile("z_artifacts/get.yml")
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
