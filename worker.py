import os
import shutil
import time
from pathlib import Path
from filerpy import pySelector
programdir = pySelector.prog_preparator()
minedir = pySelector.mine_preparator()


def finish(type):
    if type == "error":
        print("Использовать число 0 нельзя!")
        print("окно закроется через 3 секунды")
        time.sleep(3)
        while True:
            break
    if type == "normal":
        print("окно закроется через 3 секунды")
        time.sleep(3)
        while True:
            break


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
        return "restok"
    elif selector == "q" or selector == "quit":
        return "stop_soft"
    else:
        selector = int(selector)
        if selector == 0:
            return "stop"
        else:
            a = vers.pop(selector - 1)
            print("Выбрана версия " + a)
            return a


def worker(version):
    if version == "restok":
        finish("normal")
    elif version == "stop":
        finish("error")
        exit()
    elif version == "stop_soft":
        finish("normal")
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
        finish("normal")
