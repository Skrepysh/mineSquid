import os
import shutil
import time
from pathlib import Path
from filerpy import ZeroSelector
from filerpy import config
from sys import exit
programdir = config("prog")
minedir = config("mine")


def finish():
    print("завершение работы...")
    time.sleep(1)
    exit()


def verpicker(progver, vers):
    print("Привет!")
    print("Версия программы: " + progver)
    print("Список модпаков:  ")
    counter = 1
    divider = ". "
    for ver in vers:
        print(str(counter) + str(divider) + str(ver))
        counter += 1
    print("Чтобы восстановить бэкап напишите restore")
    selector = str(input("Выберите версию: "))
    if selector == "restore":
        os.chdir(minedir)
        shutil.rmtree(f"{minedir}/mods")
        os.chdir(programdir)
        shutil.copytree(f"{programdir}/backup", f"{minedir}/pySelector/")
        os.chdir(minedir)
        p = Path(f"{minedir}/pySelector/")
        p.rename("mods")
        print("Бэкап восстановлен")
        return "restored"
    elif selector == "q" or selector == "quit":
        return "quit"
    else:
        selector = int(selector)
        if selector == 0:
            raise ZeroSelector
        else:
            a = vers.pop(selector - 1)
            print("Выбрана версия " + a)
            return a


def worker(version):
    if version == "restored":
        finish()
    if version == "quit":
        finish()
    else:
        print("работаю..")
        os.chdir(minedir)
        shutil.rmtree(f"{programdir}/backup")
        shutil.copytree(f"{minedir}/mods", f"{programdir}/backup")
        shutil.rmtree(f"{minedir}/mods")
        os.chdir(f"{programdir}/mods/")
        shutil.copytree(f"{programdir}/mods/{version}", f"{minedir}/pySelector")
        os.chdir(minedir)
        p = Path(f"{minedir}/pySelector/")
        p.rename("mods")
        print("готово")
        finish()
