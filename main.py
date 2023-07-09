from pyselector import PySelector
import argparse
parser = argparse.ArgumentParser(description='Привет, от разработчика!')
parser.add_argument("--devmode", default=0, help="НЕ ИСПОЛЬЗУЙТЕ ЭТОТ ПАРАМЕТР!!!")
parser.add_argument("--mp", default=0, help="используйте --mp [номер модпака] для создания ярлыков быстрого "
                                            "доступа к определенным модпакам "
                                            "например /.../.../pyselector.exe --mp 3   <--- для создания ярлыка,"
                                            "активирующего модпак 3")
parser.add_argument("--restore", default=0, help="используйте --restore 1, чтобы восстановить бэкап")
args = parser.parse_args()

program_version = "2.9"
ok = PySelector(program_version)
args.mp = str(args.mp)
args.restore = str(args.restore)
args.devmode = str(args.devmode)
if args.devmode == "1":
    ok.devmode()
else:
    if args.mp == "0":
        if args.restore == "0":
            ok.run()
        ok.run(select2="restore")
    else:
        ok.run(select2=args.mp)
