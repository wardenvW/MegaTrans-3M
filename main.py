from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from models import E1, Ethernet, Nx64
from typing import Dict, Any, List
import datetime
import time

CHAR_DELAY = 50  # скорость появления строк
CONTINUES_DELAY = 1000 # скорость появления повторяющихся сообщений

# -----------------------
# Простая модель Megatrans
# -----------------------
class Megatrans:
    def __init__(self) -> None:
        self.model = "MGS-3M-SRL-E1B/Eth"
        self.model_desc = "MEGATRANS-3M Subrack E1/RS232/Ethernet 120 Chm"
        self.hw = "E0"
        self.sw = "3.0.V5.L.15.6 /R3.1.1"
        self.date = datetime.date.today()
        self.boot_timestamp = time.time()

        self.time_set_timestamp = time.time()
        self.base_time = datetime.datetime.now()

        self.alarm: str = "NO"   # YES/NO
        self.statuc_link: str = "UP" # UP/DOWN
    
    def get_runs(self) -> str:
        time_delta = time.time() - self.boot_timestamp
        days = int(time_delta // 86400)
        hours = int(time_delta // 3600)
        minutes = int((time_delta % 3600) // 60)
        seconds = int(time_delta % 60)

        return f" {days:05d}d {hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_time(self) -> str:
        delta = time.time() - self.time_set_timestamp
        current = self.base_time + datetime.timedelta(seconds=delta)
        return current.strftime("%H:%M:%S")

# -----------------------
# COM устройство
# -----------------------
class COM:
    def __init__(self, role: str = "SLAVE") -> None:
        self.role = role
        self.e1 = E1()
        self.nx64 = Nx64()
        self.ethernet = Ethernet()
        self.megatrans = Megatrans()
        self.menu: str = "MM"
        self.message_prefix:str = f"{'CP' if self.role == 'SLAVE' else 'CO'}_01_1_{self.menu}>Select [1..6]: "
        self.time: str = ""
        self.date: str = ""
        self.MENU_COMMANDS = {
            "MM": {
                "1": self.activate_PM,
                "2": self.activate_FMM,
                "3": self.activate_CM,
                "4": self.activate_SM,
                "6": self.exit_program
            },
            "PM": {
                "G826": self.g826,
                "RESETG826": self.reset_g826,
                "HIST": "ДОДЕЛАТЬ",
                "RESETHIST": "ДОДЕЛАТЬ",
                "DATE": "",#self.date_perf,   # c 1970 по 2106
                "TIME": self.time_perf,
                "NETSTAT": "", #self.get_nestat,
                "RESETNETSTAT": "", #self.reset_netstat,
                "CONNECT": "", #self.connect,
                "DISCONNECT": "", #self.disconnect,
                "H": "",#, self.get_help,
                "M": self.back_to_main,
            },
            "FMM": {
                "SQ": "",
                "STARTUP": "",
                "STATUS": "", #self.get_status,
                "ALARM": "",  ## ALARM T тоже самое что __CONTINUE__
                "TLM": "",
                "RESETTLM": "",
                "TLMCONF": "",
                "TLMSET": "",
                "LOOP1": "", # LOOP1 [E/N] [ON/OFF]
                "LOOP2": "",
                "STARTAL": "",
                "RESTART": "",
                "BERT": "",
                "UPDATE": "",
                "CONNECT": "", #self.connect,
                "DISCONNECt": "", #self.disconnect,
                "H": "", #self.get_help,
                "M": self.back_to_main,
            },
            "CM": {
                "CONFIG": "",#self.get_config,
                "HW": "",#self.get_hw,
                "G704": "",#self.g704,
                "CRC4": "",#self.crc4,
                "EBIT": "", #self.ebit,
                "AISGEN": "", #self.asigen,
                "AISDET": "", #self.aisdet,
                "EXTCLK": "",#self.extclk,
                "PCM": "", #self.pcm, # PCM [30/31] [C/T]
                "IDLECAS": "",
                "IDLEPAT": "",
                "SIGSLOTS": "", # [AUTO/a,e]
                "SMSHOW": "",
                "SERVICE": "",
                "TYPE": "",
                "BITRATE": "",
                "CLOCKMODE": "", # [EXT/INT]
                "CLOCKDIR": "",
                "AUTOLOOP": "",
                "SLOTUSAGE": "",
                "MASTER": "",
                "PLL": "",
                "POWER": "",
                "RS232SLOT": "",
                "RS232BITS": "",
                "RS232RATE": "",
                "RS232ERATE": "",
                "AUTORST": "",
                "BASERATE": "",
                "ADAPT": "",
                "SETADDR": "",
                "SCALE": "",
                "DEFAULT": "",
                "ID": "",
                "ETHSD": "", # [10/100/AUTO] [H/F]
                "ETHPAYLOAD": "",
                "CONNECT": "", #self.connect,
                "DISCONNECT": "", #self.disconnect,
                "H": "", #self.get_help,
                "M": self.back_to_main
            },
            "SM": {
                "M": self.back_to_main
            }
        }
    
    def date_perf(self, *args) -> str:
        pass

    def time_perf(self, *args) -> str:
        if not args:
            return f"Current time: {self.megatrans.get_time()}"

        try:
            h, m, s = map(int, args[0].split(":"))

            self.megatrans.base_time = datetime.datetime.now().replace(
                hour=h, minute=m, second=s
            )
            self.megatrans.time_set_timestamp = time.time()

            return None
        except Exception:
            return "Illegal parameter(s)!"

    def g826(self, *args) -> str:
        if not args:
            msg = (
            "----------------------------------------------------------------------\n"
            f"G.826 Error Perfomance   :    "
            "CRC6\n"
            "----------------------------------------------------------------------\n"
            "Errored blocks           :  "
            "0000000000\n"
            "Severely errored seconds :  "
            "0000000000\n"
            "Background block errors  :  "
            "0000000000\n"
            "Available time           :  "
            "0000000000\n"
            "Unavailable time         :  "
            "0000000000\n"
            "----------------------------------------------------------------------")
            return msg
        elif args == ("E1",):
            if self.e1.crc4 == True and self.e1.ebit == True:
                Err_perf_message = f"CRC4      E-Bit"
            elif self.e1.crc4 == True and self.e1.ebit == False:
                Err_perf_message = f"CRC4"
            else:
                Err_perf_message = "FAS"

            msg = (
            "----------------------------------------------------------------------\n"
            f"G.826 Error Perfomance   :    "
            f"{Err_perf_message} \n"
            "----------------------------------------------------------------------\n"
            "Errored blocks           :  "
            f"{"0000000000" if Err_perf_message == "FAS" else "0000000000  0000000000"} \n"
            "Severely errored seconds :  "
            "0000000000\n"
            "Background block errors  :  "
            "0000000000\n"
            "Available time           :  "
            "0000000000\n"
            "Unavailable time         :  "
            "0000000000\n"
            "----------------------------------------------------------------------")
            return msg
        elif args == ("C",):
            msg = (
            "__CONTINUE__"
            "----------------------------------------------------------------------\n"
            f"G.826 Error Perfomance   :    "
            "CRC6\n"
            "----------------------------------------------------------------------\n"
            "Errored blocks           :  "
            "0000000000\n"
            "Severely errored seconds :  "
            "0000000000\n"
            "Background block errors  :  "
            "0000000000\n"
            "Available time           :  "
            "0000000000\n"
            "Unavailable time         :  "
            "0000000000\n"
            "----------------------------------------------------------------------\n"
            f"{self.message_prefix}")
            return msg
        elif args == ("E1", "C"):
            if self.e1.crc4 == True:
                Err_perf_message = f"CRC4      E-Bit"
            else:
                Err_perf_message = "FAS"
            msg = (
            "__CONTINUE__"
            "----------------------------------------------------------------------\n"
            f"G.826 Error Perfomance   :    "
            f"{Err_perf_message} \n"
            "----------------------------------------------------------------------\n"
            "Errored blocks           :  "
            f"{"0000000000" if Err_perf_message == "FAS" else "0000000000  0000000000"} \n"
            "Severely errored seconds :  "
            "0000000000\n"
            "Background block errors  :  "
            "0000000000\n"
            "Available time           :  "
            "0000000000\n"
            "Unavailable time         :  "
            "0000000000\n"
            "----------------------------------------------------------------------\n"
            f"{self.message_prefix}")
            return msg
        else:
            return "Illegal parameter(s)!\n!"
    def reset_g826(self):
        pass

    def activate_PM(self) -> str:
        self.menu = "PM"
        self.update_message_prefix()
        return "Perfomance management activated\nEnter <M> to return to MAIN, or <H> for HELP information"

    def activate_FMM(self) -> str:
        self.menu = "FMM"
        self.update_message_prefix()
        return "Fault and maintenance management activated\nEnter <M> to return to MAIN, or <H> for HELP information"

    def activate_CM(self) -> str:
        self.menu = "CM"
        self.update_message_prefix()
        return "Configuration management activated\nEnter <M> to return to MAIN, or <H> for HELP information"

    def activate_SM(self) -> str:
        self.menu = "SM"
        self.update_message_prefix()
        return "Security management activated\nEnter <M> to return to MAIN, or <H> for HELP information"

    def exit_program(self) -> str:
        self.update_message_prefix()
        return "Exiting..."

    #back to MM
    def back_to_main(self) -> str:
        self.menu = "MM"
        self.update_message_prefix()
        return self.get_main_menu_text()

    def execute(self, cmd: str) -> str:
        if not cmd:
            return ""
        parts = cmd.strip().upper().split()
        cmd = parts[0]
        args = parts[1:]

        command_list = self.MENU_COMMANDS.get(self.menu, {})   
        if cmd in command_list:
            return command_list[cmd](*args)
        return "Invalid command"

    def get_main_menu_text(self) -> str:
        return (
            f"MODEL {self.megatrans.model}\n"
            f"HW {self.megatrans.hw}\n"
            f"SW {self.megatrans.sw}\n"
            f"DATE {self.megatrans.date.strftime("%b %d %Y")}\n"
            f"ID\n"
            f"RUNS{self.megatrans.get_runs()}\n"
            f"ALARM {self.megatrans.alarm}\n"
            f"STATUS LINK {self.megatrans.statuc_link}\n"
            f"MODEL_DESC {self.megatrans.model_desc}\n\n"
            "Copyright (C) 2006 by Nateks Ltd.\n\n"
            "------------- Main Menu -----------------\n"
            "1.  Perfomance management  (PM)\n"
            "2.  Fault and maintenance management (FMM)\n"
            "3.  Configuration management  (CM)\n"
            "4.  Security management  (SM)\n"
            "\n6.  Exit\n"
            "----------------------------------------\n\n"
        )
    
    def update_message_prefix(self) -> None:
        role = "CP" if self.role == "SLAVE" else "CO"

        if self.menu == "MM":
            self.message_prefix = f"{role}_01_1_{self.menu}>Select [1..6] : "
        else:
            self.message_prefix = f"{role}_01_1_{self.menu}:"
    


# -------------------------------
# Терминал
# -------------------------------
class Terminal(tk.Toplevel):
    def __init__(self, master, com: COM, settings):
        super().__init__(master)
        self.com = com
        self.settings: Dict["str": Any] = settings
        self.input_start: str = "1.0"
        self.locked: bool = True
        self.sequence_index = 0
        self.sequence: List["str"] = ["%", "0", "1"]
        self.output_in_progress: bool = False

        self.port_name = self.settings.get("port")
        self.baud_rate = self.settings.get("baud_rate")
        self.data_bits = self.settings.get("data_bits")
        self.parity = self.settings.get("parity")
        self.stop_bits = self.settings.get("stop_bits")


        self.title(("{},{},{},{},{}").format(
            self.port_name,
            self.baud_rate,
            self.data_bits,
            self.parity,
            self.stop_bits
        ))

        self.geometry("600x400")
        self.attributes("-topmost", True)

        self.text = tk.Text(self, bg="black", fg="lime", insertbackground="lime")
        self.text.pack(fill="both", expand=True)

        self.text.bind("<Key>", self.on_key)
        self.text.bind("<BackSpace>", self.backspace)
        self.text.bind("<Return>", self.enter)

        for key in ["<Up>", "<Down>", "<Left>", "<Right>", "<Home>", "<End>", "<Prior>", "<Next>"]:
            self.text.bind(key, lambda e: "break")
        self.text.bind("<Button-1>", lambda e: self.text.mark_set("insert", "end"))
        self.text.bind("<Button-2>", lambda e: "break")
        self.text.bind("<Button-3>", lambda e: "break")

        self.text.mark_set("insert", "end")
        self.text.see("end")
        self.blink_cursor()



    def type_lines(self, text, index=0, done_callback=None):
        if index == 0:
            self.output_in_progress = True
            self._lines = text.splitlines(keepends=True)

        if index < len(self._lines):
            self.text.insert("end", self._lines[index])
            self.text.see("end")
            self.after(
                CHAR_DELAY,
                lambda: self.type_lines(text, index + 1, done_callback)
            )
        else:
            self.output_in_progress = False
            if done_callback:
                done_callback()

    def blink_cursor(self):
        self.text.mark_set("insert", "end")
        self.after(500, self.blink_cursor)

    def put_message_prefix(self):
        self.text.insert("end", f"{self.com.message_prefix}")
        self.text.see("end")
        self.input_start = self.text.index("end-1c")
        self.text.mark_set("insert", "end-1c")

    def get_input(self):
        return self.text.get(self.input_start, "end-1c")

    def on_key(self, event):
        if self.output_in_progress:
            return "break"

        self.text.mark_set("insert", "end")
        self.text.see("end")

        if self.locked:
            char = event.char.upper()
            if not char or char.isspace():
                return "break"

            if char == self.sequence[self.sequence_index]:
                self.sequence_index += 1
                if self.sequence_index == len(self.sequence):
                    self.locked = False
                    self.type_lines(self.com.get_main_menu_text(), done_callback=self.put_message_prefix)
                return "break"
            else:
                self.sequence_index = 0
                return "break"

        char = event.char.upper()
        if char and char.isprintable():
            self.text.insert("end", char)
            self.text.see("end")
            return "break"

        return "break"

    def backspace(self, event):
        if self.locked:
            return "break"
        cur_index = self.text.index("insert")
        if self.text.compare(cur_index, ">", self.input_start):
            self.text.delete("%s-1c" % cur_index)
        return "break"
    
    def wait_for_key_to_continue(self):
        def unlock(event):
            self.continue_mode = False 
            self.text.unbind("<Key>", bind_id)
            self.locked = False
            self.put_message_prefix()

        self.locked = True
        bind_id = self.text.bind("<Key>", unlock)

    def repeat_output(self):
        if not self.continue_mode:
            return
        self.type_lines("\n" + self.continue_text + "\n")
        self.after(CONTINUES_DELAY, self.repeat_output)

    def enter(self, event):
        if self.locked or self.output_in_progress:
            return "break"

        cmd = self.get_input().strip()
        resp = self.com.execute(cmd)

        if resp is None:
            self.text.insert("end", "\n")
            self.put_message_prefix()
            return "break"

        if resp.startswith("__CONTINUE__"):
            self.continue_text = resp.replace("__CONTINUE__", "").strip()
            self.continue_mode = True


            self.repeat_output()


            self.wait_for_key_to_continue()
            return "break"

        # --- обычный вывод ---
        self.type_lines("\n" + resp + "\n", done_callback=self.put_message_prefix)
        return "break"


# -------------------------------
# Windows XP GUI main app
# -------------------------------
class WindowsXPApp:
    def __init__(self):
        self.COLORS = {
            "window_bg": "#a0a0a0",
            "menu_bg": "#ffffff",
            "dialog_bg": "#ece9d8",
            "button_bg": "#d4d0c8",
            "button_fg": "#000000",
            "border_dark": "#808080",
            "tab_bg": "#d4d0c8",
            "tab_active_bg": "#ece9d8",
            "label_fg": "#000000",
            "check_bg": "#ece9d8",
            "radio_bg": "#ece9d8",
            "listbox_bg": "#ffffff",
            "listbox_fg": "#000000",
        }

        self.FONTS = {
            "title": ("MS Sans Serif", 8, "bold"),
            "label": ("MS Sans Serif", 8),
            "button": ("MS Sans Serif", 8),
            "tab": ("MS Sans Serif", 8),
        }

        self.root = Tk()
        self.root.title("Windows XP Application")
        self.root.geometry("1024x768")
        self.root.configure(bg=self.COLORS["window_bg"])

        self.com_ports = {}
        self.terminals = {}
        self.child_windows = []

        self.create_classic_menu()
        self.create_toolbar()
        self.create_main_workspace()

    def create_classic_menu(self):
        menubar = Menu(self.root, bg=self.COLORS["menu_bg"], fg="black")
        self.root.config(menu=menubar)
        profile_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        profile_menu.add_command(label="New Profile")
        profile_menu.add_command(label="Open Profile...")
        profile_menu.add_command(label="Save Profile")
        profile_menu.add_separator()
        profile_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Profile", menu=profile_menu)

        edit_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        port_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        port_menu.add_command(label="Open", command=self.show_property_dialog)
        menubar.add_cascade(label="Port Manager", menu=port_menu)

    def create_toolbar(self):
        toolbar = Frame(self.root, bg=self.COLORS["window_bg"], height=32)
        toolbar.pack(fill=X, side=TOP, padx=0, pady=0)
        buttons_frame = Frame(toolbar, bg=self.COLORS["window_bg"], height=30)
        buttons_frame.pack(fill=X, side=TOP, padx=2, pady=2)

        Button(buttons_frame, text="Settings", bg=self.COLORS["button_bg"], fg=self.COLORS["button_fg"],
               font=self.FONTS["button"], relief=RAISED, command=self.show_property_dialog).pack(side=LEFT, padx=2)
        Button(buttons_frame, text="Save", bg=self.COLORS["button_bg"], fg=self.COLORS["button_fg"],
               font=self.FONTS["button"], relief=RAISED).pack(side=LEFT, padx=2)
        Button(buttons_frame, text="Exit", bg=self.COLORS["button_bg"], fg=self.COLORS["button_fg"],
               font=self.FONTS["button"], relief=RAISED, command=self.root.destroy).pack(side=LEFT, padx=2)

    def create_main_workspace(self):
        workspace = Frame(self.root, bg=self.COLORS["window_bg"])
        workspace.pack(fill=BOTH, expand=True, padx=8, pady=8)

    def show_property_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Open COM Port")
        dialog.geometry("600x400")
        dialog.configure(bg=self.COLORS["dialog_bg"])
        self.child_windows.append(dialog)

        outer_frame = Frame(dialog, bg=self.COLORS["border_dark"], borderwidth=1, relief=SOLID)
        outer_frame.pack(fill=BOTH, expand=True, padx=1, pady=1)
        main_frame = Frame(outer_frame, bg=self.COLORS["dialog_bg"])
        main_frame.pack(fill=BOTH, expand=True, padx=1, pady=1)

        # ------------------------
        # Левый блок - COM порты
        left_frame = Frame(main_frame, bg=self.COLORS["dialog_bg"])
        left_frame.pack(side=LEFT, fill=Y, padx=(10, 20), pady=10)

        Label(left_frame, text="Port:", bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(anchor=W, pady=5)
        self.port_listbox = Listbox(left_frame, bg=self.COLORS["listbox_bg"],
                                    fg=self.COLORS["listbox_fg"], height=6, selectbackground="#000080",
                                    selectforeground="#ffffff")
        self.port_listbox.pack(fill=BOTH, expand=True)

        for port_name in ["COM1", "COM2"]:
            display_name = port_name + (" *" if port_name in self.terminals else "")
            self.port_listbox.insert(END, display_name)
        self.port_listbox.selection_set(0)

        # ------------------------
        # Правый блок - параметры COM
        # ------------------------
        right_frame = Frame(main_frame, bg=self.COLORS["dialog_bg"])
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Baud rate
        baud_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        baud_frame.pack(fill=X, pady=(0,5))
        Label(baud_frame, text="Baud Rate:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        self.baud_var = StringVar(value="9600")
        ttk.Combobox(baud_frame, textvariable=self.baud_var,
                     values=["9600","19200","38400","57600","115200"],
                     state="readonly", width=15).pack(side=LEFT)
        self.user_defined_var = BooleanVar(value=False)
        Checkbutton(baud_frame, text="User defined", variable=self.user_defined_var,
                    bg=self.COLORS["check_bg"], fg=self.COLORS["label_fg"],
                    font=self.FONTS["label"]).pack(side=LEFT)

        # Data bits
        data_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        data_frame.pack(fill=X, pady=(0,5))
        Label(data_frame, text="Data bits:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        self.data_var = StringVar(value="8")
        ttk.Combobox(data_frame, textvariable=self.data_var, values=["5","6","7","8"],
                     state="readonly", width=15).pack(side=LEFT)

        # Parity
        parity_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        parity_frame.pack(fill=X, pady=(0,5))
        Label(parity_frame, text="Parity:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        self.parity_var = StringVar(value="None")
        ttk.Combobox(parity_frame, textvariable=self.parity_var,
                     values=["None","Even","Odd","Mark","Space"],
                     state="readonly", width=15).pack(side=LEFT)

        # Stop bits
        stop_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        stop_frame.pack(fill=X, pady=(0,5))
        Label(stop_frame, text="Stop bits:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        self.stop_var = StringVar(value="1")
        ttk.Combobox(stop_frame, textvariable=self.stop_var, values=["1","1.5","2"],
                     state="readonly", width=15).pack(side=LEFT)

        # Flow control
        flow_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        flow_frame.pack(fill=X, pady=(0,5))
        Label(flow_frame, text="Flow control:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        flow_control_frame = Frame(flow_frame, bg=self.COLORS["dialog_bg"])
        flow_control_frame.pack(side=LEFT)
        self.flow_var = StringVar(value="RTS/CTS")
        for val in ["RTS/CTS","DTR/DSR","XON/XOFF"]:
            Radiobutton(flow_control_frame, text=val, variable=self.flow_var, value=val,
                        bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(anchor=W)

        # RTS/DTR
        state_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        state_frame.pack(fill=X, pady=(5,0))

        # RTS
        rts_frame = Frame(state_frame, bg=self.COLORS["dialog_bg"])
        rts_frame.pack(fill=X, pady=(0,5))
        Label(rts_frame, text="RTS state:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        rts_state_frame = Frame(rts_frame, bg=self.COLORS["dialog_bg"])
        rts_state_frame.pack(side=LEFT)
        self.rts_var = StringVar(value="ON")
        Radiobutton(rts_state_frame, text="ON", variable=self.rts_var, value="ON",
                    bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(side=LEFT, padx=(0,10))
        Radiobutton(rts_state_frame, text="OFF", variable=self.rts_var, value="OFF",
                    bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(side=LEFT)

        # DTR
        dtr_frame = Frame(state_frame, bg=self.COLORS["dialog_bg"])
        dtr_frame.pack(fill=X)
        Label(dtr_frame, text="DTR state:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        dtr_state_frame = Frame(dtr_frame, bg=self.COLORS["dialog_bg"])
        dtr_state_frame.pack(side=LEFT)
        self.dtr_var = StringVar(value="ON")
        Radiobutton(dtr_state_frame, text="ON", variable=self.dtr_var, value="ON",
                    bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(side=LEFT, padx=(0,10))
        Radiobutton(dtr_state_frame, text="OFF", variable=self.dtr_var, value="OFF",
                    bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(side=LEFT)

        # ------------------------
        # Кнопки диалога
        # ------------------------
        button_frame = Frame(main_frame, bg=self.COLORS["dialog_bg"])
        button_frame.pack(fill=X, pady=10)
        Frame(button_frame, bg=self.COLORS["dialog_bg"]).pack(side=LEFT, expand=True)

        self.ok_button = Button(button_frame, text="OK", width=10,
                                command=lambda: self.open_terminal(dialog))
        self.ok_button.pack(side=LEFT, padx=5)
        Button(button_frame, text="Cancel", width=10, command=dialog.destroy).pack(side=LEFT, padx=5)

        # ------------------------
        # Логика блокировки кнопки OK
        # ------------------------
        def update_ok_button(event=None):
            sel = self.port_listbox.curselection()
            if not sel:
                self.ok_button.config(state=DISABLED)
                return
            display_name = self.port_listbox.get(sel[0])
            if "*" in display_name:
                self.ok_button.config(state=DISABLED)
            else:
                self.ok_button.config(state=NORMAL)

        self.port_listbox.bind("<<ListboxSelect>>", update_ok_button)
        update_ok_button()

    def open_terminal(self, dialog):
        selection = self.port_listbox.curselection()
        if not selection:
            return
        port = self.port_listbox.get(selection[0]).replace(" *","")

        if port not in self.com_ports:
            self.com_ports[port] = COM(role="SLAVE")

        com_obj = self.com_ports[port]

        settings = {
        "port": port,
        "baud_rate": self.baud_var.get(),
        "data_bits": self.data_var.get(),
        "parity": self.parity_var.get(),
        "stop_bits": self.stop_var.get()
    }

        term = Terminal(self.root, com=com_obj, settings=settings,)
        self.terminals[port] = term

        def on_close():
            try:
                del self.terminals[port]
            except Exception:
                pass
            term.destroy()

        term.protocol("WM_DELETE_WINDOW", on_close)
        dialog.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WindowsXPApp()
    app.run()
