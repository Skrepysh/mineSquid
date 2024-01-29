import configparser
from os import system
from argparse import ArgumentParser
from minesquid import MineSquid, ZeroSelector, Restart
from tkinter import messagebox as msg
from colorama import Fore


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

program_version = "2.26"
program = MineSquid(program_version)
logging = program.logging
if __name__ == "__main__":
    while True:
        try:
            program.setup_logger()
            logging.info(f'Версия программы: {program_version}')
            program.read_config()
            program.checker()
            program.build_list()
            logging.info(f'Путь к программе: {program.program_directory}')
            logging.info(f'Путь к игре: {program.game_directory}')
            logging.info(f'Путь к папке с пользовательскими данными: {program.userappdata}')
            if (int(args.mpnum) != 0 and int(args.mpnum) > 0) and int(args.mpnum) < len(program.list)+1:
                program.cmd_args = 1
                program.load_modpack(modpack_number=(int(args.mpnum) - 1))
            elif str(args.mpname) in program.list:
                program.cmd_args = 1
                program.load_modpack(modpack_number=program.list.index(args.mpname))
            else:
                if args.restore != 0:
                    program.cmd_args = 1
                    program.restore_backup()
                else:
                    program.run()
        except KeyError as err:
            logging.error("KeyError")
            logging.exception(err)
            program.repair_config()
        except configparser.ParsingError as err:
            logging.error("ParsingError")
            logging.exception(err)
            program.repair_config()
        except IndexError as err:
            logging.error("IndexError")
            logging.exception(err)
            print(Fore.RED + "Неверное значение!")
            a = program.err_pause()
            if a:
                print(f"{Fore.MAGENTA}Перезапуск")
            program.error(nosleep=True)
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
            print(Fore.RED + "Неверное значение")
            a = program.err_pause()
            if a:
                print(f"{Fore.MAGENTA}Перезапуск")
            program.error(nosleep=True)
        except ValueError as err:
            logging.error("ValueError")
            logging.exception(err)
            print(Fore.RED + "Неверное значение!")
            a = program.err_pause()
            if a:
                print(f"{Fore.MAGENTA}Перезапуск")
            program.error(nosleep=True)
        except FileNotFoundError as err:
            logging.error("FileNotFoundError")
            logging.exception(err)
            logging.error("FileNotFoundError, запуск чекера")
            program.checker()
            program.finish()
        except Restart:
            logging.info("Программа перезапускается (raise Restart)")
            system("cls")
        except KeyboardInterrupt:
            print(Fore.RED + '\nQuit by Ctrl+C')
            exit()
        except Exception as err:
            system("cls")
            logging.error("Неизвестная ошибка!!")
            print(Fore.RED + f"Неизвестная ошибка, смотри {Fore.MAGENTA}логи")
            logging.exception(err)
            program.err_pause()
            break
