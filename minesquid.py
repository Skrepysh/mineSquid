import time
import flet as ft
import os
from tkinter import filedialog
from shutil import rmtree, copytree
from sys import argv
from configparser import ConfigParser
import requests
from subprocess import Popen

program_version = '3.2'
build_date = '01.05.2024'


class MineSquid:

    def __init__(self, minesquid_version='nope', minesquid_build_date='nope'):
        self.mp_list = []  # список модпаков (пуст при запуске)
        self.game_directory = ''  # папка с игрой, по умолчанию не назначена
        self.game_directory_exists = False  # существует ли папка с игрой
        self.program_directory = os.path.dirname(os.path.abspath(argv[0]))  # папка, где расположена программа
        self.program_version = minesquid_version  # версия программы
        self.build_date = minesquid_build_date  # дата сборки
        self.userappdata = f'{os.environ["appdata"]}\\mineSquid'  # папка с данными (модпаками, бэкапом, настройками)
        self.config = ConfigParser()  # конфиг

    def main(self, page: ft.Page):
        themes = ['dark', 'light']
        states = ['ERROR', 'OK']
        colors = {
            'cyanaccent200': ft.colors.CYAN_ACCENT_200,  # бирюзовый (стандартный)
            'redaccent700': ft.colors.RED_ACCENT_700,  # красный
            'green': ft.colors.GREEN,  # зеленый
            'lightgreenaccent400': ft.colors.LIGHT_GREEN_ACCENT_400,  # салатовый
            'blue': ft.colors.BLUE,  # синий
            'pink': ft.colors.PINK,  # розовый
            'pink300': ft.colors.PINK_300,  # светло-розовый
            'deeppurple': ft.colors.DEEP_PURPLE,  # темно-фиолетовый
            'purple': ft.colors.PURPLE,  # фиолетовый
            'purpleaccent': ft.colors.PURPLE_ACCENT,  # светло-фиолетовый 
            'deeporange': ft.colors.DEEP_ORANGE,  # оранжевый
            'orange': ft.colors.ORANGE,  # светло-оранжевый
            'yellow': ft.colors.YELLOW,  # желтый
        }
        color_names = {
            'cyanaccent200': "Бирюзовый",
            'redaccent700': "Красный",
            'green': "Зелёный",
            'lightgreenaccent400': 'Салатовый',
            'blue': "Синий",
            'pink': "Розовый",
            'pink300': "Светло-розовый",
            'deeppurple': "Темно-фиолетовый",
            'purple': "Фиолетовый",
            'purpleaccent': "Светло-фиолетовый",
            'deeporange': "Оранжевый",
            'orange': "Светло-оранжевый",
            'yellow': 'Жёлтый',
        }
        error_message = ''
        page.theme_mode = themes[0]
        page.title = 'mineSquid'
        page.window_maximizable = False
        page.window_height = 750
        page.window_width = 450
        page.window_min_width = 375
        page.horizontal_alignment = page.vertical_alignment = "center"
        page.radio = ft.RadioGroup(radio := ft.ListView())
        page.splash = ft.ProgressBar()
        page.splash.visible = False

        def pick_folder(e):
            folder_field.value = enter_path()
            folder_field.error_text = ''
            check_settings()
            page.update()

        def select_folder(e):
            edit_config('options', 'game_path', a := enter_path())
            folder_field.value = a
            refresh(0)

        def open_mpfolder(e):
            Popen(f'explorer {self.userappdata}\\modpacks')

        def close_dlg(e=0):
            if page.dialog is not None:
                if page.dialog.open:
                    page.dialog.open = False
                    page.update()

        def open_dlg(e=0):
            page.dialog.open = True
            page.update()

        def check_settings(e=0):
            folder_field_ok = True
            width_field_ok = True
            height_field_ok = True

            if os.path.exists(folder_field.value):
                folder_field_ok = True
                folder_field.error_text = ''
            else:
                folder_field_ok = False
                folder_field.error_text = 'Указанный путь не найден'

            if len(width_field.value) == 0:
                width_field.error_text = 'Поле не может быть пустым'
                width_field_ok = False
            elif int(width_field.value) < 375:
                width_field.error_text = 'Слишком маленькое значение'
                width_field_ok = False
            elif int(width_field.value) > 2560:
                width_field.error_text = 'Слишком большое значение'
            else:
                width_field.error_text = ''
                width_field_ok = True

            if len(height_field.value) == 0:
                height_field.error_text = 'Поле не может быть пустым'
                height_field_ok = False
            elif int(height_field.value) < 650:
                height_field.error_text = 'Слишком маленькое значение'
                height_field_ok = False
            elif int(height_field.value) > 2560:
                height_field.error_text = 'Слишком большое значение'
            else:
                height_field.error_text = ''
                height_field_ok = True

            if folder_field_ok and (width_field_ok and height_field_ok):
                apply_btn.disabled = False
            else:
                apply_btn.disabled = True

            page.update()

        def apply_settings(e):
            log_add('*' * 16)
            log_add('Применение настроек')
            folder_ok = False
            checkboxes_ok = True  # Че может пойти не так?
            width_and_height_ok = False
            if os.path.exists(a := folder_field.value):
                folder_ok = True
            else:
                folder_field.error_text = 'Указанный путь не найден'
            if (375 <= int(width_field.value) <= 2560) and (650 <= int(height_field.value) <= 2560):
                width_and_height_ok = True
            log_add(f'Папка с игрой...{states[int(folder_ok)]}')
            log_add(f'Чекбоксы...{states[int(checkboxes_ok)]}')
            log_add(f'Высота и ширина окна...{states[int(width_and_height_ok)]}')

            if folder_ok and checkboxes_ok and width_and_height_ok:

                edit_config('options', 'game_path', a)
                folder_field.error_text = ''

                edit_config('options', 'backup_restore_dlg', str(open_dlg_backup_restored_checkbox.value))
                edit_config('options', 'mp_load_dlg', str(open_dlg_mp_loaded_checkbox.value))
                edit_config('options', 'check_current_modpack', str(check_current_modpack_checkbox.value))

                page.window_width = width_field.value
                page.window_height = height_field.value
                edit_config('options', 'window_height', str(height_field.value))
                edit_config('options', 'window_width', str(width_field.value))

                edit_config('options', 'compact_ui', str(compact_ui_checkbox.value))

                edit_config('options', 'ui_color', colors[ui_color_dropdown.value])

                log_add('Настройки применены успешно')
                page.dialog = dlg_settings_applied
                open_dlg()
                refresh(0)
            else:
                log_add('Обнаружены некорректные настройки, не удалось применить')
                page.dialog = dlg_incorrect_settings
                open_dlg()
            log_add('*' * 16)

        def reset_settings(e):
            log_add('*' * 16)
            log_add('Сброс настроек')
            repair_config(reset_settings=True)
            log_add("Настройки сброшены")
            read_config()
            log_add('*' * 16)
            check_settings()
            close_dlg()

        def open_reset_settings_dlg(e):
            page.dialog = dlg_confirm_reset_settings
            open_dlg()

        def refresh(e):
            start_time = time.time()
            log_add('*' * 16)
            log_add('Обновление данных')
            prepare_main_tab()
            read_config()
            check_settings()
            page.radio.value = None
            end_time = time.time()
            log_add(f'Затрачено времени: {end_time - start_time}с')
            log_add('Данные обновлены')
            log_add('*' * 16)

        def about(e):
            page.dialog = dlg_about_minesquid
            open_dlg()

        def log_add(what):
            log.controls.append(ft.Text('- ' + what))
            page.update()

        def open_readme(e):
            os.startfile(f'{self.program_directory}\\readme.txt')

        def enter_path():
            path = filedialog.askdirectory(initialdir=f'{os.environ["appdata"]}\\.minecraft')
            if path == '':
                close_dlg()
                page.dialog = dlg_edit_cancel
                open_dlg()
                if self.game_directory != '':
                    return self.game_directory
                else:
                    return ''
            else:
                close_dlg()
                return path

        def build_list():
            os.chdir(f"{self.userappdata}\\modpacks")
            self.mp_list = [e for e in os.listdir() if os.path.isdir(e)]
            if check_current_modpack_checkbox.value and os.path.exists(mdir := f'{self.game_directory}\\mods'):
                current = os.listdir(mdir)
                for x in self.mp_list:
                    if os.listdir(x) == current:
                        index = self.mp_list.index(x)
                        x1 = f'{x}👈'
                        self.mp_list[index] = x1
                        log_add(f'Текущий модпак: {x}')
            log_add('Список модпаков обновлен')
            if not self.game_directory_exists:
                log_add('Папка с игрой не назначена')

        def edit_config(section, option, what):
            self.config.set(section, option, what)
            with open(f"{self.userappdata}\\config.ini", "w") as f:
                self.config.write(f)

        def repair_config(**kwargs):
            default_values = {
                'game_path': '',
                'backup_restore_dlg': 'True',
                'mp_load_dlg': 'False',
                'theme': 'dark',
                'window_height': '750',
                'window_width': '450',
                'ui_color': 'cyanaccent200',
                'compact_ui': 'True',
                'check_current_modpack': 'False'
            }
            if 'restore_section' in kwargs:
                with open(f'{self.userappdata}\\config.ini', 'w') as cfg:
                    self.config.add_section('options')
                    self.config.write(cfg)
            elif 'reset_settings' in kwargs:
                for x in default_values:
                    edit_config('options', x, default_values[x])
            else:
                edit_config('options', kwargs['option'], default_values[kwargs['option']])

        def read_config():
            self.config.read(f"{self.userappdata}\\config.ini", encoding="windows-1251")

            options = ['game_path',
                       'mp_load_dlg',
                       'backup_restore_dlg',
                       'theme', 'window_width',
                       'window_height',
                       'ui_color',
                       'compact_ui',
                       'check_current_modpack'
                       ]

            if not self.config.has_section('options'):
                log_add('Конфиг отсутствует')
                repair_config(restore_section=True)
                log_add('Конфиг создан')

            for x in options:
                if not self.config.has_option('options', x):
                    log_add(f'В конфиге отсутствует параметр {x}, восстановление')
                    repair_config(option=x)

            config_game_directory = self.config['options']['game_path'].replace('"', '').replace('/', '\\')
            config_open_dlg_mp_loaded = self.config['options']['mp_load_dlg']
            config_open_dlg_backup_restored = self.config['options']['backup_restore_dlg']
            config_theme = self.config['options']['theme']
            config_width = self.config['options']['window_width']
            config_height = self.config['options']['window_height']
            config_ui_color = self.config['options']['ui_color']
            config_compact_ui = self.config['options']['compact_ui']
            config_check_current_modpack = self.config['options']['check_current_modpack']

            if os.path.exists(config_game_directory):  # Обработка пути к папке с игрой
                self.game_directory = config_game_directory
                self.game_directory_exists = True
                folder_field.error_text = ''
            elif not os.path.exists(config_game_directory) and len(config_game_directory) > 0:
                self.game_directory_exists = False
                folder_field.error_text = 'Указанный путь не найден'
            else:
                self.game_directory_exists = False
                self.game_directory = ''
                folder_field.error_text = ''
            folder_field.value = config_game_directory  # Конец обработки пути к папке с игрой

            if config_open_dlg_mp_loaded == 'True':  # Обработка настроек диалогов об успешном действии
                open_dlg_mp_loaded_checkbox.value = True
            else:
                open_dlg_mp_loaded_checkbox.value = False
            if config_open_dlg_backup_restored == 'True':
                open_dlg_backup_restored_checkbox.value = True
            else:
                open_dlg_backup_restored_checkbox.value = False  # Конец обработки настроек диалогов об успешном
                # действии

            if config_check_current_modpack == 'True':
                check_current_modpack_checkbox.value = True
            else:
                check_current_modpack_checkbox.value = False

            if config_theme == 'dark':
                page.theme_mode = themes[0]  # Темная тема
            elif config_theme == 'light':
                page.theme_mode = themes[1]  # Светлая темя
            else:
                pass

            page.window_width = config_width
            page.window_height = config_height
            width_field.value = config_width
            height_field.value = config_height
            width_field.error_text = ''
            height_field.error_text = ''

            ui_color_dropdown.value = colors[config_ui_color]  # ставим текущий цвет в выпадающий список
            if config_compact_ui == 'True':
                page.theme = ft.Theme(
                    color_scheme_seed=colors[ui_color_dropdown.value],
                    visual_density=ft.ThemeVisualDensity.COMPACT
                )
                compact_ui_checkbox.value = True
            else:
                page.theme = ft.Theme(
                    color_scheme_seed=colors[ui_color_dropdown.value],
                    visual_density=ft.ThemeVisualDensity.COMFORTABLE
                )
                compact_ui_checkbox.value = False
            page.appbar.bgcolor = colors[ui_color_dropdown.value]  # ставим цвет аппбара
            page.bottom_appbar.bgcolor = colors[ui_color_dropdown.value]  # ставим цвет нижнего аппбара
            page.splash.color = colors[ui_color_dropdown.value]  # ставим цвет сплэша (прогрессбара)
            page.splash.update()  # обновляем сплэш (почему он не обновляется сам)

            log_add(f"Путь к папке с игрой: {self.game_directory}")
            log_add(f"Ширина окна: {config_width}")
            log_add(f"Высота окна: {config_height}")
            log_add(f'Цвет интерфейса: {color_names[config_ui_color]}')

            page.update()

        dlg_papka = ft.AlertDialog(
            modal=True,
            title=ft.Text('Ошибка'),
            content=ft.Text('Папка с игрой не назначена'),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton('Назначить', on_click=select_folder),
                ft.TextButton("OK", on_click=close_dlg),
            ],
        )

        dlg_mp = ft.AlertDialog(
            modal=True,
            title=ft.Text('Внимание!'),
            content=ft.Text("Сначала выберите модпак"),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ],

        )

        dlg_nobackup = ft.AlertDialog(
            modal=True,
            title=ft.Text('Информация'),
            content=ft.Text('Бэкап отсутствует, восстанавливать нечего'),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ]
        )

        dlg_edit_cancel = ft.AlertDialog(
            modal=True,
            title=ft.Text('Информация'),
            content=ft.Text('Редактирование отменено'),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ]
        )

        dlg_backup_restored = ft.AlertDialog(
            modal=True,
            title=ft.Text('Информация'),
            content=ft.Text('Готово! Бэкап восстановлен'),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ]
        )

        dlg_mp_loaded = ft.AlertDialog(
            modal=True,
            title=ft.Text('Информация'),
            content=ft.Text('Готово! Модпак загружен'),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ]
        )

        dlg_incorrect_settings = ft.AlertDialog(
            modal=True,
            title=ft.Text('Ошибка'),
            content=ft.Text('Обнаружены неверные настройки!'),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ]
        )

        dlg_settings_applied = ft.AlertDialog(
            modal=True,
            title=ft.Text('Информация'),
            content=ft.Text('Настройки применены'),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ]
        )

        dlg_confirm_reset_settings = ft.AlertDialog(
            modal=True,
            title=ft.Text('Внимание!'),
            content=ft.Text('Сбросить настройки?'),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("Да", on_click=reset_settings),
                ft.TextButton("Нет", on_click=close_dlg),
            ]
        )

        dlg_about_minesquid = ft.AlertDialog(
            modal=True,
            title=ft.Text('О программе'),
            content=ft.Text(
                f'mineSquid версии {self.program_version}\n'
                f'Дата сборки: {self.build_date}\n'
                f'by Skrepysh'
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("Закрыть", on_click=close_dlg),
            ]
        )

        def load_modpack(modpack_number):
            start_time = time.time()
            if not os.path.exists(a := f'{self.game_directory}\\mods'):
                os.mkdir(a)
            user_choice = self.mp_list[modpack_number]
            log_add(f'Выбран модпак {user_choice}')
            log_add('Загрузка...')
            fileslist = os.listdir(f"{self.game_directory}\\mods")
            if len(fileslist) > 0:
                rmtree(f'{self.userappdata}\\backup')
                copytree(f"{self.game_directory}\\mods",
                         f"{self.userappdata}\\backup", dirs_exist_ok=True)
                log_add('Бэкап создан')
            else:
                log_add('Бэкап не требуется')
            rmtree(f"{self.game_directory}\\mods")
            copytree(f"{self.userappdata}\\modpacks\\{user_choice}",
                     f"{self.game_directory}\\mods\\", dirs_exist_ok=True)
            log_add(f'Модпак "{user_choice}" загружен')
            end_time = time.time()
            log_add(f'Затрачено времени: {end_time - start_time}с')

        def restore_backup():
            start_time = time.time()
            fileslist = os.listdir(f"{self.game_directory}\\mods")
            log_add('Восстановление бэкапа...')
            bob = False

            if os.path.exists(f"{self.game_directory}\\mods") and len(fileslist):
                log_add('Создаю бэкап текущих модов (на всякий случай)...')
                bob = True
                if not os.path.exists(f"{self.userappdata}\\bob\\"):
                    os.mkdir(f"{self.userappdata}\\bob\\")
                copytree(
                    src=f"{self.game_directory}\\mods",
                    dst=f"{self.userappdata}\\bob",
                    dirs_exist_ok=True
                )
                rmtree(f'{self.game_directory}\\mods')
                log_add('Бэкап текущих модов создан')
            else:
                pass
            log_add('Восстанавливаю...')
            copytree(f"{self.userappdata}\\backup", f"{self.game_directory}\\mods\\", dirs_exist_ok=True)
            if bob:
                rmtree(f"{self.userappdata}\\backup")
                os.rename(f"{self.userappdata}\\bob", f"{self.userappdata}\\backup")
            else:
                pass
            log_add('Бэкап восстановлен')
            end_time = time.time()
            log_add(f'Затрачено времени {end_time - start_time}')

        def change_theme(e):
            current_theme = themes.index(page.theme_mode)
            current_theme = bool(current_theme)
            new_theme = themes[int(not current_theme)]
            page.theme_mode = new_theme
            edit_config('options', 'theme', new_theme)
            if bool(not current_theme):
                theme_btn.icon = ft.icons.NIGHTLIGHT_OUTLINED
            else:
                theme_btn.icon = ft.icons.WB_SUNNY_OUTLINED
            page.update()

        def prepare_main_tab():
            page.update()
            build_list()
            if len(self.mp_list) > 0:
                page.update()
                radio.controls.clear()
                for x in self.mp_list:
                    a = ft.Radio(value=x, label=x, )
                    radio.controls.append(a)
                main_tab.content = page.radio
                page.floating_action_button.disabled = False
            else:
                page.floating_action_button.disabled = True
                main_tab.content = ft.Column(controls=[
                    ft.Text('Внимание!', size=36),
                    ft.Text('[папка модпаков пуста]', size=24)
                ])
            page.update()

        def loadmp(e):
            log_add('*' * 16)
            log_add('Попытка загрузить модпак...')
            if not page.radio.value:
                log_add('Модпак не выбран, отмена операции')
                page.dialog = dlg_mp
                open_dlg()
            else:
                page.floating_action_button.disabled = True
                restore_btn.disabled = True
                page.update()
                if self.game_directory_exists:
                    log_add('Все ок, начинаю загрузку...')
                    page.splash.visible = True
                    page.update()
                    load_modpack(self.mp_list.index(page.radio.value))
                    page.splash.visible = False
                    if open_dlg_mp_loaded_checkbox.value:
                        page.dialog = dlg_mp_loaded
                        open_dlg()
                    page.update()
                else:
                    log_add('Не назначена папка с игрой, отмена операции')
                    page.dialog = dlg_papka
                    open_dlg()
                refresh(0)
                page.floating_action_button.disabled = False
                restore_btn.disabled = False
                page.update()
            log_add('*' * 16)

        def restore(e):
            log_add('*' * 16)
            log_add('Попытка восстановить бэкап...')
            page.floating_action_button.disabled = True
            restore_btn.disabled = True
            page.update()
            if self.game_directory_exists:
                if len(os.listdir(f"{self.userappdata}\\backup")) > 0:  # Если папка с бэкапом не пуста
                    log_add('Все ок, начинаю восстановление')
                    page.splash.visible = True
                    page.update()
                    restore_backup()
                    page.splash.visible = False
                    if open_dlg_backup_restored_checkbox.value:
                        page.dialog = dlg_backup_restored
                        open_dlg()
                else:
                    log_add('Бэкап отсутствует, отмена операции')
                    page.dialog = dlg_nobackup
                    open_dlg()
            else:
                page.dialog = dlg_papka
                open_dlg()
                log_add('Папка с игрой не назначена, отмена операции')
            refresh(0)
            page.floating_action_button.disabled = False
            restore_btn.disabled = False
            log_add('*' * 16)
            page.update()

        def check_for_updates(e):
            log_add('*' * 16)
            log_add('Проверка обновлений...')
            log_add(f'Текущая версия программы {self.program_version}')
            global new_version
            try:
                repo = 'https://raw.githubusercontent.com/Skrepysh/mineSquid/master/version.txt'
                new_version = requests.get(repo).text.replace('\n', '')
            except Exception:
                log_add("Не удалось проверить обновления!")
                log_add('*' * 16)
                dlg_update1.title = ft.Text('Ошибка')
                dlg_update1.content = ft.Text('Не удалось проверить наличие обновлений.\n'
                                              'Проверьте подключение к интернету!')
                page.dialog = dlg_update1
                open_dlg()
                return

            current_version_major = self.program_version.partition('.')[0]
            current_version_minor = self.program_version[len(current_version_major) + 1:]
            new_version_major = new_version.partition('.')[0]
            new_version_minor = new_version[len(new_version_major) + 1:]
            current_version_major = int(current_version_major)
            current_version_minor = int(current_version_minor)
            new_version_major = int(new_version_major)
            new_version_minor = int(new_version_minor)

            def update_available():
                log_add(f'Найдена новая версия программы: {new_version}')
                dlg_update_available.content = ft.Text(f'Найдена новая версия программы: {new_version}\nУстановить?')
                page.dialog = dlg_update_available
                open_dlg()

            def no_updates():
                dlg_update1.title = ft.Text('Информация')
                dlg_update1.content = ft.Text('У вас установлена последняя версия программы!')
                page.dialog = dlg_update1
                open_dlg()

            if current_version_major < new_version_major:
                update_available()
            elif current_version_major == new_version_major:
                if new_version_minor > current_version_minor:
                    update_available()
                else:
                    no_updates()
            else:
                no_updates()
            log_add('*' * 16)

        def install_update(e):
            log_add('*' * 16)
            log_add('Начало установки обновления')
            page.splash.visible = True
            page.update()
            global new_version
            close_dlg()
            update_url = (f"https://github.com/Skrepysh/mineSquid/releases/download/v{new_version}"
                          f"/mineSquid_v{new_version}_setup.exe")
            try:
                log_add('Скачивание...')
                os.chdir(os.environ['temp'])
                open("mineSquidUpdate.exe", "wb").write(requests.get(update_url, allow_redirects=True).content)
            except Exception:
                dlg_update1.title = ft.Text('Ошибка')
                dlg_update1.content = ft.Text('Не удалось скачать обновление')
                page.dialog = dlg_update1
                open_dlg()
                return
            log_add('Обновление скачано')
            if os.path.exists(f'{os.environ["temp"]}\\mineSquidUpdate.exe'):
                try:
                    log_add('Запускаю установку...')
                    Popen(f'{os.environ["temp"]}\\mineSquidUpdate.exe /Silent')
                    page.window_destroy()
                except Exception:
                    log_add('Не удалось установить обновление :(((')
                    dlg_update1.title = ft.Text('Ошибка')
                    dlg_update1.content = ft.Text('Не удалось установить обновление')
                    page.dialog = dlg_update1
                    open_dlg()
            else:
                log_add("Файл обновления потерялся, отмена операции")
                dlg_update1.title = ft.Text('Ошибка')
                dlg_update1.content = ft.Text('Не удалось установить обновление')
                page.dialog = dlg_update1
                open_dlg()
            log_add('*' * 16)
            page.splash.visible = False
            page.update()

        def cancel_update(e):
            log_add('Обновление отменено пользователем')
            log_add('*' * 16)
            close_dlg()

        def check_folders():
            if not os.path.exists(f"{self.userappdata}"):
                os.mkdir(self.userappdata)
            if not os.path.exists(a := f"{self.userappdata}\\modpacks"):
                os.mkdir(a)
            if not os.path.exists(a := f"{self.userappdata}\\backup"):
                os.mkdir(a)

        dlg_update1 = ft.AlertDialog(
            modal=True,
            title=ft.Text(''),
            content=ft.Text(''),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ]
        )

        dlg_update_available = ft.AlertDialog(
            modal=True,
            title=ft.Text('Информация'),
            content=ft.Text(''),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("Да", on_click=install_update),
                ft.TextButton("Нет", on_click=cancel_update),
            ]
        )

        page.appbar = ft.AppBar(
            leading=ft.Image(
                src=rf'\{self.program_directory}\mineSquid.jpg',
                width=25,
                height=25
            ),
            title=ft.Text(f'mineSquid {self.program_version}', color=ft.colors.BLACK),
            center_title=True,
            actions=[
                ft.IconButton(
                    icon=ft.icons.HELP,
                    icon_color=ft.colors.BLACK,
                    on_click=open_readme,
                    tooltip='Помощь'
                )
            ]
        )

        page.bottom_appbar = ft.BottomAppBar(
            shape=ft.NotchShape.CIRCULAR,
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.REFRESH,
                        icon_color=ft.colors.BLACK,
                        on_click=refresh,
                        tooltip="Обновить данные"
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        tooltip='Папка с модпаками',
                        icon=ft.icons.FOLDER_ZIP,
                        icon_color=ft.colors.BLACK,
                        on_click=open_mpfolder
                    ),
                    restore_btn := ft.IconButton(tooltip='Восстановить бэкап',
                                                 icon=ft.icons.RESTORE,
                                                 bgcolor=ft.colors.BLACK,
                                                 on_click=restore,
                                                 ),
                    theme_btn := ft.IconButton(icon=ft.icons.WB_SUNNY_OUTLINED,
                                               icon_color=ft.colors.BLACK,
                                               on_click=change_theme,
                                               tooltip='Сменить тему оформления'
                                               )
                ]
            )
        )
        log = ft.ListView(
            controls=[],
            auto_scroll=True
        )

        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                main_tab := ft.Tab(
                    text="Главная",
                    content=page.radio
                ),
                ft.Tab(
                    text='Лог',
                    content=log
                ),
                ft.Tab(
                    text='Настройки',
                    content=ft.ListView(
                        controls=[
                            ft.Container(padding=5),
                            ft.Row(
                                controls=[
                                    folder_field := ft.TextField(
                                        hint_text='Введите путь к папке с игрой',
                                        label='Путь к папке с игрой',
                                        value='',
                                        on_change=check_settings,
                                        error_text='',
                                        expand=True,
                                        border_color=ft.colors.GREY
                                    ),
                                    ft.ElevatedButton(
                                        text='Обзор...',
                                        width=page.window_width * 0.23,
                                        on_click=pick_folder,
                                    ),
                                ]
                            ),
                            ft.Container(padding=5),
                            ft.Row(
                                controls=[
                                    width_field := ft.TextField(
                                        label='Ширина окна',
                                        width=page.window_width // 2.5,
                                        value=page.window_width,
                                        input_filter=ft.NumbersOnlyInputFilter(),
                                        error_text='',
                                        on_change=check_settings,
                                        expand=True,
                                        border_color=ft.colors.GREY,
                                        suffix_text='px'
                                    ),
                                    ft.Text('X', size=24),
                                    height_field := ft.TextField(
                                        label='Высота окна',
                                        width=page.window_width // 2.5,
                                        value=page.window_height,
                                        input_filter=ft.NumbersOnlyInputFilter(),
                                        error_text='',
                                        on_change=check_settings,
                                        expand=True,
                                        border_color=ft.colors.GREY,
                                        suffix_text='px'
                                    ),
                                ]
                            ),
                            ft.Container(padding=5),
                            ui_color_dropdown := ft.Dropdown(
                                label='Цвет интерфейса',
                                options=[]
                            ),
                            compact_ui_checkbox := ft.Checkbox(
                                label='Компактный вид интерфейса',
                                value=True,
                                tooltip='Уменьшает расстояние между элементами интерфейса'
                            ),
                            open_dlg_mp_loaded_checkbox := ft.Checkbox(
                                label='Оповещать об успешной загрузке модпака',
                                value=False,
                                tooltip='Если включено, то после загрузки модпака будет показываться диалоговое окно'
                            ),
                            open_dlg_backup_restored_checkbox := ft.Checkbox(
                                label='Оповещать об успешном восстановлении бэкапа',
                                value=True,
                                tooltip='Если включено, '
                                        'то после восстановления бэкапа будет показываться диалоговое окно'
                            ),
                            check_current_modpack_checkbox := ft.Checkbox(
                                label='Выделять активный модпак',
                                value=False,
                                tooltip='Если включено, то программа будет '
                                        'проверять, какой из имеющихся модпаков '
                                        'сейчас находится в папке mods, и выделять его символом 👈.\n'
                                        'ВНИМАНИЕ! НЕ включайте, эту функцию, если у вас слабый ПК или медленный '
                                        'жесткий диск!'
                            ),
                            ft.Container(padding=5),
                            ft.Row(
                                controls=[
                                    apply_btn := ft.ElevatedButton(
                                        text='Применить',
                                        expand=True,
                                        on_click=apply_settings,
                                    )
                                ]
                            ),
                            ft.Container(padding=5),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        text='Проверка обновлений',
                                        expand=True,
                                        on_click=check_for_updates,
                                    ),
                                    ft.ElevatedButton(
                                        text='О программе',
                                        expand=True,
                                        on_click=about,
                                    )
                                ]
                            ),
                            ft.Container(padding=5),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        text='Сбросить настройки',
                                        color=ft.colors.RED,
                                        expand=True,
                                        on_click=open_reset_settings_dlg
                                    )
                                ]
                            ),
                            ft.Container(padding=15)  # чтобы при слишком маленькой высоте окна кнопка
                                                      # сброса настроек не перекрывалась кнопкой GO
                        ]
                    ),
                ),
            ],
            expand=1,
        )
        page.floating_action_button = ft.FloatingActionButton(
            text='GO',
            shape=ft.CircleBorder(),
            on_click=loadmp,
            tooltip='Загрузить выбранный модпак',
        )
        page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
        page.add(t)
        log_add(f'mineSquid {self.program_version} запущен')
        check_folders()
        read_config()
        check_settings()
        for e in colors:
            a = ft.dropdown.Option(text=color_names[e], key=colors[e])
            ui_color_dropdown.options.append(a)
        prepare_main_tab()


program = MineSquid(
    minesquid_version=program_version,
    minesquid_build_date=build_date
)

if __name__ == "__main__":
    ft.app(target=program.main)
