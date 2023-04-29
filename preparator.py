import os
import time
from filerpy import dirdefine
programdir = dirdefine("settings.txt", "prog")
minedir = dirdefine("settings.txt", "mine")

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
            print("Не удалось создать папку!\nПроверьте settings.txt")
            time.sleep(2)
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
            print("Какой-то файл/папка не найден.\nПроверьте settings.txt")
            time.sleep(2)
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
            print("Не удалось создать папку!\nПроверьте settings.txt")
            time.sleep(2)
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

