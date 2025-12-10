from tkinter import *
import tkinter.ttk as ttk
import random
import threading
import time
import os


class WindowsXPApp:
    def __init__(self):
        # Настройка Windows Classic цветов
        self.COLORS = {
            "window_bg": "#a0a0a0",  # ТЕМНО-СЕРЫЙ фон главного окна (было #f0f0f0)
            "menu_bg": "#ffffff",
            "dialog_bg": "#ece9d8",
            "button_bg": "#d4d0c8",
            "button_fg": "#000000",
            "border_light": "#c0c0c0",
            "border_dark": "#808080",
            "active_border": "#000080",
            "tab_bg": "#d4d0c8",
            "tab_active_bg": "#ece9d8",
            "label_bg": "#ece9d8",
            "label_fg": "#000000",
            "combobox_bg": "#ffffff",
            "entry_bg": "#ffffff",
            "entry_fg": "#000000",
            "listbox_bg": "#ffffff",
            "listbox_fg": "#000000",
            "radio_bg": "#ece9d8",
            "check_bg": "#ece9d8",
            "frame_bg": "#ece9d8",
            "terminal_bg": "#ffffff",
            "terminal_fg": "#000000",
            "status_bg": "#d4d0c8",
            "status_fg": "#000000",
            "indicator_gray": "#c0c0c0",
            "indicator_red": "#ff0000",
            "indicator_green": "#00ff00",
            "indicator_yellow": "#ffff00",
            "sidebar_bg": "#d4d0c8",
            "toolbar_separator": "#ffffff",  # Белый разделитель
        }

        self.FONTS = {
            "title": ("MS Sans Serif", 8, "bold"),
            "label": ("MS Sans Serif", 8),
            "button": ("MS Sans Serif", 8),
            "entry": ("Courier New", 9),
            "tab": ("MS Sans Serif", 8),
            "terminal": ("Courier New", 10),
            "status": ("MS Sans Serif", 8, "bold"),
            "indicator_small": ("MS Sans Serif", 7, "bold"),
            "indicator_large": ("MS Sans Serif", 8, "bold"),
            "sidebar_label": ("MS Sans Serif", 8, "bold"),
        }

        self.root = Tk()
        self.root.title("Windows XP Application")
        self.root.geometry("1024x768")

        # Разрешаем изменение размера главного окна
        self.root.resizable(True, True)

        # Устанавливаем минимальный размер главного окна
        self.root.minsize(800, 600)

        # Темно-серый фон главного окна
        self.root.configure(bg=self.COLORS["window_bg"])

        self.child_windows = []
        self.terminal_windows = []
        self.indicators = {}

        self.port_image = None
        self.exit_image = None
        self.save_image = None
        self.load_button_images()

        self.create_classic_menu()
        self.create_toolbar()
        self.create_main_workspace()
        self.start_window_monitor()

        # Следим за изменениями главного окна
        self.root.bind('<Configure>', self.on_root_configure)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_root_configure(self, event=None):
        """Обработчик изменения размера/положения главного окна"""
        if event and event.widget == self.root:
            # Обновляем ограничения для всех дочерних окон
            self.update_child_windows_constraints()

    def update_child_windows_constraints(self):
        """Обновление ограничений для всех дочерних окон"""
        for window in self.child_windows[:]:
            if isinstance(window, Toplevel) and window.winfo_exists():
                self.constrain_window_to_parent(window)

    def constrain_window_to_parent(self, child_window):
        """Ограничивает положение окна в пределах родительского окна"""
        if not child_window.winfo_exists():
            return

        # Получаем текущее положение главного окна
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Получаем текущее положение дочернего окна
        child_x = child_window.winfo_rootx()
        child_y = child_window.winfo_rooty()
        child_width = child_window.winfo_width()
        child_height = child_window.winfo_height()

        # Вычисляем новые координаты
        new_x = child_x
        new_y = child_y

        # Проверяем границы и корректируем положение
        changed = False

        # Левая граница
        if child_x < root_x:
            new_x = root_x
            changed = True

        # Верхняя граница
        if child_y < root_y:
            new_y = root_y
            changed = True

        # Правая граница
        if child_x + child_width > root_x + root_width:
            new_x = root_x + root_width - child_width
            changed = True

        # Нижняя граница
        if child_y + child_height > root_y + root_height:
            new_y = root_y + root_height - child_height
            changed = True

        # Если координаты изменились, перемещаем окно
        if changed:
            # Преобразуем координаты из экранных в относительные
            screen_x = new_x
            screen_y = new_y
            child_window.geometry(f"+{screen_x}+{screen_y}")

    def load_button_images(self):
        """Загрузка изображений для кнопок"""
        try:
            port_image_path = "images/port.png"
            if os.path.exists(port_image_path):
                self.port_image = PhotoImage(file=port_image_path)
                print(f"Изображение порта успешно загружено: {port_image_path}")
            else:
                print(f"Файл изображения порта не найден: {port_image_path}")
                self.port_image = None
        except Exception as e:
            print(f"Ошибка при загрузке изображения порта: {e}")
            self.port_image = None

        try:
            exit_image_path = "images/exit.png"
            if os.path.exists(exit_image_path):
                self.exit_image = PhotoImage(file=exit_image_path)
                print(f"Изображение выхода успешно загружено: {exit_image_path}")
            else:
                print(f"Файл изображения выхода не найден: {exit_image_path}")
                self.exit_image = None
        except Exception as e:
            print(f"Ошибка при загрузке изображения выхода: {e}")
            self.exit_image = None

        try:
            save_image_path = "images/save.png"
            if os.path.exists(save_image_path):
                self.save_image = PhotoImage(file=save_image_path)
                print(f"Изображение сохранения успешно загружено: {save_image_path}")
            else:
                print(f"Файл изображения сохранения не найден: {save_image_path}")
                self.save_image = None
        except Exception as e:
            print(f"Ошибка при загрузке изображения сохранения: {e}")
            self.save_image = None

    def create_classic_menu(self):
        """Создание классического меню Windows XP"""
        menubar = Menu(self.root,
                       bg=self.COLORS["menu_bg"],
                       fg="black",
                       activebackground="#000080",
                       activeforeground="#ffffff",
                       relief=FLAT)
        self.root.config(menu=menubar)

        profile_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        profile_menu.add_command(label="New Profile")
        profile_menu.add_command(label="Open Profile...")
        profile_menu.add_command(label="Save Profile", command=self.save_settings)
        profile_menu.add_separator()
        profile_menu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="Profile", menu=profile_menu)

        edit_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        port_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        port_menu.add_command(label="Open", command=self.show_property_dialog)
        menubar.add_cascade(label="Port Manager", menu=port_menu)

        window_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        window_menu.add_command(label="New Window")
        menubar.add_cascade(label="Window", menu=window_menu)

        help_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

    def create_toolbar(self):
        """Панель инструментов с изображениями кнопок и белым разделителем"""
        toolbar = Frame(self.root, bg=self.COLORS["window_bg"], height=32)
        toolbar.pack(fill=X, side=TOP, padx=0, pady=0)

        # Фрейм для кнопок
        buttons_frame = Frame(toolbar, bg=self.COLORS["window_bg"], height=30)
        buttons_frame.pack(fill=X, side=TOP, padx=2, pady=2)

        if self.port_image:
            settings_btn = Button(buttons_frame,
                                  image=self.port_image,
                                  bg=self.COLORS["button_bg"],
                                  fg=self.COLORS["button_fg"],
                                  relief=RAISED,
                                  borderwidth=1,
                                  command=self.show_property_dialog)
            settings_btn.pack(side=LEFT, padx=2)
            self.create_tooltip(settings_btn, "Communication Settings")
        else:
            settings_btn = Button(buttons_frame,
                                  text="Settings",
                                  bg=self.COLORS["button_bg"],
                                  fg=self.COLORS["button_fg"],
                                  font=self.FONTS["button"],
                                  relief=RAISED,
                                  borderwidth=1,
                                  command=self.show_property_dialog)
            settings_btn.pack(side=LEFT, padx=2)

        if self.save_image:
            save_btn = Button(buttons_frame,
                              image=self.save_image,
                              bg=self.COLORS["button_bg"],
                              fg=self.COLORS["button_fg"],
                              relief=RAISED,
                              borderwidth=1,
                              command=self.save_settings)
            save_btn.pack(side=LEFT, padx=2)
            self.create_tooltip(save_btn, "Save Settings")
        else:
            save_btn = Button(buttons_frame,
                              text="Save",
                              bg=self.COLORS["button_bg"],
                              fg=self.COLORS["button_fg"],
                              font=self.FONTS["button"],
                              relief=RAISED,
                              borderwidth=1,
                              command=self.save_settings)
            save_btn.pack(side=LEFT, padx=2)

        if self.exit_image:
            exit_btn = Button(buttons_frame,
                              image=self.exit_image,
                              bg=self.COLORS["button_bg"],
                              fg=self.COLORS["button_fg"],
                              relief=RAISED,
                              borderwidth=1,
                              command=self.on_close)
            exit_btn.pack(side=LEFT, padx=2)
            self.create_tooltip(exit_btn, "Exit Application")
        else:
            exit_btn = Button(buttons_frame,
                              text="Exit",
                              bg=self.COLORS["button_bg"],
                              fg=self.COLORS["button_fg"],
                              font=self.FONTS["button"],
                              relief=RAISED,
                              borderwidth=1,
                              command=self.on_close)
            exit_btn.pack(side=LEFT, padx=2)

        # Белый разделитель под панелью инструментов
        separator = Frame(toolbar,
                          bg=self.COLORS["toolbar_separator"],
                          height=1)
        separator.pack(fill=X, side=BOTTOM, padx=0, pady=0)

    def save_settings(self):
        """Сохранение настроек"""
        print("Settings saved to file")

    def create_tooltip(self, widget, text):
        """Создание всплывающей подсказки для кнопки с изображением"""

        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25

            self.tooltip = Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")

            label = Label(self.tooltip,
                          text=text,
                          background="#ffffe0",
                          relief=SOLID,
                          borderwidth=1,
                          font=("Tahoma", 8))
            label.pack()

        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)



    def create_main_workspace(self):
        """Рабочая область"""
        workspace = Frame(self.root, bg=self.COLORS["window_bg"])
        workspace.pack(fill=BOTH, expand=True, padx=8, pady=8)

        label = Label(workspace,
                      text="",
                      bg=self.COLORS["window_bg"],
                      fg="black",
                      font=("MS Sans Serif", 10))
        label.pack(pady=20)

    def show_property_dialog(self):
        """Создание диалогового окна свойств в стиле Win2000/XP"""
        dialog = Toplevel(self.root)
        dialog.title("Open")
        dialog.geometry("500x500")

        # Разрешаем изменение размера диалогового окна
        dialog.resizable(True, True)

        # Устанавливаем минимальный размер
        dialog.minsize(400, 400)

        # Делаем окно поверх главного
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.configure(bg=self.COLORS["dialog_bg"])

        # Привязываем обработчики для контроля положения окна
        dialog.bind('<Configure>', lambda e: self.on_child_configure(dialog))
        dialog.bind('<Map>', lambda e: self.on_child_map(dialog))  # Когда окно становится видимым

        outer_frame = Frame(dialog,
                            bg=self.COLORS["border_dark"],
                            borderwidth=1,
                            relief=SOLID)
        outer_frame.pack(fill=BOTH, expand=True, padx=1, pady=1)

        main_frame = Frame(outer_frame,
                           bg=self.COLORS["dialog_bg"],
                           borderwidth=0)
        main_frame.pack(fill=BOTH, expand=True, padx=1, pady=1)

        self.create_tabs_win2000(main_frame)
        self.create_dialog_buttons(main_frame, dialog)

        self.child_windows.append(dialog)

        # Позиционируем окно относительно родительского
        self.position_window_near_parent(dialog)

        dialog.protocol("WM_DELETE_WINDOW", lambda: self.close_child_window(dialog))

    def on_child_configure(self, child_window):
        """Обработчик изменения размера/положения дочернего окна"""
        if child_window.winfo_exists():
            self.constrain_window_to_parent(child_window)

    def on_child_map(self, child_window):
        """Обработчик, когда дочернее окно становится видимым"""
        if child_window.winfo_exists():
            # Поднимаем дочернее окно на передний план
            child_window.lift()
            # Принудительно обновляем ограничения
            self.constrain_window_to_parent(child_window)

    def position_window_near_parent(self, window):
        """Позиционирует окно рядом с родительским окном"""
        window.update_idletasks()

        # Получаем размеры окна
        width = window.winfo_width()
        height = window.winfo_height()

        # Получаем положение и размеры родительского окна
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Вычисляем позицию для размещения окна рядом с родительским
        x = root_x + root_width - width - 50
        y = root_y + 50

        # Если окно не помещается справа, размещаем слева
        if x < root_x:
            x = root_x + 50

        # Если окно не помещается снизу, сдвигаем выше
        if y + height > root_y + root_height:
            y = root_y + root_height - height - 50

        # Устанавливаем положение окна (используем абсолютные координаты экрана)
        window.geometry(f"+{x}+{y}")

    def create_tabs_win2000(self, parent):
        """Создание вкладок в стиле Windows 2000"""
        tab_frame = Frame(parent, bg=self.COLORS["dialog_bg"])
        tab_frame.pack(fill=X, padx=8, pady=(8, 0))

        tabs = ["Communication Parameter", "Terminal", "File Transfer", "Capturing"]

        self.tab_content = Frame(parent,
                                 bg=self.COLORS["dialog_bg"],
                                 relief=SUNKEN,
                                 borderwidth=1)
        self.tab_content.pack(fill=BOTH, expand=True, padx=8, pady=8)

        self.tab_contents = {}

        self.create_communication_tab()

        for tab_name in tabs[1:]:
            frame = Frame(self.tab_content, bg=self.COLORS["dialog_bg"])
            self.tab_contents[tab_name] = frame
            Label(frame,
                  text=f"{tab_name} Settings",
                  bg=self.COLORS["dialog_bg"],
                  fg="black",
                  font=self.FONTS["title"]).pack(pady=20)
            Label(frame,
                  text="This tab is under construction",
                  bg=self.COLORS["dialog_bg"],
                  fg="gray",
                  font=self.FONTS["label"]).pack()

        for i, tab_name in enumerate(tabs):
            btn = Button(tab_frame,
                         text=tab_name,
                         bg=self.COLORS["tab_bg"],
                         fg=self.COLORS["label_fg"],
                         font=self.FONTS["tab"],
                         relief=RAISED,
                         borderwidth=1,
                         padx=10,
                         pady=3,
                         command=lambda name=tab_name: self.switch_tab(name))
            btn.pack(side=LEFT, padx=(0, 1))

            if i == 0:
                btn.config(relief=SUNKEN, bg=self.COLORS["tab_active_bg"])
                self.current_tab = tab_name
                self.tab_contents[tab_name].pack(fill=BOTH, expand=True)

    def switch_tab(self, tab_name):
        """Переключение вкладок"""
        self.tab_contents[self.current_tab].pack_forget()

        for widget in self.tab_content.master.children.values():
            if isinstance(widget, Button):
                if widget.cget("text") == tab_name:
                    widget.config(relief=SUNKEN, bg=self.COLORS["tab_active_bg"])
                elif widget.cget("text") == self.current_tab:
                    widget.config(relief=RAISED, bg=self.COLORS["tab_bg"])

        self.current_tab = tab_name
        self.tab_contents[tab_name].pack(fill=BOTH, expand=True)

    def create_communication_tab(self):
        """Создание вкладки Communication Parameter с новой структурой"""
        frame = Frame(self.tab_content, bg=self.COLORS["dialog_bg"])
        self.tab_contents["Communication Parameter"] = frame

        # Protocol selection
        protocol_frame = Frame(frame, bg=self.COLORS["dialog_bg"])
        protocol_frame.pack(fill=X, padx=10, pady=(10, 5))

        Label(protocol_frame,
              text="Protocol:",
              bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"],
              font=self.FONTS["label"],
              width=15,
              anchor=W).pack(side=LEFT)

        self.protocol_var = StringVar(value="Serial")
        protocol_combo = ttk.Combobox(protocol_frame,
                                      textvariable=self.protocol_var,
                                      values=["Serial", "TCP", "UDP"],
                                      state="readonly",
                                      width=15)
        protocol_combo.pack(side=LEFT, padx=(0, 20))

        # Frame for Serial Parameters with thin border
        serial_frame = Frame(frame,
                             bg=self.COLORS["dialog_bg"],
                             relief=SUNKEN,
                             borderwidth=1)
        serial_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Title for Serial Parameters
        serial_title_frame = Frame(serial_frame, bg=self.COLORS["dialog_bg"])
        serial_title_frame.pack(fill=X, padx=5, pady=5)

        serial_title = Label(serial_title_frame,
                             text="Serial Parameters",
                             bg=self.COLORS["dialog_bg"],
                             fg=self.COLORS["label_fg"],
                             font=self.FONTS["title"])
        serial_title.pack(side=LEFT)

        # Main content frame for serial parameters
        content_frame = Frame(serial_frame, bg=self.COLORS["dialog_bg"])
        content_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Left column - Port selection
        left_frame = Frame(content_frame, bg=self.COLORS["dialog_bg"], width=100)
        left_frame.pack(side=LEFT, fill=Y, padx=(0, 20))

        # Port selection label
        port_label = Label(left_frame,
                           text="Port:",
                           bg=self.COLORS["dialog_bg"],
                           fg=self.COLORS["label_fg"],
                           font=self.FONTS["label"])
        port_label.pack(anchor=W, pady=(0, 5))

        # Create listbox for port selection
        port_listbox_frame = Frame(left_frame, bg=self.COLORS["dialog_bg"])
        port_listbox_frame.pack(fill=BOTH, expand=True)

        # Create scrollbar for port listbox
        scrollbar = Scrollbar(port_listbox_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create listbox
        self.port_listbox = Listbox(port_listbox_frame,
                                    bg=self.COLORS["listbox_bg"],
                                    fg=self.COLORS["listbox_fg"],
                                    font=self.FONTS["label"],
                                    yscrollcommand=scrollbar.set,
                                    height=8,
                                    selectbackground="#000080",
                                    selectforeground="#ffffff")

  
        self.port_listbox.insert(END, f"COM{1}")
        self.port_listbox.insert(END, f"COM{2}")

        # Select first port by default
        self.port_listbox.selection_set(0)
        self.port_listbox.see(0)

        self.port_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.port_listbox.yview)

        # Right column - Parameters
        right_frame = Frame(content_frame, bg=self.COLORS["dialog_bg"])
        right_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Baud Rate selection
        baud_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        baud_frame.pack(fill=X, pady=(0, 5))

        Label(baud_frame,
              text="Baud Rate:",
              bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"],
              font=self.FONTS["label"],
              width=15,
              anchor=W).pack(side=LEFT)

        self.baud_var = StringVar(value="9600")
        baud_combo = ttk.Combobox(baud_frame,
                                  textvariable=self.baud_var,
                                  values=["9600", "19200", "38400", "57600", "115200"],
                                  state="readonly",
                                  width=15)
        baud_combo.pack(side=LEFT, padx=(0, 10))

        # User defined checkbox (под Baud Rate)
        self.user_defined_var = BooleanVar(value=False)
        user_defined_check = Checkbutton(baud_frame,
                                         text="User defined",
                                         variable=self.user_defined_var,
                                         bg=self.COLORS["check_bg"],
                                         fg=self.COLORS["label_fg"],
                                         font=self.FONTS["label"])
        user_defined_check.pack(side=LEFT)

        # Data bits selection
        data_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        data_frame.pack(fill=X, pady=(0, 10))

        Label(data_frame,
              text="Data bits:",
              bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"],
              font=self.FONTS["label"],
              width=15,
              anchor=W).pack(side=LEFT)

        self.data_var = StringVar(value="8")
        data_combo = ttk.Combobox(data_frame,
                                  textvariable=self.data_var,
                                  values=["5", "6", "7", "8"],
                                  state="readonly",
                                  width=15)
        data_combo.pack(side=LEFT)

        # Parity selection
        parity_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        parity_frame.pack(fill=X, pady=(0, 10))

        Label(parity_frame,
              text="Parity:",
              bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"],
              font=self.FONTS["label"],
              width=15,
              anchor=W).pack(side=LEFT)

        self.parity_var = StringVar(value="None")
        parity_combo = ttk.Combobox(parity_frame,
                                    textvariable=self.parity_var,
                                    values=["None", "Even", "Odd", "Mark", "Space"],
                                    state="readonly",
                                    width=15)
        parity_combo.pack(side=LEFT)

        # Stop bits selection
        stop_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        stop_frame.pack(fill=X, pady=(0, 10))

        Label(stop_frame,
              text="Stop bits:",
              bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"],
              font=self.FONTS["label"],
              width=15,
              anchor=W).pack(side=LEFT)

        self.stop_var = StringVar(value="1")
        stop_combo = ttk.Combobox(stop_frame,
                                  textvariable=self.stop_var,
                                  values=["1", "1.5", "2"],
                                  state="readonly",
                                  width=15)
        stop_combo.pack(side=LEFT)

        # Flow control
        flow_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        flow_frame.pack(fill=X, pady=(0, 10))

        Label(flow_frame,
              text="Flow control:",
              bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"],
              font=self.FONTS["label"],
              width=15,
              anchor=W).pack(side=LEFT, anchor=N, pady=5)

        flow_control_frame = Frame(flow_frame, bg=self.COLORS["dialog_bg"])
        flow_control_frame.pack(side=LEFT, fill=X, expand=True)

        # Радиокнопки для Flow control
        self.flow_var = StringVar(value="RTS/CTS")

        radio1 = Radiobutton(flow_control_frame,
                             text="RTS/CTS",
                             variable=self.flow_var,
                             value="RTS/CTS",
                             bg=self.COLORS["radio_bg"],
                             fg=self.COLORS["label_fg"],
                             font=self.FONTS["label"],
                             anchor=W)
        radio1.pack(fill=X, pady=1)

        radio2 = Radiobutton(flow_control_frame,
                             text="DTR/DSR",
                             variable=self.flow_var,
                             value="DTR/DSR",
                             bg=self.COLORS["radio_bg"],
                             fg=self.COLORS["label_fg"],
                             font=self.FONTS["label"],
                             anchor=W)
        radio2.pack(fill=X, pady=1)

        radio3 = Radiobutton(flow_control_frame,
                             text="XON/XOFF",
                             variable=self.flow_var,
                             value="XON/XOFF",
                             bg=self.COLORS["radio_bg"],
                             fg=self.COLORS["label_fg"],
                             font=self.FONTS["label"],
                             anchor=W)
        radio3.pack(fill=X, pady=1)

        # RTS и DTR состояния - друг под другом с радиокнопками ON/OFF
        state_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        state_frame.pack(fill=X, pady=(10, 0))

        # RTS state frame
        rts_frame = Frame(state_frame, bg=self.COLORS["dialog_bg"])
        rts_frame.pack(fill=X, pady=(0, 5))

        Label(rts_frame,
              text="RTS state:",
              bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"],
              font=self.FONTS["label"],
              width=15,
              anchor=W).pack(side=LEFT)

        rts_state_frame = Frame(rts_frame, bg=self.COLORS["dialog_bg"])
        rts_state_frame.pack(side=LEFT)

        self.rts_var = StringVar(value="ON")

        rts_on = Radiobutton(rts_state_frame,
                             text="ON",
                             variable=self.rts_var,
                             value="ON",
                             bg=self.COLORS["radio_bg"],
                             fg=self.COLORS["label_fg"],
                             font=self.FONTS["label"])
        rts_on.pack(side=LEFT, padx=(0, 10))

        rts_off = Radiobutton(rts_state_frame,
                              text="OFF",
                              variable=self.rts_var,
                              value="OFF",
                              bg=self.COLORS["radio_bg"],
                              fg=self.COLORS["label_fg"],
                              font=self.FONTS["label"])
        rts_off.pack(side=LEFT)

        # DTR state frame
        dtr_frame = Frame(state_frame, bg=self.COLORS["dialog_bg"])
        dtr_frame.pack(fill=X)

        Label(dtr_frame,
              text="DTR state:",
              bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"],
              font=self.FONTS["label"],
              width=15,
              anchor=W).pack(side=LEFT)

        dtr_state_frame = Frame(dtr_frame, bg=self.COLORS["dialog_bg"])
        dtr_state_frame.pack(side=LEFT)

        self.dtr_var = StringVar(value="ON")

        dtr_on = Radiobutton(dtr_state_frame,
                             text="ON",
                             variable=self.dtr_var,
                             value="ON",
                             bg=self.COLORS["radio_bg"],
                             fg=self.COLORS["label_fg"],
                             font=self.FONTS["label"])
        dtr_on.pack(side=LEFT, padx=(0, 10))

        dtr_off = Radiobutton(dtr_state_frame,
                              text="OFF",
                              variable=self.dtr_var,
                              value="OFF",
                              bg=self.COLORS["radio_bg"],
                              fg=self.COLORS["label_fg"],
                              font=self.FONTS["label"])
        dtr_off.pack(side=LEFT)

    def create_dialog_buttons(self, parent, dialog):
        """Создание кнопок внизу диалогового окна"""
        button_frame = Frame(parent, bg=self.COLORS["dialog_bg"])
        button_frame.pack(fill=X, padx=8, pady=(0, 8))

        spacer = Frame(button_frame, bg=self.COLORS["dialog_bg"])
        spacer.pack(side=LEFT, expand=True)

        default_btn = Button(button_frame,
                             text="Default",
                             bg=self.COLORS["button_bg"],
                             fg=self.COLORS["button_fg"],
                             font=self.FONTS["button"],
                             width=10,
                             height=1,
                             relief=RAISED,
                             borderwidth=1)
        default_btn.pack(side=LEFT, padx=2)

        cancel_btn = Button(button_frame,
                            text="Cancel",
                            bg=self.COLORS["button_bg"],
                            fg=self.COLORS["button_fg"],
                            font=self.FONTS["button"],
                            width=10,
                            height=1,
                            relief=RAISED,
                            borderwidth=1,
                            command=dialog.destroy)
        cancel_btn.pack(side=LEFT, padx=2)

        ok_btn = Button(button_frame,
                        text="OK",
                        bg=self.COLORS["button_bg"],
                        fg=self.COLORS["button_fg"],
                        font=self.FONTS["button"],
                        width=10,
                        height=1,
                        relief=RAISED,
                        borderwidth=1,
                        command=lambda: self.apply_settings(dialog))
        ok_btn.pack(side=LEFT, padx=2)

        dialog.bind('<Return>', lambda e: self.apply_settings(dialog))

    def apply_settings(self, dialog):
        """Применение настроек и открытие терминала"""
        selection = self.port_listbox.curselection()
        if selection:
            selected_port = self.port_listbox.get(selection[0])
        else:
            selected_port = "COM1"

        print("Settings applied")
        print(f"Protocol: {self.protocol_var.get()}")
        print(f"Port: {selected_port}")
        print(f"Baud rate: {self.baud_var.get()}")
        print(f"User defined: {self.user_defined_var.get()}")
        print(f"Data bits: {self.data_var.get()}")
        print(f"Parity: {self.parity_var.get()}")
        print(f"Stop bits: {self.stop_var.get()}")
        print(f"Flow control: {self.flow_var.get()}")
        print(f"RTS state: {self.rts_var.get()}")
        print(f"DTR state: {self.dtr_var.get()}")

        self.selected_port_for_terminal = selected_port
        dialog.destroy()
        self.open_terminal_window()

    def open_terminal_window(self):
        """Открытие окна терминала"""
        terminal = Toplevel(self.root)
        terminal.title(f"Terminal - {self.selected_port_for_terminal}")
        terminal.geometry("700x500")

        # Разрешаем изменение размера терминала
        terminal.resizable(True, True)

        # Устанавливаем минимальный размер терминала
        terminal.minsize(600, 400)

        # Сохраняем ссылку на окно терминала
        terminal_data = {
            'window': terminal,
            'indicators': {}
        }
        self.terminal_windows.append(terminal_data)

        # Делаем окно поверх главного
        terminal.transient(self.root)

        terminal.configure(bg=self.COLORS["terminal_bg"])

        # Привязываем обработчики для контроля положения окна
        terminal.bind('<Configure>', lambda e: self.on_child_configure(terminal))
        terminal.bind('<Map>', lambda e: self.on_child_map(terminal))

        outer_frame = Frame(terminal,
                            bg=self.COLORS["border_dark"],
                            borderwidth=1,
                            relief=SOLID)
        outer_frame.pack(fill=BOTH, expand=True, padx=1, pady=1)

        main_frame = Frame(outer_frame,
                           bg=self.COLORS["terminal_bg"],
                           borderwidth=0)
        main_frame.pack(fill=BOTH, expand=True, padx=1, pady=1)

        title_frame = Frame(main_frame, bg=self.COLORS["terminal_bg"], height=25)
        title_frame.pack(fill=X, side=TOP, pady=(3, 3))
        title_frame.pack_propagate(False)

        Label(title_frame,
              text=f"Terminal: {self.selected_port_for_terminal} | Protocol: {self.protocol_var.get()} | Baud: {self.baud_var.get()}",
              bg=self.COLORS["terminal_bg"],
              fg=self.COLORS["terminal_fg"],
              font=self.FONTS["title"]).pack(side=LEFT, padx=8)

        content_frame = Frame(main_frame, bg=self.COLORS["terminal_bg"])
        content_frame.pack(fill=BOTH, expand=True, pady=(0, 8))

        # Левая часть - боковая панель с индикаторами
        sidebar_frame = Frame(content_frame,
                              bg=self.COLORS["sidebar_bg"],
                              width=55,
                              relief=SUNKEN,
                              borderwidth=1)
        sidebar_frame.pack(side=LEFT, fill=Y, padx=(8, 4))
        sidebar_frame.pack_propagate(False)

        sidebar_title_frame = Frame(sidebar_frame,
                                    bg=self.COLORS["sidebar_bg"],
                                    height=18)
        sidebar_title_frame.pack(fill=X, side=TOP)
        sidebar_title_frame.pack_propagate(False)

        sidebar_title = Label(sidebar_title_frame,
                              text="CTRL",
                              bg=self.COLORS["sidebar_bg"],
                              fg=self.COLORS["status_fg"],
                              font=("MS Sans Serif", 6, "bold"))
        sidebar_title.pack(pady=1)

        indicators_container = Frame(sidebar_frame,
                                     bg=self.COLORS["sidebar_bg"])
        indicators_container.pack(fill=BOTH, expand=True, padx=2, pady=2)

        # Красный индикатор (SIG)
        red_container = Frame(indicators_container,
                              bg=self.COLORS["sidebar_bg"])
        red_container.pack(side=TOP, pady=(0, 4))

        red_label = Label(red_container,
                          text="SIG",
                          bg=self.COLORS["sidebar_bg"],
                          fg=self.COLORS["status_fg"],
                          font=("MS Sans Serif", 5, "bold"))
        red_label.pack()

        red_indicator = Label(red_container,
                              text="",
                              bg=self.COLORS["indicator_red"],
                              width=4,
                              height=1,
                              relief=SUNKEN,
                              borderwidth=1)
        red_indicator.pack(pady=(0, 0))

        # Сохраняем ссылку на индикатор
        terminal_data['indicators']['sig'] = red_indicator

        # Индикатор RTS
        rts_container = Frame(indicators_container,
                              bg=self.COLORS["sidebar_bg"])
        rts_container.pack(side=TOP, pady=(0, 4))

        rts_label = Label(rts_container,
                          text="RTS",
                          bg=self.COLORS["sidebar_bg"],
                          fg=self.COLORS["status_fg"],
                          font=("MS Sans Serif", 5, "bold"))
        rts_label.pack()

        rts_indicator = Label(rts_container,
                              text="",
                              bg=self.COLORS["indicator_gray"],
                              width=4,
                              height=1,
                              relief=SUNKEN,
                              borderwidth=1)
        rts_indicator.pack(pady=(0, 0))

        terminal_data['indicators']['rts'] = rts_indicator

        # Индикатор DTR
        dtr_container = Frame(indicators_container,
                              bg=self.COLORS["sidebar_bg"])
        dtr_container.pack(side=TOP, pady=(0, 0))

        dtr_label = Label(dtr_container,
                          text="DTR",
                          bg=self.COLORS["sidebar_bg"],
                          fg=self.COLORS["status_fg"],
                          font=("MS Sans Serif", 5, "bold"))
        dtr_label.pack()

        dtr_indicator = Label(dtr_container,
                              text="",
                              bg=self.COLORS["indicator_gray"],
                              width=4,
                              height=1,
                              relief=SUNKEN,
                              borderwidth=1)
        dtr_indicator.pack(pady=(0, 0))

        terminal_data['indicators']['dtr'] = dtr_indicator

        sidebar_spacer = Frame(indicators_container,
                               bg=self.COLORS["sidebar_bg"])
        sidebar_spacer.pack(side=TOP, fill=BOTH, expand=True)

        # Правая часть - терминал
        terminal_frame = Frame(content_frame, bg=self.COLORS["terminal_bg"])
        terminal_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 8))

        # Область вывода терминала
        output_frame = Frame(terminal_frame,
                             bg=self.COLORS["terminal_bg"],
                             relief=SUNKEN,
                             borderwidth=1)
        output_frame.pack(fill=BOTH, expand=True)

        # Текстовое поле для вывода
        text_widget = Text(output_frame,
                           bg=self.COLORS["terminal_bg"],
                           fg=self.COLORS["terminal_fg"],
                           font=self.FONTS["terminal"],
                           wrap=WORD,
                           relief=FLAT)

        scrollbar = Scrollbar(output_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_widget.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        settings_text = f"""Terminal opened with settings:
Port: {self.selected_port_for_terminal}
Protocol: {self.protocol_var.get()}
Baud rate: {self.baud_var.get()}
Data bits: {self.data_var.get()}
Parity: {self.parity_var.get()}
Stop bits: {self.stop_var.get()}
Flow control: {self.flow_var.get()}
RTS state: {self.rts_var.get()}
DTR state: {self.dtr_var.get()}

Ready for communication...
Type commands like: cts=green, dsr=red, ri=yellow, dcd=green, sig=green, rts=green, dtr=green
"""

        text_widget.insert(END, settings_text)
        text_widget.configure(state='disabled')

        # Поле ввода для команд
        input_frame = Frame(terminal_frame, bg=self.COLORS["terminal_bg"], height=30)
        input_frame.pack(fill=X, side=BOTTOM, pady=(5, 0))
        input_frame.pack_propagate(False)

        Label(input_frame,
              text="Command:",
              bg=self.COLORS["terminal_bg"],
              fg=self.COLORS["terminal_fg"],
              font=self.FONTS["label"]).pack(side=LEFT, padx=(0, 5))

        command_entry = Entry(input_frame,
                              bg=self.COLORS["entry_bg"],
                              fg=self.COLORS["entry_fg"],
                              font=self.FONTS["entry"],
                              width=40)
        command_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

        # Кнопка для выполнения команды
        def execute_command():
            command = command_entry.get().strip().lower()
            if command:
                self.process_command(command, terminal_data, text_widget)
                command_entry.delete(0, END)

        execute_btn = Button(input_frame,
                             text="Execute",
                             bg=self.COLORS["button_bg"],
                             fg=self.COLORS["button_fg"],
                             font=self.FONTS["button"],
                             command=execute_command)
        execute_btn.pack(side=LEFT)

        # Привязываем Enter к выполнению команды
        command_entry.bind('<Return>', lambda e: execute_command())

        # Панель управления
        control_frame = Frame(main_frame, bg=self.COLORS["terminal_bg"], height=35)
        control_frame.pack(fill=X, side=BOTTOM, pady=(0, 3))
        control_frame.pack_propagate(False)

        Button(control_frame,
               text="Clear",
               bg=self.COLORS["button_bg"],
               fg=self.COLORS["button_fg"],
               font=self.FONTS["button"],
               command=lambda: self.clear_terminal(text_widget)).pack(side=LEFT, padx=8)

        Button(control_frame,
               text="Close",
               bg=self.COLORS["button_bg"],
               fg=self.COLORS["button_fg"],
               font=self.FONTS["button"],
               command=terminal.destroy).pack(side=RIGHT, padx=8)

        # Создаем статус-панель
        self.create_status_panel_win2000(main_frame, terminal_data)

        self.child_windows.append(terminal)

        # Позиционируем окно относительно родительского
        self.position_window_near_parent(terminal)

        terminal.protocol("WM_DELETE_WINDOW", lambda: self.close_child_window(terminal))

    def process_command(self, command, terminal_data, text_widget):
        """Обработка команд для изменения цвета индикаторов"""
        text_widget.configure(state='normal')
        text_widget.insert(END, f"\n> {command}\n")

        # Парсим команду
        parts = command.split('=')
        if len(parts) == 2:
            indicator = parts[0].strip()
            color = parts[1].strip()

            # Определяем цвет
            color_map = {
                'red': self.COLORS["indicator_red"],
                'green': self.COLORS["indicator_green"],
                'yellow': self.COLORS["indicator_yellow"],
                'gray': self.COLORS["indicator_gray"],
                'grey': self.COLORS["indicator_gray"]
            }

            if color in color_map:
                target_color = color_map[color]

                # Меняем цвет индикатора в боковой панели
                if indicator in terminal_data['indicators']:
                    terminal_data['indicators'][indicator].config(bg=target_color)
                    text_widget.insert(END, f"Changed {indicator.upper()} to {color}\n")

                # Меняем цвет индикатора в статус-панели
                if hasattr(self, 'status_indicators'):
                    if indicator in self.status_indicators:
                        self.status_indicators[indicator].config(bg=target_color)
                        text_widget.insert(END, f"Changed status {indicator.upper()} to {color}\n")

                # Специальные команды
                if indicator == 'all':
                    for ind in terminal_data['indicators'].values():
                        ind.config(bg=target_color)
                    if hasattr(self, 'status_indicators'):
                        for ind in self.status_indicators.values():
                            ind.config(bg=target_color)
                    text_widget.insert(END, f"Changed ALL indicators to {color}\n")
            else:
                text_widget.insert(END, f"Unknown color: {color}. Use red, green, yellow, or gray\n")
        else:
            text_widget.insert(END, "Invalid command format. Use: indicator=color\n")
            text_widget.insert(END, "Example: cts=green, rts=red, all=yellow\n")

        text_widget.see(END)
        text_widget.configure(state='disabled')

    def create_status_panel_win2000(self, parent, terminal_data):
        """Создание статус-панели с индикаторами"""
        status_panel = Frame(parent,
                             bg=self.COLORS["border_dark"],
                             borderwidth=1,
                             relief=SUNKEN,
                             height=20)
        status_panel.pack(fill=X, side=BOTTOM, padx=2, pady=2)
        status_panel.pack_propagate(False)

        status_content = Frame(status_panel,
                               bg=self.COLORS["status_bg"],
                               borderwidth=0)
        status_content.pack(fill=BOTH, expand=True, padx=1, pady=1)

        # Ячейка состояния
        state_cell = Frame(status_content,
                           bg=self.COLORS["status_bg"],
                           relief=RAISED,
                           borderwidth=1)
        state_cell.pack(side=LEFT, padx=(2, 0), pady=1)

        state_label = Label(state_cell,
                            text="State: OPEN",
                            bg=self.COLORS["status_bg"],
                            fg=self.COLORS["status_fg"],
                            font=("MS Sans Serif", 7, "bold"),
                            width=10,
                            anchor=W)
        state_label.pack(side=LEFT, padx=3, pady=1)

        # Индикаторы
        indicators_frame = Frame(status_content,
                                 bg=self.COLORS["status_bg"])
        indicators_frame.pack(side=LEFT, padx=(4, 0))

        # Создаем словарь для хранения индикаторов статус-панели
        self.status_indicators = {}

        # Индикатор CTS
        cts_frame = Frame(indicators_frame,
                          bg=self.COLORS["status_bg"])
        cts_frame.pack(side=LEFT, padx=(0, 2))

        cts_indicator = Label(cts_frame,
                              text="CTS",
                              bg=self.COLORS["indicator_gray"],
                              fg="black",
                              font=("MS Sans Serif", 6, "bold"),
                              width=4,
                              height=1,
                              relief=SUNKEN,
                              borderwidth=1)
        cts_indicator.pack(padx=1, pady=1)
        self.status_indicators['cts'] = cts_indicator

        # Индикатор DSR
        dsr_frame = Frame(indicators_frame,
                          bg=self.COLORS["status_bg"])
        dsr_frame.pack(side=LEFT, padx=(0, 2))

        dsr_indicator = Label(dsr_frame,
                              text="DSR",
                              bg=self.COLORS["indicator_red"],
                              fg="black",
                              font=("MS Sans Serif", 6, "bold"),
                              width=4,
                              height=1,
                              relief=SUNKEN,
                              borderwidth=1)
        dsr_indicator.pack(padx=1, pady=1)
        self.status_indicators['dsr'] = dsr_indicator

        # Индикатор RI
        ri_frame = Frame(indicators_frame,
                         bg=self.COLORS["status_bg"])
        ri_frame.pack(side=LEFT, padx=(0, 2))

        ri_indicator = Label(ri_frame,
                             text="RI",
                             bg=self.COLORS["indicator_gray"],
                             fg="black",
                             font=("MS Sans Serif", 6, "bold"),
                             width=4,
                             height=1,
                             relief=SUNKEN,
                             borderwidth=1)
        ri_indicator.pack(padx=1, pady=1)
        self.status_indicators['ri'] = ri_indicator

        # Индикатор DCD
        dcd_frame = Frame(indicators_frame,
                          bg=self.COLORS["status_bg"])
        dcd_frame.pack(side=LEFT, padx=(0, 4))

        dcd_indicator = Label(dcd_frame,
                              text="DCD",
                              bg=self.COLORS["indicator_gray"],
                              fg="black",
                              font=("MS Sans Serif", 6, "bold"),
                              width=4,
                              height=1,
                              relief=SUNKEN,
                              borderwidth=1)
        dcd_indicator.pack(padx=1, pady=1)
        self.status_indicators['dcd'] = dcd_indicator

        # Текстовые ячейки справа
        ready_cell = Frame(status_content,
                           bg=self.COLORS["status_bg"],
                           relief=RAISED,
                           borderwidth=1)
        ready_cell.pack(side=LEFT, padx=(0, 3), pady=1)

        ready_label = Label(ready_cell,
                            text="Ready",
                            bg=self.COLORS["status_bg"],
                            fg=self.COLORS["status_fg"],
                            font=("MS Sans Serif", 7, "bold"),
                            width=6,
                            anchor=CENTER)
        ready_label.pack(padx=3, pady=1)

        tx_cell = Frame(status_content,
                        bg=self.COLORS["status_bg"],
                        relief=RAISED,
                        borderwidth=1)
        tx_cell.pack(side=LEFT, padx=(0, 3), pady=1)

        tx_label = Label(tx_cell,
                         text="TX: 48",
                         bg=self.COLORS["status_bg"],
                         fg=self.COLORS["status_fg"],
                         font=("MS Sans Serif", 7, "bold"),
                         width=6,
                         anchor=CENTER)
        tx_label.pack(padx=3, pady=1)

        rx_cell = Frame(status_content,
                        bg=self.COLORS["status_bg"],
                        relief=RAISED,
                        borderwidth=1)
        rx_cell.pack(side=LEFT, padx=(0, 3), pady=1)

        rx_label = Label(rx_cell,
                         text="RX: 10827",
                         bg=self.COLORS["status_bg"],
                         fg=self.COLORS["status_fg"],
                         font=("MS Sans Serif", 7, "bold"),
                         width=8,
                         anchor=CENTER)
        rx_label.pack(padx=3, pady=1)

        spacer = Frame(status_content,
                       bg=self.COLORS["status_bg"])
        spacer.pack(side=LEFT, fill=X, expand=True)

    def clear_terminal(self, text_widget):
        """Очистка терминала"""
        text_widget.configure(state='normal')
        text_widget.delete(1.0, END)
        text_widget.insert(END, "Terminal cleared.\n")
        text_widget.configure(state='disabled')

    def start_window_monitor(self):
        """Мониторинг окон"""

        def monitor():
            while self.running:
                time.sleep(0.1)

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

    def close_child_window(self, window):
        """Закрытие дочернего окна"""
        if window in self.child_windows:
            self.child_windows.remove(window)
            window.destroy()

    def on_close(self):
        """Закрытие приложения"""
        self.running = False
        for window in self.child_windows[:]:
            window.destroy()
        self.root.destroy()

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


if __name__ == "__main__":
    app = WindowsXPApp()
    app.run()