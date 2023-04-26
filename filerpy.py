import os


def dirdefine(file, type):
    if type == "mine":
        minedir1 = open(file, "r")
        minedir = minedir1.readlines()
        minedir1.close()
        ok = minedir.pop(0).split("\n")
        ok = ok.pop(0).split("\n")
        ok = ok.pop(0)
        return ok
    if type == "prog":
        programdir1 = open(file, "r")
        programdir = programdir1.readlines()
        programdir1.close()
        ok2 = programdir.pop(1).split("/n")
        ok2 = ok2.pop(0).split("\n")
        ok2 = ok2.pop(0)
        return ok2