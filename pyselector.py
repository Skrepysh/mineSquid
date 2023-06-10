import configparser
import logging
import os
import shutil
import time
from pathlib import Path
from tkinter import messagebox as msg
from sys import exit


def error():
    time.sleep(2)
    os.system("cls")


class ZeroSelector(Exception):
    pass


def version_define(version):
    version = str(version)
    unknown = "unknown"
    if version == "" or version == " ":
        return unknown
    else:
        return version


def config(type):
    settings = configparser.ConfigParser()
    settings.read("config.ini")
    game_directory = settings["paths"]["minecraft"]
    program_directory = settings["paths"]["program"]
    if type == "mine":
        if game_directory == "" or not os.path.exists(game_directory):
            print(game_directory)
            print(os.path.exists(game_directory))
            game_directory = "%appdata%/.minecraft"
            return game_directory
        else:
            return game_directory
    if type == "prog":
        if program_directory == "" or not os.path.exists(program_directory):
            program_directory = os.getcwd()
            return program_directory
        else:
            return program_directory


programdir = config("prog")
minedir = config("mine")
os.chdir(f"{programdir}\mods")
version_list = [e for e in os.listdir() if os.path.isdir(e)]


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
            os.system("cls")
            msg.showerror(title="Ошибка",
                          message="Не удалось создать папку mods в корне игры!\nПроверьте config.ini")
            os.system(f"notepad {programdir}/config.ini")
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
            os.system("cls")
            msg.showerror(title="Ошибка",
                          message="Не удалось создать папку mods в корне игры!\nПроверьте config.ini")
            os.system(f"notepad {programdir}/config.ini")
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


def finish():
    print("завершение работы...")
    time.sleep(1)
    exit()


def verpicker(progver, vers_list):
    print("Привет!")
    print("Версия программы: " + progver)
    print("Список модпаков:  ")
    counter = 1
    divider = ". "
    for ver in vers_list:
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
            a = vers_list.pop(selector - 1)
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


def run(version):
    progver = version_define(version)
    while True:
        try:
            if preparator("init") == "stopnow":
                break
            else:
                pass
            os.chdir(f"{programdir}/mods")
            worker(verpicker(progver, version_list))
            break
        except IndexError:
            print("неверное значение\nперезапуск")
            error()
        except PermissionError:
            msg.showerror(title="Ошибка доступа", message="Произошло повреждение файлов программы."
                                                          "\nНеобходимо произвести запуск от имени администратора!")
            exit()
        except OverflowError:
            print("многацифер\nперезапуск")
            error()
        except ZeroSelector:
            print("неверное значение\nперезапуск")
            error()
        except ValueError:
            print("что ты несешь\nперезапуск")
            error()
        except SyntaxError:
            print("Что-то пошло не так!")
        except FileNotFoundError:
            if preparator("error") == "stopnow":
                break
            else:
                os.system("cls")
                continue
        except Exception as err:
            os.system("cls")
            print("неизвестная ошибка")
            print("Сообщите разработчику следующий код ошибки:")
            logging.error(err, exc_info=True)
            time.sleep(7)
            break
