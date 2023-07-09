import configparser
import logging
import os
import sys
import shutil
import time
from progress.bar import Bar
from pathlib import Path
import datetime as dt
from tkinter import messagebox as msg
from sys import exit


class ZeroSelector(Exception):
    pass


class PySelector:
    def __init__(self, version):
        self.dt = dt.datetime.now()
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

    def setup_logger(self):
        if not os.path.exists(f"{self.userappdata}\\logs"):
            os.mkdir(f"{self.userappdata}\\logs")
        logging.basicConfig(level=logging.DEBUG, filename=f"{self.userappdata}\\logs\\{self.dt.hour}_{self.dt.minute}_"
                                                          f"{self.dt.second}_at_{self.dt.day}_{self.dt.month}_"
                                                          f"{self.dt.year}.log", filemode="w",
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
        os.chdir(self.program_directory)
        logging.info("Чекер запущен")
        if not os.path.exists(f"{self.userappdata}/backup"):
            logging.warning("Нет папки с бэкапом")
            os.mkdir(rf"{self.userappdata}\backup")
            logging.info("Папка создана")
            self.error()
        try:
            if not os.path.exists(f"{self.game_directory}/mods"):
                logging.warning("Нету папки mods в корне игры")
                os.mkdir(f"{self.game_directory}/mods")
                logging.info("Папка создана")
                self.error()
        except FileNotFoundError:
            os.system("cls")
            logging.error("Не удалось создать папку mods в корне игры!")
            msg.showwarning(title="Ошибка",
                            message="Не удалось создать папку mods в корне игры!\nПроверьте config.ini")
            os.system(f"notepad {self.userappdata}/config.ini")
            logging.info("Конфиг открыт в блокноте")
            sys.exit()
        if not os.path.exists(f"{self.userappdata}/modpacks"):
            print("Отсутствует хранилище модпаков:-(")
            logging.warning("Отсутствует хранилище модпаков:-(")
            pb1 = Bar("Создание", max=2)  # прогрессбар для создания папки с модпаками
            os.mkdir(f"{self.userappdata}/modpacks")
            logging.info("Хранилище создано")
            pb1.next()
            readme = open(f"{self.userappdata}/modpacks/readME PLS.txt", "w")
            readme.write("put your modpacks in this folder")
            readme.close()
            logging.info("Readme создан")
            pb1.next()
            pb1.finish()
            print("В корне программы создана папка modpacks, поместите туда свои модпаки")
            self.error()
        logging.info("Чекер завершил работу")

    def worker(self):
        logging.info("Worker запущен")
        os.chdir(f"{self.userappdata}\\modpacks\\")
        self.list = [e for e in os.listdir() if os.path.isdir(e)]
        logging.info("Составлен список модпаков", )
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
        logging.info(f"Количество модпаков: {str(counter)}")
        print("Чтобы восстановить бэкап напишите restore")
        logging.info("Ждем выбора модпака пользователем...")
        selector = str(input("Выберите версию: "))
        if selector == "restore":
            logging.info("Пользователь запустил восстановление бэкапа")
            pb4 = Bar("Восстановление", max=3)
            shutil.rmtree(f"{self.game_directory}\\mods")
            logging.info("Папка mods удалена")
            pb4.next()
            shutil.copytree(f"{self.userappdata}\\backup", f"{self.game_directory}\\tempfiles\\")
            logging.info("Бэкап скопирован во временную папку")
            pb4.next()
            p = Path(f"{self.game_directory}\\tempfiles\\")
            p.rename("mods")
            logging.info("Папка переименована в mods, бэкап восстановлен")
            pb4.next()
            pb4.finish()
            print("Бэкап восстановлен")
            self.finish()
        elif selector == "q" or selector == "quit":
            logging.info("Пользователь ввел команду q!")
            self.finish()
        else:
            selector = int(selector)
            if selector == 0:
                logging.error("Пользователь ввел '0'!!!")
                raise ZeroSelector
            else:
                user_choice = self.list.pop(selector - 1)
                logging.info(f"Пользователь выбрал модпак: {selector} ___ Имя модпака: {user_choice}")
                print("Выбрана версия " + user_choice)
                print("работаю..")
                logging.info("Начата работа над модпаком...")
                pb5 = Bar("Выполнение", max=5)
                shutil.rmtree(f"{self.userappdata}\\backup")
                logging.info("Удален текущий бэкап")
                pb5.next()
                shutil.copytree(f"{self.game_directory}\\mods", f"{self.userappdata}\\backup")
                logging.info("Сделан бэкап текущих модов")
                pb5.next()
                shutil.rmtree(f"{self.game_directory}\\mods")
                logging.info("Папка mods удалена")
                pb5.next()
                shutil.copytree(f"{self.userappdata}\\modpacks\\{user_choice}", f"{self.game_directory}\\tempfiles\\")
                logging.info("Модпак скопирован в директорию игры")
                pb5.next()
                p = Path(f"{self.game_directory}\\tempfiles\\")
                p.rename("mods")
                logging.info("Модпак переименован в mods")
                pb5.next()
                pb5.finish()
                print("готово")
                self.finish()
            logging.info("Worker завершил работу")

    def build_config(self):
        logging.info('Запущен build_config')
        file = open(f"{self.userappdata}\\config.ini", "w")
        file.write(
            '[paths]\n; write path to minecraft folder below (%appdata%/.minecraft if not filled)\nminecraft = \n'
            '; do not use parameter below, if do not know, what are you doing!!!!\nprogram = ')
        file.close()
        logging.info('Конфиг создан успешно')
        msg.showerror(title="Файлы были повреждены!",
                      message='Папка с данными была повреждена:-( Проверьте config.ini!!!')
        os.system(f"notepad {self.userappdata}/config.ini")
        logging.info('Конфиг открыт в блокноте')
        self.error()

    def run(self):
        while True:
            try:
                self.setup_logger()
                logging.info(f'Версия программы: {self.version}')
                os.chdir(self.userappdata)
                if not os.path.exists("logs"):
                    os.mkdir("logs")
                self.read_config()
                self.checker()
                logging.info(f'Путь к программе: {self.program_directory}')
                logging.info(f'Путь к игре: {self.game_directory}')
                logging.info(f'Путь к папке с пользовательскими данными: {self.userappdata}')
                if os.path.exists(f"{self.game_directory}\\tempfiles\\"):
                    shutil.rmtree(f"{self.game_directory}\\tempfiles")
                else:
                    pass
                self.worker()
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
