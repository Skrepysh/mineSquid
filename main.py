from pyselector import PySelector
import argparse
parser = argparse.ArgumentParser(description='Привет от разработчика!')
parser.add_argument("--devmode", default=0, help="Режим разработчика. НЕ ИСПОЛЬЗУЙТЕ ЭТОТ ПАРАМЕТР!!!")
parser.add_argument("--mp", default=0, help="используйте --mp [номер модпака] для создания ярлыков быстрого "
                                            "доступа к определенным модпакам "
                                            "например /.../.../pyselector.exe --mp 3   <--- для создания ярлыка,"
                                            "активирующего модпак 3")
parser.add_argument("--restore", default=0, help="используйте --restore 1, чтобы восстановить бэкап")
args = parser.parse_args()

program_version = "2.9.5"
ok = PySelector(program_version)
args.mp = int(args.mp)
args.restore = str(args.restore)
args.devmode = str(args.devmode)
if args.devmode == "1":
    ok.devmode()
else:
    if args.mp != 0 and args.mp > 0:
        ok.setup_logger()
        ok.read_config()
        ok.build_list()
        ok.load_modpack(args.mp - 1)
    else:
        if args.restore != "0":
            ok.setup_logger()
            ok.read_config()
            ok.restore_backup()
        else:
            ok.run()
