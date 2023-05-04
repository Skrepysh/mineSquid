import os
from paths import minedir, programdir


def version_define(version):
    version = str(version)
    unknown = "unknown"
    if version == "" or version == " ":
        return unknown
    else:
        return version


class prep:
    def __init__(self, minedirectory, programdirectory):
        self.minedir = minedirectory
        self.programdir = programdirectory

    def mine_preparator(self):
        if self.minedir == "" or not os.path.exists(self.minedir):
            self.minedir = "%appdata%/.minecraft"
            return self.minedir
        else:
            minedir.replace('\\', '/')
            return self.minedir

    def prog_preparator(self):
        if self.programdir == "" or not os.path.exists(self.programdir):
            self.programdir = os.getcwd()
            return self.programdir
        else:
            return self.programdir


pySelector = prep(minedir, programdir)
