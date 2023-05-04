import os
import time
from filerpy import pySelector
from tkinter import messagebox

programdir = pySelector.prog_preparator()
minedir = pySelector.mine_preparator()


def error():
    time.sleep(2)
    os.system("cls")


def preparator(type_of_work):
    os.chdir(programdir)
    if type_of_work == "error":
        if not os.path.exists(f"{programdir}/backup"):
            print("Нету папки backup:-(")
            os.mkdir(f"{os.getcwd()}/backup")
            time.sleep(2)
            print("Папка создана, повторите попытку")
            error()
        try:
            if not os.path.exists(f"{minedir}/mods"):
                print("Нету папки mods в директории игры:-(")
                os.chdir(minedir)
                os.mkdir("mods")
                print("Папка создана, повторите попытку")
                error()
        except FileNotFoundError:
            messagebox.showerror(title="Ошибка",
                                 message="Не удалось создать папку mods в корне игры!\nПроверьте paths.py")
            return "stopnow"
        if not os.path.exists(f"{programdir}/mods"):
            print("Отсутствует хранилище модпаков:-(")
            os.chdir(programdir)
            os.mkdir(f"{os.getcwd()}/mods")
            readme = open(f"{os.getcwd()}/mods/readME PLS.txt", "w")
            readme.write("put your modpacks in this folder")
            readme.close()
            print("В корне программы создана папка mods, поместите туда свои модпаки")
            time.sleep(2)
            error()
        else:
            print("hfdsjkhfljka")
            return "stopnow"
    if type_of_work == "init":
        if not os.path.exists(f"{programdir}/backup"):
            print("Нету папки backup:-(")
            os.mkdir(f"{os.getcwd()}/backup")
            time.sleep(2)
            print("Папка создана, повторите попытку")
            error()
        try:
            if not os.path.exists(f"{minedir}/mods"):
                print("Нету папки mods в директории игры:-(")
                os.chdir(minedir)
                os.mkdir("mods")
                print("Папка создана, повторите попытку")
                error()
        except FileNotFoundError:
            messagebox.showerror(title="Ошибка",
                                 message="Не удалось создать папку mods в корне игры!\nПроверьте paths.py")
            return "stopnow"
        if not os.path.exists(f"{programdir}/mods"):
            print("Отсутствует хранилище модпаков:-(")
            os.chdir(programdir)
            os.mkdir(f"{os.getcwd()}/mods")
            readme = open(f"{os.getcwd()}/mods/readME PLS.txt", "w")
            readme.write("put your modpacks in this folder")
            readme.close()
            print("В корне программы создана папка mods, поместите туда свои модпаки")
            time.sleep(2)
            error()
