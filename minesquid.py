import time
from configparser import ConfigParser
import logging
import os
from sys import exit, argv
from shutil import rmtree, copy, copytree
from time import sleep
from progress.bar import Bar
from datetime import datetime
from tkinter import messagebox as msg
from tkinter import filedialog
import requests
from subprocess import Popen
from colorama import Fore, init


class ZeroSelector(Exception):
    pass


class Restart(Exception):
    pass


class DiskRoot(Exception):
    pass


class MineSquid:
    def __init__(self, version='none'):
        self.username = os.getlogin()  # пользовательское имя, отображается при запуске программы
        self.dt = datetime.now()  # текущее время
        self.user_choice = ""  # имя выбранного пользователем модпака
        self.list = []  # список модпаков (пуст при запуске)
        self.version = str(version)  # версия программы
        self.game_directory = 'не назначена'  # папка с игрой, по умолчанию не назначена
        self.program_directory = os.path.dirname(os.path.abspath(argv[0]))  # папка, где расположена сама программа
        self.userappdata = f'{os.environ["appdata"]}\\mineSquid'  # папка с данными (модпаками, бэкапом, настройками)
        self.wait_on_error = 1  # ожидание enter при ошибке, включено по умолчанию
        self.config = ConfigParser()  # конфиг
        self.logging = logging  # логирование
        init(autoreset=True)  # инит модуля Colorama. Внесение настройки автосброса цвета после каждого print()
        # noinspection PyGlobalUndefined

    def error(self, nosleep):
        if not nosleep:
            sleep(0.5)
        elif self.wait_on_error == 0:
            sleep(0.5)
        os.system("cls")

    @staticmethod
    def finish():
        print(Fore.RED + "Завершение работы...")
        sleep(0.5)
        logging.info("Работа программы завершена")
        exit()

    def err_pause(self):
        if self.wait_on_error == 1:
            string = str(Fore.RED + '>>>' + Fore.RESET)
            input(string)
        else:
            return 'disabled'

    def settings(self):
        logging.info('Открыты настройки')
        print('1 - изменить путь к папке с игрой\n2 - изменить имя пользователя, '
              'отображаемое в программе\n3 - включить/выключить ожидание enter при ошибке\n4 - выход\n*')
        input1 = input(f"Выберите настройку: {Fore.RED}")
        print(Fore.RESET, end='\r')
        if str(input1) == '1':
            logging.info('Начат процесс изменения пути к папке с игрой')
            self.edit_config('options', 'game_path', self.enter_path())
        elif str(input1) == '2':
            logging.info('Начат процесс изменения пользовательского никнейма')
            username = input(f'Введите новое имя пользователя(default - сбросить имя): {Fore.RED}')
            print(Fore.RESET, end='\r')
            if username != 'default':
                self.edit_config('options', 'custom_username', username)
            else:
                self.edit_config('options', 'custom_username', 'default')
            time.sleep(0.2)
        elif str(input1) == '3':
            wait_on_errss = input(f'Включить/выключить ожидание enter при ошибке (1 - вкл, 0 - выкл): {Fore.RED}')
            if wait_on_errss == "1":
                self.edit_config('options', 'err_pause', '1')
            elif wait_on_errss == "0":
                self.edit_config('options', 'err_pause', '0')
            else:
                print(Fore.RED + 'Неверное значение!')
            time.sleep(0.2)
        elif str(input1) == '4':
            logging.info('Выход из настроек...')
            time.sleep(0.2)
        else:
            print('Неизвестный параметр')
            self.err_pause()

    def enter_path(self):
        while True:
            path = filedialog.askdirectory(initialdir=f'{os.environ["appdata"]}\\.minecraft')
            if path == '':
                print(Fore.RED + "Редактирование отменено")
                self.err_pause()
                return self.game_directory
            elif path.replace('\\', '').replace('/', '') == path[:2]:
                logging.warning('Пользователь попытался выбрать корень диска в качестве пути к игре!')
                logging.info(f'Пользователь выбрал {path}')
                print(Fore.RED + 'Похоже, в качестве директории игры выбран корень диска\nВ целях безопасности '
                                 f'данных так делать нельзя\n{Fore.MAGENTA}Пожалуйста, выберите другой путь')
            else:
                return path

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
        self.config.read(f"{self.userappdata}\\config.ini", encoding="windows-1251")
        game_directory = self.config['options']['game_path'].replace('"', '').replace('/', '\\')
        custom_username = self.config['options']['custom_username']
        wait_on_errs = self.config['options']['err_pause']
        logging.info("Конфиг прочитан")
        if game_directory == "default" and os.path.exists(f'{os.environ["appdata"]}\\.minecraft'):
            self.game_directory = f'{os.environ["appdata"]}\\.minecraft'
        elif os.path.exists(game_directory):
            if game_directory.replace('\\', '').replace('/', '') == game_directory[:2]:
                print(Fore.RED+'Похоже, в качестве директории игры выбран корень диска\nВ целях безопасности '
                      f'данных так делать нельзя\n{Fore.MAGENTA}Пожалуйста, выберите другой путь')
                self.edit_config('options', 'game_path', self.enter_path())
            else:
                self.game_directory = game_directory
        else:
            pass
        if custom_username == 'default':
            self.username = os.getlogin()
        else:
            self.username = custom_username
        if int(wait_on_errs) == 1:
            self.wait_on_error = 1
        else:
            self.wait_on_error = 0
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
                self.edit_config('options', 'game_path', self.enter_path())
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
        print(f"Привет, {Fore.RED + self.username}!")
        print("Версия программы: " + Fore.GREEN + self.version)
        print(f'Путь к папке с игрой: {Fore.CYAN+self.game_directory}')
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
        print("re - восстановление бэкапа\nset - открыть настройки\nupd - обновление программы"
              "\n? - открыть readME\nq - выход")
        logging.info(f"Количество модпаков: {int(counter) - 1}")
        logging.info("Ждем выбора модпака пользователем...")
        selector = str(input(f"Выберите модпак: {Fore.RED}"))
        print(Fore.RESET, end='\r')
        if selector == "re":
            self.restore_backup()
        elif selector == "set":
            print("Открытие настроек...\n*")
            logging.info("Введена команда set, открыты настройки...")
            self.settings()
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
            logging.info("Составлен список модпаков")
        else:
            self.list = ["Папка с игрой не назначена", "Модпаки недоступны", Fore.RED + "Для выбора папки введите set"]
            logging.info("Папка с игрой не назначена!")

    def edit_config(self, section, option, what):
        logging.info('Запущен edit_config')
        logging.info("Начато редактирование config файла")
        self.config.set(section, option, what)
        with open(f"{self.userappdata}\\config.ini", "w") as f:
            self.config.write(f)
        logging.info('Конфиг отредактирован успешно')

    def repair_config(self):
        tempparser = ConfigParser()
        logging.warning('Запуск восстановление конфига!')
        with open(f"{self.userappdata}\\config.ini", "w") as cfg:
            tempparser.add_section("options")
            tempparser.set("options", "game_path", "default")
            tempparser.set("options", "custom_username", "default")
            tempparser.set("options", "err_pause", "1")
            tempparser.write(cfg)
        self.read_config()
        self.edit_config('options', 'game_path', self.enter_path())
        logging.info('Конфиг восстановлен')

    def load_modpack(self, modpack_number):
        if self.game_directory != 'не назначена':
            self.user_choice = self.list[modpack_number]
            fileslist1 = os.listdir(f"{self.userappdata}\\modpacks\\{self.user_choice}")
            fileslist2 = os.listdir(f"{self.game_directory}\\mods")
            print("Выбрана версия " + Fore.GREEN + self.user_choice)
            print(Fore.RED + "Работаю...")
            logging.info("Начата работа над модпаком...")
            if len(fileslist2) > 1:
                pb1 = Bar(Fore.LIGHTMAGENTA_EX + "Резервное коп-е" + Fore.CYAN,
                          max=len(fileslist2), fill=Fore.GREEN + '@' + Fore.CYAN)
                for file in os.listdir(f'{self.userappdata}\\backup'):
                    if os.path.isfile(f'{self.userappdata}\\backup\\{file}'):
                        os.remove(f'{self.userappdata}\\backup\\{file}')
                    else:
                        rmtree(f'{self.userappdata}\\backup\\{file}')
                logging.info("Удален текущий бэкап")
                for file in fileslist2:
                    if os.path.isdir(f"{self.game_directory}\\mods\\{file}"):
                        copytree(f"{self.game_directory}\\mods\\{file}",
                                 f"{self.userappdata}\\backup\\{file}", dirs_exist_ok=True)
                    else:
                        copy(src=f"{self.game_directory}\\mods\\{file}", dst=f"{self.userappdata}\\backup")
                    pb1.next()
                logging.info("Сделан бэкап текущих модов")
                pb1.finish()
            else:
                logging.info('Папка модов пуста, бэкапить нечего')
            pb2 = Bar(Fore.LIGHTMAGENTA_EX + "Выполнение" + Fore.CYAN,
                      max=len(fileslist1) + 1, fill=Fore.GREEN + '@' + Fore.CYAN)
            for file in os.listdir(f"{self.game_directory}\\mods\\"):
                if os.path.isfile(f"{self.game_directory}\\mods\\{file}"):
                    os.remove(f"{self.game_directory}\\mods\\{file}")
                else:
                    rmtree(f"{self.game_directory}\\mods\\{file}")
            logging.info("Папка mods очищена")
            pb2.next()
            for file in fileslist1:
                if os.path.isdir(f"{self.userappdata}\\modpacks\\{self.user_choice}\\{file}"):
                    copytree(f"{self.userappdata}\\modpacks\\{self.user_choice}\\{file}",
                             f"{self.game_directory}\\mods\\{file}", dirs_exist_ok=True)
                else:
                    copy(src=f"{self.userappdata}\\modpacks\\{self.user_choice}\\{file}",
                         dst=f"{self.game_directory}\\mods")
                pb2.next()
            # copytree(f"{self.userappdata}\\modpacks\\{self.user_choice}", f"{self.game_directory}\\mods\\")
            logging.info("Модпак скопирован в папку mods")
            logging.info("ГОТОВО!")
            pb2.finish()
            print(Fore.GREEN + "Готово")
            self.finish()
        else:
            print(Fore.RED + "Папка с игрой не назначена!")
            a = self.err_pause()
            if a == 'disabled':
                sleep(1.5)
            raise Restart

    def restore_backup(self):
        if self.game_directory != 'не назначена':
            if len(os.listdir(f"{self.userappdata}\\backup")) == 0:
                print("Бэкап отсутствует, восстанавливать нечего")
                sleep(1)
                raise Restart
            else:
                fileslist = os.listdir(f"{self.game_directory}\\mods")
                fileslist2 = os.listdir(f'{self.userappdata}\\backup')
                bob = False
                print(Fore.RED + "Работаю...")
                logging.info("Пользователь запустил восстановление бэкапа")
                if os.path.exists(f"{self.game_directory}\\mods") and len(os.listdir(f"{self.game_directory}\\mods")):
                    pb1 = Bar(Fore.LIGHTMAGENTA_EX + "Резервное коп-е" + Fore.CYAN,
                              max=len(fileslist), fill=Fore.GREEN + '@' + Fore.CYAN)
                    bob = True
                    if not os.path.exists(f"{self.userappdata}\\bob\\"):
                        os.mkdir(f"{self.userappdata}\\bob\\")
                    # copytree(f"{self.game_directory}\\mods", f"{self.userappdata}\\bob", dirs_exist_ok=True)
                    for file in fileslist:
                        if os.path.isdir(f"{self.game_directory}\\mods\\{file}"):
                            copytree(f"{self.game_directory}\\mods\\{file}",
                                     f"{self.userappdata}\\bob\\{file}", dirs_exist_ok=True)
                        else:
                            copy(f"{self.game_directory}\\mods\\{file}", f"{self.userappdata}\\bob\\")
                        pb1.next()
                    logging.info("Бэкап сделан перед восстановлением бэкапа)")
                    for file in os.listdir(f"{self.game_directory}\\mods\\"):
                        if os.path.isfile(f"{self.game_directory}\\mods\\{file}"):
                            os.remove(f"{self.game_directory}\\mods\\{file}")
                        else:
                            rmtree(f"{self.game_directory}\\mods\\{file}")
                    logging.info("Папка mods очищена")
                    pb1.finish()
                else:
                    pass
                pb2 = Bar(Fore.LIGHTMAGENTA_EX + "Восстановление" + Fore.CYAN,
                          max=len(fileslist2)+2, fill=Fore.GREEN + '@' + Fore.CYAN)
                for file in fileslist2:
                    if os.path.isfile(f'{self.userappdata}\\backup\\{file}'):
                        copy(f'{self.userappdata}\\backup\\{file}', f'{self.game_directory}\\mods')
                    else:
                        copytree(f'{self.userappdata}\\backup\\{file}',
                                 f'{self.game_directory}\\mods\\{file}', dirs_exist_ok=True)
                    pb2.next()
                # copytree(f"{self.userappdata}\\backup", f"{self.game_directory}\\mods\\")
                pb2.next()
                if bob:
                    rmtree(f"{self.userappdata}\\backup")
                    os.rename(f"{self.userappdata}\\bob", f"{self.userappdata}\\backup")
                else:
                    pass
                logging.info("Бэкап восстановлен")
                pb2.next()
                pb2.finish()
                print(Fore.GREEN + "Бэкап восстановлен")
                self.finish()
        else:
            print(Fore.RED + "Папка с игрой не назначена!")
            a = self.err_pause()
            if a == 'disabled':
                sleep(1.5)
            raise Restart

    def update(self):
        logging.info("Начата проверка обновлений...")
        print("Проверка обновлений...")
        try:
            version_url = 'https://raw.githubusercontent.com/Skrepysh/mineSquid/master/version.txt'
            version = requests.get(version_url).text.replace('\n', '')
        except Exception:
            print("Не удалось проверить обновления(((\nПроверьте подключение к интернету")
            sleep(1.5)
            raise Restart
        if float(version) > float(self.version):
            print(f"Найдена новая версия программы: {Fore.GREEN + version}")
            logging.info(f"Найдена новая версия программы: {version}!")
            accept = input(f"Выполнить обновление? {Fore.GREEN}Y{Fore.RESET} - да, "
                           f"{Fore.RED}N{Fore.RESET} - нет: {Fore.CYAN}")
            print(Fore.RESET, end='\r')
            if accept.lower() == "y":
                logging.info("Обновление подтверждено")
                print(Fore.CYAN + "Скачиваю обновление...")
                try:
                    logging.info("Скачивание...")
                    update_url = (f"https://github.com/Skrepysh/mineSquid/releases/download/v{version}"
                                  f"/mineSquid_v{version}_setup.exe")
                    os.chdir(os.environ['temp'])
                    open("mineSquidUpdate.exe", "wb").write(requests.get(update_url, allow_redirects=True).content)
                except Exception:
                    print(Fore.RED + "Не удалось скачать обновление(((\nПроверьте подключение к интернету")
                    sleep(1.5)
                    raise Restart
                print("Запускаю процесс установки...")
                logging.info(Fore.CYAN + "Запускаю процесс установки...")
                if os.path.exists(f'{os.environ["temp"]}\\mineSquidUpdate.exe'):
                    Popen(f'{os.environ["temp"]}\\mineSquidUpdate.exe /Silent')
                else:
                    print(Fore.RED + "При обновлении произошла ошибка!")
                exit()
            else:
                logging.info("Обновление отменено")
                print(Fore.RED + "Обновление отменено")
                sleep(1)
                raise Restart
        else:
            logging.info("Обновлений нет")
            print(Fore.LIGHTMAGENTA_EX + "Обновлений нет")
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
