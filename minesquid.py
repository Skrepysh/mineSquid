import time
from configparser import ConfigParser
import logging
import os
from sys import exit, argv
from shutil import rmtree, copytree
from time import sleep
from progress.bar import Bar
from datetime import datetime
from tkinter import messagebox as msg
from tkinter import filedialog
import requests
from subprocess import Popen


class ZeroSelector(Exception):
    pass


class Restart(Exception):
    pass


class MineSquid:
    def __init__(self, version):
        self.dt = datetime.now()
        self.user_choice = ""
        self.list = []
        self.version = str(version)
        self.game_directory = 'не назначена'
        self.program_directory = os.path.dirname(os.path.abspath(argv[0]))
        self.userappdata = f'{os.environ["appdata"]}\\mineSquid'
        self.config = ConfigParser()
        self.logging = logging
        # noinspection PyGlobalUndefined

    @staticmethod
    def error():
        sleep(0.5)
        os.system("cls")

    @staticmethod
    def finish():
        print("завершение работы...")
        sleep(0.5)
        logging.info("Работа программы завершена")
        exit()

    def enter_path(self):
        while True:
            path = filedialog.askdirectory(initialdir=f'{os.environ["appdata"]}\\.minecraft')
            if path != '':
                return path
            else:
                print("Редактирование отменено")
                time.sleep(1)
                return self.game_directory

    def setup_logger(self):
        if not os.path.exists(f"{self.userappdata}\\logs"):
            os.makedirs(f"{self.userappdata}\\logs")
        logging.basicConfig(level=logging.DEBUG,
                            filename=f"{self.userappdata}\\logs\\{self.dt.hour}_{self.dt.minute}_"
                                     f"{self.dt.second}_at_{self.dt.day}_{self.dt.month}_"
                                     f"{self.dt.year}.log", filemode="w+",
                            format="%(asctime)s #%(levelname)s, %(funcName)s(): %(message)s")

    def read_config(self):
        logging.info("Read_config запущен")
        if not os.path.exists(f"{self.userappdata}"):
            logging.info("Нету папки с данными пользователя")
            os.mkdir(self.userappdata)
            logging.info("Папка создана")
            self.repair_config()
            raise Restart
        if not os.path.exists(f'{self.userappdata}\\config.ini'):
            logging.error("Не найден config.ini!, Запуск repair_config`а")
            self.repair_config()
            raise Restart
        self.config.read(f"{self.userappdata}\\config.ini")
        game_directory = self.config["paths"]["game_path"].replace('"', '').replace('/', '\\')
        logging.info("Конфиг прочитан")
        if game_directory == "default" and os.path.exists(f'{os.environ["appdata"]}\\.minecraft'):
            self.game_directory = f'{os.environ["appdata"]}\\.minecraft'
        elif os.path.exists(game_directory):
            self.game_directory = game_directory
        else:
            pass
        logging.info("Конфиг обработан")

    def checker(self):
        os.chdir(self.program_directory)
        logging.info("Чекер запущен")
        if not os.path.exists(f"{self.userappdata}/backup"):
            logging.warning("Нет папки с бэкапом")
            os.mkdir(rf"{self.userappdata}\backup")
            logging.info("Папка создана")
        if self.game_directory != 'не назначена':
            try:
                if not os.path.exists(f"{self.game_directory}/mods"):
                    logging.warning("Нету папки mods в корне игры")
                    os.mkdir(f"{self.game_directory}/mods")
                    logging.info("Папка создана")
            except FileNotFoundError:
                os.system("cls")
                logging.error("Не удалось создать папку mods в корне игры!")
                msg.showwarning(title="Ошибка",
                                message="Не удалось создать папку mods в корне игры, похоже, указан неверный путь!"
                                        f"\nПроверьте путь к папке с игрой: {self.game_directory}")
                self.edit_config()
                raise Restart
        if not os.path.exists(f"{self.userappdata}/modpacks"):
            logging.warning("Отсутствует хранилище модпаков:-(")
            os.mkdir(f"{self.userappdata}/modpacks")
            logging.info("Хранилище создано")
        if not os.path.exists(f"{self.userappdata}\\config.ini"):
            logging.warning("Конфиг отсутствует!")
            self.repair_config()
            raise Restart
        else:
            pass
        logging.info("Чекер завершил работу")

    def ui(self):
        logging.info("UI запущен")
        print(f"Привет, {os.getlogin()}!")
        print("Версия программы: " + self.version)
        print(f'Путь к папке с игрой: {self.game_directory}')
        print("Список модпаков:  ")
        print("*")
        counter = 1
        if len(self.list) == 0:
            print("Папка модпаков пуста")
            logging.warning('Папка модпаков пуста')
            os.system(f"explorer {self.userappdata}\\modpacks\\")
            logging.info('Открыта папка модпаков в проводнике')
        else:
            logging.info("Список модпаков: ")
            for ver in self.list:
                logging.info(str(counter) + ". " + str(ver))
                print(str(counter) + ". " + str(ver))
                counter += 1
        print("*")
        print("re - восстановление бэкапа\nset - изменить путь к папке с игрой\nupd - обновление программы"
              "\n? - открыть readME\nq - выход")
        logging.info(f"Количество модпаков: {int(counter) - 1}")
        logging.info("Ждем выбора модпака пользователем...")
        selector = str(input("Выберите модпак: "))
        if selector == "re":
            self.restore_backup()
        elif selector == "set":
            print("Редактирование конфига...")
            logging.info("Введена команда set, начат процесс изменения пути к папке с игрой...")
            self.edit_config()
            raise Restart
        elif selector == "upd":
            logging.info('Пользователь ввел upd')
            self.update()
            exit()
        elif selector == "?":
            Popen(f"notepad {self.program_directory}\\readME.txt")
            raise Restart
        elif selector == "q" or selector == "quit":
            logging.info("Пользователь ввел q!")
            self.finish()
        else:
            selector = int(selector)
            if selector == 0:
                logging.error("Пользователь ввел '0'!!!")
                raise ZeroSelector
            else:
                logging.info(f'Пользователь ввел {selector}')
                self.load_modpack(selector - 1)

    def build_list(self):
        if self.game_directory != 'не назначена':
            os.chdir(f"{self.userappdata}\\modpacks")
            self.list = [e for e in os.listdir() if os.path.isdir(e)]
        else:
            self.list = ["Папка с игрой не назначена", "Модпаки недоступны"]
        logging.info("Составлен список модпаков")

    def edit_config(self):
        logging.info('Запущен edit_config')
        logging.info("Начато редактирование config файла")
        self.config.set("paths", "game_path", self.enter_path())
        with open(f"{self.userappdata}\\config.ini", "w") as f:
            self.config.write(f)
        logging.info('Конфиг отредактирован успешно')

    def repair_config(self):
        logging.warning('Запуск восстановление конфига!')
        if os.path.exists(f"{self.userappdata}\\config.ini"):
            os.remove(f"{self.userappdata}\\config.ini")
        else:
            pass
        with open(f"{self.userappdata}\\config.ini", "w") as cfg:
            self.config.add_section("paths")
            self.config.set("paths", "game_path", "default")
            self.config.write(cfg)
        self.edit_config()
        logging.info('Конфиг восстановлен')

    def load_modpack(self, modpack_number):
        if self.game_directory != 'не назначена':
            self.user_choice = self.list[modpack_number]
            print("Выбрана версия " + self.user_choice)
            print("работаю..")
            logging.info("Начата работа над модпаком...")
            pb1 = Bar("Выполнение", max=4, fill='@')
            rmtree(f"{self.userappdata}\\backup")
            logging.info("Удален текущий бэкап")
            pb1.next()
            copytree(f"{self.game_directory}\\mods", f"{self.userappdata}\\backup")
            logging.info("Сделан бэкап текущих модов")
            pb1.next()
            rmtree(f"{self.game_directory}\\mods")
            logging.info("Папка mods удалена")
            pb1.next()
            copytree(f"{self.userappdata}\\modpacks\\{self.user_choice}", f"{self.game_directory}\\mods\\")
            logging.info("Модпак скопирован в папку mods")
            logging.info("ГОТОВО!")
            pb1.next()
            pb1.finish()
            print("готово")
            self.finish()
        else:
            print("Папка с игрой не указана!")
            sleep(1.5)
            raise Restart

    def restore_backup(self):
        if self.game_directory != 'не назначена':
            if len(os.listdir(f"{self.userappdata}\\backup")) == 0:
                print("Бэкап отсутствует, восстанавливать нечего")
                sleep(1)
                raise Restart
            else:
                bob = False
                logging.info("Пользователь запустил восстановление бэкапа")
                pb2 = Bar("Восстановление", max=3, fill='@')
                if os.path.exists(f"{self.game_directory}\\mods"):
                    pb2.next()
                    bob = True
                    copytree(f"{self.game_directory}\\mods", f"{self.userappdata}\\bob", dirs_exist_ok=True)
                    logging.info("Бэкап сделан перед восстановлением бэкапа)")
                    rmtree(f"{self.game_directory}\\mods")
                    logging.info("Папка mods удалена")
                else:
                    pb2.next()
                copytree(f"{self.userappdata}\\backup", f"{self.game_directory}\\mods\\")
                pb2.next()
                if bob:
                    rmtree(f"{self.userappdata}\\backup")
                    os.rename(f"{self.userappdata}\\bob", f"{self.userappdata}\\backup")
                else:
                    pass
                logging.info("Бэкап восстановлен")
                pb2.next()
                pb2.finish()
                print("Бэкап восстановлен")
                self.finish()
        else:
            print("Папка с игрой не указана!")
            sleep(1.5)
            raise Restart

    def update(self):
        logging.info("Начата проверка обновлений...")
        print("Проверка обновлений...")
        try:
            version_url = "https://raw.githubusercontent.com/Skrepysh/mineSquid/master/version.txt"
            version = requests.get(version_url).text.replace('\n', '')
        except Exception:
            print("Не удалось проверить обновления(((\nПроверьте подключение к интернету")
            sleep(1.5)
            raise Restart
        if float(version) > float(self.version):
            print(f"Найдена новая версия программы: {version}")
            logging.info(f"Найдена новая версия программы: {version}!")
            accept = input("Выполнить обновление? Y - да, N - нет: ")
            if accept.lower() == "y":
                logging.info("Обновление подтверждено")
                print("Скачиваю обновление...")
                try:
                    logging.info("Скачивание...")
                    update_url = (f"https://github.com/Skrepysh/mineSquid/releases/download/v{version}"
                                  f"/mineSquid_v{version}_setup.exe")
                    os.chdir(os.environ['temp'])
                    open("mineSquidUpdate.exe", "wb").write(requests.get(update_url, allow_redirects=True).content)
                except Exception:
                    print("Не удалось скачать обновление(((\nПроверьте подключение к интернету")
                    sleep(1.5)
                    raise Restart
                print("Запускаю процесс установки...")
                logging.info("Запускаю процесс установки...")
                if os.path.exists(f'{os.environ["temp"]}\\mineSquidUpdate.exe'):
                    Popen(f'{os.environ["temp"]}\\mineSquidUpdate.exe /Silent')
                else:
                    print("При обновлении произошла ошибка!")
                exit()
            else:
                logging.info("Обновление отменено")
                print("Обновление отменено")
                sleep(1)
                raise Restart
        else:
            logging.info("Обновлений нет")
            print("Обновлений нет")
            sleep(1)
            raise Restart

    def run(self):
        os.chdir(self.userappdata)
        if os.path.exists(f"{self.game_directory}\\tempfiles\\") and self.game_directory != 'не назначена':
            rmtree(f"{self.game_directory}\\tempfiles")
        else:
            pass
        if self.game_directory != 'не назначена':
            os.chdir(self.game_directory)
        else:
            pass
        self.ui()
