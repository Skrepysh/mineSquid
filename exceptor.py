import os
from tkinter import messagebox
from filerpy import pySelector
from filerpy import version_define
from preparator import error
from preparator import preparator
from worker import worker, verpicker

programdir = pySelector.prog_preparator()
minedir = pySelector.mine_preparator()


def run(version):
    progver = version_define(version)
    while True:
        if preparator("init") == "stopnow":
            break
        else:
            pass
        try:
            os.chdir(f"{programdir}/mods")
            vers = [e for e in os.listdir() if os.path.isdir(e)]
            worker(verpicker(progver, vers))
            break
        except IndexError:
            print("неверное значение\nперезапуск")
            error()
        except OverflowError:
            print("многацифер\nперезапуск")
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
        except Exception:
            print("неизвестная ошибка")
            messagebox.showerror(title="Ошибка", message="Неизвестная ошибка")
            break
