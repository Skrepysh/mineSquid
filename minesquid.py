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
        self.game_directory = ''
        self.program_directory = os.getcwd()
        self.userappdata = f'{os.environ["appdata"]}\\mineSquid'
        self.config = configparser.ConfigParser()
        self.logging = logging
        # noinspection PyGlobalUndefined

    @staticmethod
    def error():
        time.sleep(2)
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
                    inp = ""
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
            logging.error("Не найден config.ini!, Запуск build_config`а")
            self.repair_config()
            raise Restart
        self.config.read(f"{self.userappdata}\\config.ini")
        game_directory = self.config["paths"]["game_path"].replace('"', '').replace('/', '\\')
        logging.info("Конфиг прочитан")
        if game_directory == "" or not os.path.exists(game_directory):
            self.game_directory = f'{os.environ["appdata"]}\\.minecraft'
        else:
            self.game_directory = game_directory
        logging.info("Конфиг обработан")

    def checker(self):
        errs = 0
        os.chdir(self.program_directory)
        logging.info("Чекер запущен")
        if not os.path.exists(f"{self.userappdata}/backup"):
            logging.warning("Нет папки с бэкапом")
            errs += 1
            os.mkdir(rf"{self.userappdata}\backup")
            logging.info("Папка создана")
        try:
            if not os.path.exists(f"{self.game_directory}/mods"):
                errs += 1
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
            errs += 1
            logging.warning("Отсутствует хранилище модпаков:-(")
            os.mkdir(f"{self.userappdata}/modpacks")
            logging.info("Хранилище создано")
        if errs == 0:
            logging.info("Ошибок нет!")
        else:
            logging.warning("Были обнаружены ошибки!")
        logging.info("Чекер завершил работу")

    def ui(self):
        logging.info("UI запущен")
        os.chdir(self.game_directory)
        print("Привет!")
        print("Версия программы: " + self.version)
        print(f'Путь к папке с игрой: {self.game_directory}')
        print("Список модпаков:  ")
        print("*")
        counter = 1
        if len(self.list) == 0:
            print("Папка модпаков пуста\n*")
            logging.warning('Папка модпаков пуста')
            os.system(f"explorer {self.userappdata}\\modpacks\\")
            logging.info('Открыта папка модпаков в проводнике')
            self.finish()
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
        selector = str(input("Выберите версию: "))
        if selector == "re":
            self.restore_backup()
        if selector == "set":
            os.system("cls")
            print("Редактирование конфига...")
            logging.info("Введена команда set, начат процесс изменения пути к папке с игрой...")
            self.edit_config()
            raise Restart
        if selector == "?":
            os.system(f"notepad {self.program_directory}\\readME.txt")
            raise Restart
        if selector == "q" or selector == "quit":
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
        os.chdir(f"{self.userappdata}\\modpacks")
        self.list = [e for e in os.listdir() if os.path.isdir(e)]
        logging.info("Составлен список модпаков")

    def edit_config(self):
        logging.info('Запущен edit_config')
        logging.info("Начато редактирование config файла")
        self.config.set("paths", "game_path", self.enter_path())
        with open(f"{self.userappdata}\\config.ini", "w") as f:
            self.config.write(f)
        logging.info('Конфиг создан успешно')

    def repair_config(self):
        msg.showerror(title="Ошибка конфиг-файла", message="Похоже, config.ini поврежден, "
                                                           "он будет пересоздан")
        if os.path.exists(f"{self.userappdata}\\config.ini"):
            os.remove(f"{self.userappdata}\\config.ini")
        else:
            pass
        with open(f"{self.userappdata}\\config.ini", "w") as cfg:
            self.config.add_section("paths")
            self.config.set("paths", "game_path", "")
            self.config.write(cfg)
        self.edit_config()

    def load_modpack(self, modpack_number, mode="0"):
        if modpack_number > len(self.list) - 1 and mode == "1":
            self.run()
        else:
            pass
        self.user_choice = self.list[modpack_number]
        print("Выбрана версия " + self.user_choice)
        print("работаю..")
        logging.info("Начата работа над модпаком...")
        pb5 = Bar("Выполнение", max=4)
        shutil.rmtree(f"{self.userappdata}\\backup")
        logging.info("Удален текущий бэкап")
        pb5.next()
        shutil.copytree(f"{self.game_directory}\\mods", f"{self.userappdata}\\backup")
        logging.info("Сделан бэкап текущих модов")
        pb5.next()
        shutil.rmtree(f"{self.game_directory}\\mods")
        logging.info("Папка mods удалена")
        pb5.next()
        shutil.copytree(f"{self.userappdata}\\modpacks\\{self.user_choice}", f"{self.game_directory}\\mods\\")
        logging.info("Модпак скопирован в папку mods")
        logging.info("ГОТОВО!")
        pb5.next()
        pb5.finish()
        print("готово")
        self.finish()

    def restore_backup(self):
        logging.info("Пользователь запустил восстановление бэкапа")
        pb4 = Bar("Восстановление", max=2)
        if os.path.exists(f"{self.game_directory}\\mods"):
            shutil.rmtree(f"{self.game_directory}\\mods")
        else:
            pass
        logging.info("Папка mods удалена")
        pb4.next()
        shutil.copytree(f"{self.userappdata}\\backup", f"{self.game_directory}\\mods\\")
        logging.info("Бэкап восстановлен")
        pb4.next()
        pb4.finish()
        print("Бэкап восстановлен")
        self.finish()

    def run(self):
        self.setup_logger()
        if not os.path.exists(f"{self.userappdata}\\config.ini"):
            self.repair_config()
            raise Restart
        else:
            pass
        os.chdir(self.userappdata)
        self.build_list()
        if os.path.exists(f"{self.game_directory}\\tempfiles\\"):
            shutil.rmtree(f"{self.game_directory}\\tempfiles")
        else:
            pass
        self.ui()
