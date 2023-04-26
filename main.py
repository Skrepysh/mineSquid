import os
import shutil
from pathlib import Path
import time
from filerpy import dirdefine
programdir = str(dirdefine("settings.txt", "prog"))
minedir = str(dirdefine("settings.txt", "mine"))
os.chdir(f"{programdir}/mods")
vers = [e for e in os.listdir() if os.path.isdir(e)]


def finish():
    print("окно закроется через 3 секунды")
    time.sleep(3)
    while True:
        break
def main():
    print("Привет!")
    versamount = len(vers)
    for i, item in enumerate(vers):
        print(i + 1, "> ", item)
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
    else:
        selector = int(selector)
        a = vers.pop(selector - 1)
        print("Выбрана версия " + a)
        return a


def worker(version):
    if version == "restok":
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



worker(main())