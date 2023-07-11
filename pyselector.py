import configparser
import logging
import os
import sys
import shutil
import time
from progress.bar import Bar
import datetime as dt
from tkinter import messagebox as msg
from sys import exit


class ZeroSelector(Exception):
    pass


class PySelector:
    def __init__(self, version):
        self.dt = dt.datetime.now()
        self.user_choice = "ОШИБКА"
        self.list = ["ОШИБКА!", "УДАЛИТЕ ЭТУ ВЕРСИЮ ПРОГРАММЫ!!!"]
        self.configfile_name = 'config'
        self.version = str(version)
        self.game_directory = "%appdata%/.minecraft"
        self.program_directory = os.getcwd()
        self.userappdata = f'{os.environ["appdata"]}\\pySelector'
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

    def setup_logger(self, mode=0):
        if not os.path.exists(f"{self.userappdata}\\logs"):
            os.makedirs(f"{self.userappdata}\\logs")
        if mode == 0:
            logging.basicConfig(level=logging.DEBUG,
                                filename=f"{self.userappdata}\\logs\\{self.dt.hour}_{self.dt.minute}_"
                                         f"{self.dt.second}_at_{self.dt.day}_{self.dt.month}_"
                                         f"{self.dt.year}.log", filemode="w",
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
            self.build_config()
        if not os.path.exists(f'{self.userappdata}\\config.ini'):
            logging.error("Не найден config.ini!, Запуск build_config`а")
            self.build_config()

        os.chdir(self.userappdata)
        settings = configparser.ConfigParser()
        settings.read(f"{self.configfile_name}.ini")
        game_directory = settings["paths"]["minecraft"].replace('"', '').replace('/', '\\')
        program_directory = settings["paths"]["program"].replace('"', '').replace('/', '\\')
        logging.info("Конфиг прочитан")
        if game_directory == "" or not os.path.exists(game_directory):
            pass
        else:
            self.game_directory = game_directory
        if program_directory == "" or not os.path.exists(program_directory):
            pass
        else:
            self.program_directory = program_directory
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
                                    "\nПроверьте config.ini")
            os.system(f"notepad {self.userappdata}/config.ini")
            logging.info("Конфиг открыт в блокноте")
            sys.exit()
        if not os.path.exists(f"{self.userappdata}/modpacks"):
            errs += 1
            logging.warning("Отсутствует хранилище модпаков:-(")
            os.mkdir(f"{self.userappdata}/modpacks")
            logging.info("Хранилище создано")
            readme = open(f"{self.userappdata}/modpacks/readME PLS.txt", "w")
            readme.write("put your modpacks in this folder")
            readme.close()
            logging.info("Readme создан")
        if errs == 0:
            logging.info("Ошибок нет!")
        else:
            logging.warning("Были обнаружены ошибки!")
        errs = 0
        logging.info("Чекер завершил работу")

    def ui(self):
        logging.info("UI запущен")
        os.chdir(self.game_directory)
        print("Привет!")
        print("Версия программы: " + self.version)
        print("Список модпаков:  ")
        print("*")
        counter = 1
        divider = ". "
        if len(self.list) == 0:
            print("Папка модпаков пуста\n*")
            logging.warning('Папка модпаков пуста')
            os.system(f"explorer {self.userappdata}\\modpacks\\")
            logging.info('Открыта папка модпаков в проводнике')
            self.finish()
        else:
            logging.info("Список модпаков: ")
            for ver in self.list:
                logging.info(str(counter) + str(divider) + str(ver))
                print(str(counter) + str(divider) + str(ver))
                counter += 1
        print("*")
        logging.info(f"Количество модпаков: {int(counter) - 1}")
        print("Чтобы восстановить бэкап напишите restore")
        logging.info("Ждем выбора модпака пользователем...")
        selector = str(input("Выберите версию: "))
        if selector == "restore":
            self.restore_backup()
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

    def build_config(self):
        logging.info('Запущен build_config')
        file = open(f"{self.userappdata}\\config.ini", "w")
        file.write(
            '[paths]\n; write path to minecraft folder below (%appdata%/.minecraft if not filled)\nminecraft = \n'
            '; do not use parameter below, if do not know, what are you doing!!!!\nprogram = ')
        file.close()
        logging.info('Конфиг создан успешно')
        msg.showinfo(title="Привет!",
                     message='Ты запустил эту программу в первый раз, и ее надо настроить. Проверь config.ini!')
        logging.info('Конфиг открыт в блокноте')
        os.system(f"notepad {self.userappdata}/config.ini")

    def devmode(self):
        self.setup_logger(mode=1)
        logging.info("Запущен devmode!!")
        while True:
            devm = str(input(">>>"))
            if devm == "0":
                self.finish()
            if devm == "1":
                logging.warning("Запущено принудительное восстановление конфига")
                self.build_config()
            if devm == "2":
                self.read_config()
                print(f'Путь к программе: {self.program_directory}')
                print(f'Путь к игре: {self.game_directory}')
                print(f'Путь к папке с пользовательскими данными: {self.userappdata}')
                input("<<<")
            if devm == "3":
                logging.warning("Принудительный запуск чекера!")
                self.read_config()
                self.checker()
            if devm == "4":
                confirm1 = input("?>")
                if confirm1 == "yes":
                    shutil.rmtree(f"{self.userappdata}\\logs")
                    shutil.rmtree(f"{self.userappdata}\\backup")
                    os.mkdir(f"{self.userappdata}\\logs")
                    os.mkdir(f"{self.userappdata}\\backup")
                    logging.warning("Выполнена принудительная очистка папок с логами и бэкапом!!!")
                else:
                    pass
            if devm == "5":
                confirm2 = input("?>")
                if confirm2 == "yes":
                    shutil.rmtree(f"{self.userappdata}\\modpacks")
                    os.mkdir(f"{self.userappdata}\\modpacks")
                    logging.warning("Выполнена принудительная очистка папки с модпаками!!!")
                else:
                    pass
            if devm == "6":
                confirm3 = input("?>")
                if confirm3 == "1":
                    shutil.rmtree(f"{self.userappdata}\\modpacks")
                    logging.warning("Папка модпаков удалена!")
                if confirm3 == "2":
                    shutil.rmtree(f"{self.userappdata}\\backup")
                    logging.warning("Папка с бэкапом удалена!")
                if confirm3 == "3":
                    shutil.rmtree(f"{self.userappdata}\\logs")
                    logging.warning("Папка с логами удалена!")
                else:
                    pass
            if devm == "7":
                confirm4 = input("?>")
                if confirm4 == "yes":
                    os.chdir(os.environ["appdata"])
                    shutil.rmtree("pySelector")
                    logging.info("Папка с данными пользователя удалена!")
                else:
                    pass

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
        while True:
            try:
                self.setup_logger()
                logging.info(f'Версия программы: {self.version}')
                if not os.path.exists(f"{self.userappdata}\\config.ini"):
                    self.build_config()
                else:
                    pass
                os.chdir(self.userappdata)
                self.read_config()
                self.build_list()
                self.checker()
                logging.info(f'Путь к программе: {self.program_directory}')
                logging.info(f'Путь к игре: {self.game_directory}')
                logging.info(f'Путь к папке с пользовательскими данными: {self.userappdata}')
                if os.path.exists(f"{self.game_directory}\\tempfiles\\"):
                    shutil.rmtree(f"{self.game_directory}\\tempfiles")
                else:
                    pass
                self.ui()
            except IndexError as err:
                logging.error("IndexError")
                logging.exception(err)
                print("неверное значение\nперезапуск")
                self.error()
            except PermissionError as err:
                logging.error("PermissionError")
                logging.exception(err)
                msg.showerror(title="Ошибка доступа", message="Не удается получить доступ к какому-то файлу."
                                                              "\nПопробуйте произвести запуск от имени администратора!")
                exit()
            except OverflowError as err:
                logging.error("OverflowError")
                logging.exception(err)
                print("многацифер\nперезапуск")
                self.error()
            except ZeroSelector as err:
                logging.error("ZeroSelector")
                logging.exception(err)
                print("неверное значение\nперезапуск")
                self.error()
            except ValueError as err:
                logging.error("ValueError")
                logging.exception(err)
                print("неверное значение\nперезапуск")
                self.error()
            except FileNotFoundError as err:
                logging.error("FileNotFoundError")
                logging.exception(err)
                logging.error("FileNotFoundError, запуск чекера")
                self.checker()
                self.finish()
            except Exception as err:
                os.system("cls")
                logging.error("Неизвестная ошибка!!")
                print("неизвестная ошибка, смотри логи")
                logging.exception(err)
                time.sleep(7)
                break
