import logging
import os
import time
from filerpy import ZeroSelector, version_define, config
from preparator import error
from preparator import preparator
from worker import worker, verpicker
from tkinter import messagebox as msg

programdir = config("prog")
minedir = config("mine")


def run(version):
    progver = version_define(version)
    while True:
        try:
            if preparator("init") == "stopnow":
                break
            else:
                pass
            os.chdir(f"{programdir}/mods")
            vers = [e for e in os.listdir() if os.path.isdir(e)]
            worker(verpicker(progver, vers))
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
            print("неизвестная ошибка")
            print("Сообщите разработчику следующий код ошибки:")
            logging.error(err, exc_info=True)
            time.sleep(7)
            break
