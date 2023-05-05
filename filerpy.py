import os
import configparser


def version_define(version):
    version = str(version)
    unknown = "unknown"
    if version == "" or version == " ":
        return unknown
    else:
        return version


def config(type):
    config = configparser.ConfigParser()
    config.read("config.ini")
    minedir = config["paths"]["minecraft"]
    programdir = config["paths"]["program"]
    if type == "mine":
        if minedir == "" or not os.path.exists(minedir):
            minedir = "%appdata%/.minecraft"
            return minedir
        else:
            minedir.replace('\\', '/')
            return minedir
    if type == "prog":
        if programdir == "" or not os.path.exists(programdir):
            programdir = os.getcwd()
            return programdir
        else:
            programdir.replace('\\', '/')
            return programdir


class ZeroSelector(Exception):
    pass
