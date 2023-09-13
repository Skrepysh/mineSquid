import configparser
import logging
import os
import sys
import shutil
import time
from progress.bar import Bar
import datetime as dt
from tkinter import messagebox as msg


class ZeroSelector(Exception):
    pass


class Restart(Exception):
    pass


class MineSquid:
    def __init__(self, version):
        self.dt = dt.datetime.now()
        self.user_choice = ""
        self.list = []
        self.version = str(version)
        self.game_directory = 'не назначена'
        self.program_directory = os.getcwd()
        self.userappdata = f'{os.environ["appdata"]}\\mineSquid'
        self.config = configparser.ConfigParser()
        self.logging = logging
        # noinspection PyGlobalUndefined

    @staticmethod
    def error():
        time.sleep(1.5)
        os.system("cls")

    @staticmethod
    def finish():
        print("завершение работы...")
        time.sleep(1)
        logging.info("Работа программы завершена")
        sys.exit()

    def enter_path(self):
        logging.info("Запущен enter_path!")
        while True:
            logging.info("Запрашиваем путь к папке с игрой")
            print("Не вводите ничего, чтобы использовать стандартный путь %appdata%/.minecraft\nc - отмена")
            inp = str(input("Введите путь к папке с игрой: "))
            logging.info(f"Пользователь ввел {inp}")
            inp = inp.replace('"', '')
            if inp.replace(" ", "") == "":
                if os.path.exists(f'{os.environ["appdata"]}\\.minecraft'):
                    inp = "default"
                    logging.info("Выбран стандартный путь %appdata%/.minecraft")
                    print("Выбран стандартный путь %appdata%/.minecraft")
                    break
                else:
                    print("Ooooops! Стандартный путь не существует, выберите другой!\n*******")
            elif inp.lower() == "c":
                print("Редактирование отменено")
                inp = self.game_directory
                break
            elif not os.path.exists(inp):
                print("Путь не существует!\n*******")
                logging.info("Ooooops! Путь не существует")
            else:
                logging.info("Введен действительный путь")
                print("Введен действительный путь")
                break
        time.sleep(1)
        os.system("cls")
        return str(inp)

    def setup_logger(self, mode=0):
        if not os.path.exists(f"{self.userappdata}\\logs"):
            os.makedirs(f"{self.userappdata}\\logs")
        if mode == 0:
            logging.basicConfig(level=logging.DEBUG,
                                filename=f"{self.userappdata}\\logs\\{self.dt.hour}_{self.dt.minute}_"
                                         f"{self.dt.second}_at_{self.dt.day}_{self.dt.month}_"
                                         f"{self.dt.year}.log", filemode="w+",
                                format="%(asctime)s #%(levelname)s: %(message)s")
        else:
            logging.basicConfig(level=logging.DEBUG,
                                format="%(asctime)s #%(levelname)s: %(message)s")

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
        logging.info("Чекер завершил работу")

    def ui(self):
        logging.info("UI запущен")
        print("Привет!")
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
        print("re - восстановление бэкапа\nset - изменить путь к папке с игрой\n? - открыть readME\nq - выход")
        logging.info(f"Количество модпаков: {int(counter) - 1}")
        logging.info("Ждем выбора модпака пользователем...")
        selector = str(input("Выберите модпак: "))
        if selector == "re":
            self.restore_backup()
        elif selector == "set":
            os.system("cls")
            print("Редактирование конфига...")
            logging.info("Введена команда set, начат процесс изменения пути к папке с игрой...")
            self.edit_config()
            raise Restart
        elif selector == "?":
            os.system(f"notepad {self.program_directory}\\readME.txt")
            raise Restart
        elif selector == "q" or selector == "quit":
            logging.info("Пользователь ввел команду q!")
            self.finish()
        else:
            selector = int(selector)
            if selector == 0:
                logging.error("Пользователь ввел '0'!!!")
                raise ZeroSelector
            else:
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
        logging.info('Конфиг создан успешно')

    def repair_config(self):
        if os.path.exists(f"{self.userappdata}\\config.ini"):
            os.remove(f"{self.userappdata}\\config.ini")
        else:
            pass
        with open(f"{self.userappdata}\\config.ini", "w") as cfg:
            self.config.add_section("paths")
            self.config.set("paths", "game_path", "default")
            self.config.write(cfg)
        self.edit_config()

    def load_modpack(self, modpack_number, mode="0"):
        if self.game_directory != 'не назначена':
            if modpack_number > len(self.list) - 1 and mode == "1":
                self.run()
            else:
                pass
            self.user_choice = self.list[modpack_number]
            print("Выбрана версия " + self.user_choice)
            print("работаю..")
            logging.info("Начата работа над модпаком...")
            pb1 = Bar("Выполнение", max=4, fill='@')
            shutil.rmtree(f"{self.userappdata}\\backup")
            logging.info("Удален текущий бэкап")
            pb1.next()
            shutil.copytree(f"{self.game_directory}\\mods", f"{self.userappdata}\\backup")
            logging.info("Сделан бэкап текущих модов")
            pb1.next()
            shutil.rmtree(f"{self.game_directory}\\mods")
            logging.info("Папка mods удалена")
            pb1.next()
            shutil.copytree(f"{self.userappdata}\\modpacks\\{self.user_choice}", f"{self.game_directory}\\mods\\")
            logging.info("Модпак скопирован в папку mods")
            logging.info("ГОТОВО!")
            pb1.next()
            pb1.finish()
            print("готово")
            self.finish()
        else:
            print("Папка с игрой не указана!")
            time.sleep(1.5)
            raise Restart

    def restore_backup(self):
        if self.game_directory != 'не назначена':
            bob = False
            logging.info("Пользователь запустил восстановление бэкапа")
            pb2 = Bar("Восстановление", max=3, fill='@')
            if os.path.exists(f"{self.game_directory}\\mods"):
                pb2.next()
                bob = True
                shutil.copytree(f"{self.game_directory}\\mods", f"{self.userappdata}\\bob", dirs_exist_ok=True)
                logging.info("Бэкап сделан перед восстановлением бэкапа)")
                shutil.rmtree(f"{self.game_directory}\\mods")
                logging.info("Папка mods удалена")
            else:
                pb2.next()
            shutil.copytree(f"{self.userappdata}\\backup", f"{self.game_directory}\\mods\\")
            pb2.next()
            if bob:
                shutil.rmtree(f"{self.userappdata}\\backup")
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
            time.sleep(1.5)
            raise Restart

    def run(self):
        if not os.path.exists(f"{self.userappdata}\\config.ini"):
            self.repair_config()
            raise Restart
        else:
            pass
        os.chdir(self.userappdata)
        self.build_list()
        if os.path.exists(f"{self.game_directory}\\tempfiles\\") and self.game_directory != 'не назначена':
            shutil.rmtree(f"{self.game_directory}\\tempfiles")
        else:
            pass
        if self.game_directory != 'не назначена':
            os.chdir(self.game_directory)
        else:
            pass
        self.ui()
