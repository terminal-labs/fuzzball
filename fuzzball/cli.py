import os
import yaml
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

tmp_rendering = ".tmp/rendering"
tmp_artifacts = ".tmp/artifacts"
tmp_jinja = ".tmp/rendering/jinja"
tmp_yaml = ".tmp/rendering/yaml"
conf = "z_fussball.fbc"
arti = "z_artifacts/get.fbc"
conf_hypertop = "z_tops/hypertop.fbt"

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
    dir_create(".tmp")


def download_artifacts(rec_artifacts):
    if not dir_exists(tmp_artifacts):
        dir_create(tmp_artifacts)
        for file in rec_artifacts:
            urllib.request.urlretrieve(file, tmp_artifacts + "/" + file.split("/")[-1])


def get_dict_from_fbcfile(path):
    stream = open(path, 'r')
    dict = yaml.load(stream, Loader=yaml.SafeLoader)
    return dict


def emit_files(names, contents):
    files = list(zip(names, contents))
    for file in files:
        f = open(".tmp/rendering/jinja" + "/" + file[0] + ".jinja", "w")
        f.write(file[1])
        f.close()


def renderstates():
    splitter = "########\n"
    tag_block = "!! block"
    tag_endblock = "!! endblock"
    tag_end = "!! file"
    tag_endend = "!! endfile"

    def _getname(line):
        return line.split(' ')[-1].replace('"','').strip()

    def _tostr(line):
        return line.decode("utf-8")

    def _clean(line):
        return line.replace("\r", "\n")

    def _emit(data):
        pass

    dir_exists(tmp_rendering)
    dir_create(".tmp/rendering/jinja")
    dir_create(".tmp/rendering/yaml")
    content = file_read(conf_hypertop)
    content = _tostr(content)
    lines = content.split("\n")

    names = []
    parse = []

    inblack = False
    for line in lines:
        line = _clean(line)
        if line.startswith(tag_block):
            inblack = True
            names.append(_getname(line))
            _emit(splitter)
            parse.append(splitter)
        elif line.startswith(tag_endblock):
            inblack = False
        else:
            if not line.startswith(tag_end):
                _emit(line)
                parse.append(line)
            else:
                _emit(splitter)
                parse.append(splitter)
                names.append(_getname(line))
                _emit(line)
                parse.append(line)

    parse = ''.join(parse)
    parse = parse.split(splitter)
    parse.remove("")

    return (names, parse)


@click.group(context_settings=context_settings)
@click.version_option(prog_name=PROJECT_NAME.capitalize(), version=version)
@click.pass_context
def cli(ctx):
    pass


@cli.command(name="up")
def version_up():
    init()
    config = get_dict_from_fbcfile(conf)
    artifacts = get_dict_from_fbcfile(arti)
    download_artifacts(artifacts["required"])
    chunks = renderstates()
    emit_files(chunks[0], chunks[1])


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
