import os

def dirdefine(file, type):
    if type == "mine":
        minedir1 = open(file, "r")
        minedir = minedir1.readlines()
        minedir1.close()
        result = minedir.pop(0).split("\n")
        result = result.pop(0).split("\n")
        result = result.pop(0)
        return result
    if type == "prog":
        result2 = os.getcwd()
        return result2
def version_define(version):
    version = str(version)
    unknown = "unknown"
    if version == "" or version == " ":
        return unknown
    else:
        return version
