from worker import worker, verpicker, finish
import os
import time
from filerpy import version_define, dirdefine
from preparator import preparator
from preparator import error
programdir = dirdefine("settings.txt", "prog")
minedir = dirdefine("settings.txt", "mine")

def run(version):
    progver = version_define(version)
    if preparator("init") == "stopnow":
        finish("normal")
    else:
        pass
    while True:
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
            time.sleep(3)
            break
