#  ******************************************************
#  Этот скрипт выполнит переименование папки pySelector
#  в mineSquid, если таковая существует
#  ******************************************************
import os
import shutil
import time

path = f"{os.environ['appdata']}"  # ищем папку %AppData%
os.system(r'chcp 65001')
if os.path.exists(f"{path}\\pySelector") and len(os.listdir(f"{path}\\mineSquid\\modpacks")) == 0:  # если имеется папка pySelector,
                                                                                                    # а папка mineSquid/modpacks пуста
    print("Программа была обновлена\nВыполняется перенос данных в новую папку\n"
          "Ждите...")
    shutil.rmtree(f"{path}\\mineSquid")
    shutil.move(f"{path}\\pySelector", f"{path}\\mineSquid")  # перемещаем старые данные в новую папку
    print("Перенос данных завершен")
    time.sleep(2)
else:
    pass
