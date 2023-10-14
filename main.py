from os import system
import time
from argparse import ArgumentParser
from minesquid import MineSquid, ZeroSelector, Restart
from tkinter import messagebox as msg

parser = ArgumentParser(description='Привет!')
group1 = parser.add_mutually_exclusive_group()
group1.add_argument("--mpname", default=0, help="используйте --mpname [имя модпака] для создания ярлыков быстрого "
                                                "доступа к определенным модпакам ПО ИМЕНИ"
                                                "например /.../.../mineSquid.exe --mpname '1.20.1 survival'  <--- для "
                                                "создания ярлыка,"
                                                "активирующего модпак c именем '1.20.1 survival'")
group1.add_argument("--mpnum", default=0, help="используйте --mpnum [номер модпака] для создания ярлыков быстрого "
                                               "доступа к определенным модпакам ПО НОМЕРУ"
                                               "например /.../.../mineSquid.exe --mpnum 3  <--- для "
                                               "создания ярлыка,"
                                               "активирующего модпак с номером 3")
group1.add_argument("--restore", default=0, nargs='?', const=1, help="используйте --restore, чтобы восстановить бэкап")
args = parser.parse_args()

program_version = "2.22"
ok = MineSquid(program_version)
logging = ok.logging
while True:
    try:
        ok.setup_logger()
        logging.info(f'Версия программы: {program_version}')
        ok.read_config()
        ok.checker()
        ok.build_list()
        logging.info(f'Путь к программе: {ok.program_directory}')
        logging.info(f'Путь к игре: {ok.game_directory}')
        logging.info(f'Путь к папке с пользовательскими данными: {ok.userappdata}')
        if (int(args.mpnum) != 0 and int(args.mpnum) > 0) and int(args.mpnum) < len(ok.list)+1:
            ok.load_modpack(modpack_number=(int(args.mpnum) - 1))
        elif str(args.mpname) in ok.list:
            ok.load_modpack(modpack_number=ok.list.index(args.mpname))
        else:
            if args.restore != 0:
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
        system("cls")
        pass
    except Exception as err:
        system("cls")
        logging.error("Неизвестная ошибка!!")
        print("Неизвестная ошибка, смотри логи")
        logging.exception(err)
        time.sleep(7)
        break
