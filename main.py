import os
import time
import argparse
from minesquid import MineSquid, ZeroSelector, Restart
from tkinter import messagebox as msg
parser = argparse.ArgumentParser(description='Привет от разработчика!')
parser.add_argument("--mp", default=0, help="используйте --mp [номер модпака] для создания ярлыков быстрого "
                                            "доступа к определенным модпакам "
                                            "например /.../.../mineSquid.exe --mp 3   <--- для создания ярлыка,"
                                            "активирующего модпак 3")
parser.add_argument("--restore", default=0, nargs='?', const=1, help="используйте --restore, чтобы восстановить бэкап")
args = parser.parse_args()

program_version = "2.16"
ok = MineSquid(program_version)
args.mp = int(args.mp)
args.restore = str(args.restore)
logging = ok.logging

while True:
    try:
        ok.setup_logger()
        logging.info(f'Версия программы: {program_version}')
        ok.read_config()
        ok.checker()
        logging.info(f'Путь к программе: {os.getcwd()}')
        logging.info(f'Путь к игре: {ok.game_directory}')
        logging.info(f'Путь к папке с пользовательскими данными: {ok.userappdata}')
        if args.mp != 0 and args.mp > 0:
            ok.build_list()
            ok.load_modpack(modpack_number=(args.mp - 1), mode="1")
        else:
            if args.restore != "0":
                ok.restore_backup()
            else:
                ok.run()
    except KeyError as err:
        logging.error("KeyError")
        logging.exception(err)
        ok.repair_config()
    except IndexError as err:
        logging.error("IndexError")
        logging.exception(err)
        print("неверное значение\nперезапуск")
        ok.error()
    except PermissionError as err:
        logging.error("PermissionError")
        logging.exception(err)
        msg.showerror(title="Ошибка доступа", message="Не удается получить доступ к какому-то файлу.\n"
                                                      "Проверьте, закрыт ли клиент игры!"
                                                      "\nИли попробуйте запустить программу "
                                                      "от имени администратора")
        exit()
    except OverflowError as err:
        logging.error("OverflowError")
        logging.exception(err)
        print("многацифер\nперезапуск")
        ok.error()
    except ZeroSelector:
        logging.error("ZeroSelector")
        print("неверное значение\nперезапуск")
        ok.error()
    except ValueError as err:
        logging.error("ValueError")
        logging.exception(err)
        print("неверное значение\nперезапуск")
        ok.error()
    except FileNotFoundError as err:
        logging.error("FileNotFoundError")
        logging.exception(err)
        logging.error("FileNotFoundError, запуск чекера")
        ok.checker()
        ok.finish()
    except Restart:
        print("Перезапуск...")
        logging.info("Программа перезапускается...")
        os.system("cls")
        pass
    except Exception as err:
        os.system("cls")
        logging.error("Неизвестная ошибка!!")
        print("неизвестная ошибка, смотри логи")
        logging.exception(err)
        time.sleep(7)
        break
