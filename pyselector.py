import configparser
import logging
import os
import sys
import shutil
import time
from progress.bar import Bar
from pathlib import Path
from tkinter import messagebox as msg
from sys import exit


def finish():
    print("завершение работы...")
    time.sleep(1)
    sys.exit()


def error():
    time.sleep(2)
    os.system("cls")


userappdata = f'{os.environ["appdata"]}\\pySelector'
if not os.path.exists(f"{userappdata}"):
    os.mkdir(userappdata)
    file = open(f"{userappdata}\\config.ini", "w+")
    file.write('[paths]\n; write path to minecraft folder below (%appdata%/.minecraft if not filled)\nminecraft = \n'
               '; do not use parameter below, if do not know, what are you doing\nprogram =')
    file.close()
    msg.showerror(title="Файлы были повреждены!",
                  message="Файлы программы были повреждены! Восстановление завершено успешно, перезапуск программы...")
    error()


class ZeroSelector(Exception):
    pass


def version_define(version):
    version = str(version)
    if version == "" or version == " ":
        return "DEV Build"
    else:
        return version


def config(type_of_work):
    os.chdir(userappdata)
    settings = configparser.ConfigParser()
    settings.read("config.ini")
    game_directory = settings["paths"]["minecraft"].replace('"', '')
    program_directory = settings["paths"]["program"].replace('"', '')
    if type_of_work == "mine":
        if game_directory == "" or not os.path.exists(game_directory):
            game_directory = "%appdata%/.minecraft"
            return game_directory
        else:
            return game_directory
    if type_of_work == "prog":
        if program_directory == "" or not os.path.exists(program_directory):
            program_directory = os.getcwd()
            return program_directory
        else:
            return program_directory


programdir = config("prog")
minedir = config("mine")


def preparator(type_of_work):
    os.chdir(programdir)
    if not os.path.exists(f"{userappdata}/backup"):
        os.mkdir(rf"{userappdata}\backup")
        error()
    try:
        if not os.path.exists(f"{minedir}/mods"):
            os.mkdir(f"{minedir}/mods")
            error()
    except FileNotFoundError:
        os.system("cls")
        msg.showwarning(title="Ошибка",
                        message="Не удалось создать папку mods в корне игры!\nПроверьте config.ini")
        os.system(f"notepad {programdir}/config.ini")
        return "stopnow"
    if not os.path.exists(f"{userappdata}/modpacks"):
        print("Отсутствует хранилище модпаков:-(")
        pb1 = Bar("Создание", max=2)  # прогрессбар для создания папки с модпаками
        os.mkdir(f"{userappdata}/modpacks")
        pb1.next()
        readme = open(f"{userappdata}/modpacks/readME PLS.txt", "w")
        readme.write("put your modpacks in this folder")
        readme.close()
        pb1.next()
        pb1.finish()
        print("В корне программы создана папка modpacks, поместите туда свои модпаки")
        error()
    else:
        if type_of_work == "init":
            pass
        if type_of_work == "error":
            return "stopnow"


def worker(progver):
    os.chdir(f"{userappdata}\\modpacks\\")
    vers_list = [e for e in os.listdir() if os.path.isdir(e)]
    os.chdir(minedir)
    print("Привет!")
    print("Версия программы: " + progver)
    print("Список модпаков:  ")
    print("*")
    counter = 1
    divider = ". "
    if len(vers_list) == 0:
        print("Папка модпаков пуста\n*")
        os.system(f"explorer {userappdata}\\modpacks\\")
        finish()
    else:
        for ver in vers_list:
            print(str(counter) + str(divider) + str(ver))
            counter += 1
    print("*")
    print("Чтобы восстановить бэкап напишите restore")
    selector = str(input("Выберите версию: "))
    if selector == "restore":
        pb4 = Bar("Восстановление", max=3)
        shutil.rmtree(f"{minedir}\\mods")
        pb4.next()
        shutil.copytree(f"{userappdata}\\backup", f"{minedir}\\tempfiles\\")
        pb4.next()
        p = Path(f"{minedir}\\tempfiles\\")
        p.rename("mods")
        pb4.next()
        pb4.finish()
        print("Бэкап восстановлен")
        finish()
    elif selector == "q" or selector == "quit":
        finish()
    else:
        selector = int(selector)
        if selector == 0:
            raise ZeroSelector
        else:
            user_choice = vers_list.pop(selector - 1)
            print("Выбрана версия " + user_choice)
            print("работаю..")
            pb5 = Bar("Выполнение", max=5)
            shutil.rmtree(f"{userappdata}\\backup")
            pb5.next()
            shutil.copytree(f"{minedir}\\mods", f"{userappdata}\\backup")
            pb5.next()
            shutil.rmtree(f"{minedir}\\mods")
            pb5.next()
            shutil.copytree(f"{userappdata}\\modpacks\\{user_choice}", f"{minedir}\\tempfiles\\")
            pb5.next()
            p = Path(f"{minedir}\\tempfiles\\")
            p.rename("mods")
            pb5.next()
            pb5.finish()
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
            if os.path.exists(f"{minedir}\\tempfiles\\"):
                shutil.rmtree(f"{minedir}\\tempfiles")
            else:
                pass
            os.chdir(f"{userappdata}/modpacks")
            worker(progver)
        except IndexError:
            print("неверное значение\nперезапуск")
            error()
        except PermissionError:
            msg.showerror(title="Ошибка доступа", message="Не удается получить доступ к какому-то файлу."
                                                          "\nПопробуйте произвести запуск от имени администратора!")
            exit()
        except OverflowError:
            print("многацифер\nперезапуск")
            error()
        except ZeroSelector:
            print("неверное значение\nперезапуск")
            error()
        except ValueError:
            print("неверное значение\nперезапуск")
            error()
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
