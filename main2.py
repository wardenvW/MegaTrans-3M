import tkinter as tk

# -------------------------------
# Устройства Megatrans
# -------------------------------
class Megatrans:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.e1 = True
        self.eth = True
        self.nx64 = True

    def execute(self, cmd: str) -> str:
        cmd = cmd.strip().upper()
        if cmd == "SHOW":
            return f"{self.name} ({self.role})\nE1={self.e1}\nETH={self.eth}\nNX64={self.nx64}"
        if cmd == "E1 ON":
            self.e1 = True
            return "E1 turned ON"
        if cmd == "E1 OFF":
            self.e1 = False
            return "E1 turned OFF"
        return f"Unknown command: {cmd}"

# -------------------------------
# COM-сессия
# -------------------------------
class ComPortSession:
    def __init__(self, name, device):
        self.name = name
        self.device = device
        self.connected = False
        self.remote = None
        self.locked = False
        self.ui = None

# -------------------------------
# Менеджер COM-портов
# -------------------------------
class ComPortManager:
    def __init__(self):
        self.com1 = ComPortSession("COM1", Megatrans("M1", "MASTER"))
        self.com2 = ComPortSession("COM2", Megatrans("M2", "SLAVE"))

    def register_ui(self, com, ui_window):
        com.ui = ui_window

    def send_command(self, com: ComPortSession, cmd: str) -> str:
        cmd_upper = cmd.strip().upper()
        if com.locked:
            return "*** TERMINAL LOCKED BY REMOTE CONTROL ***"

        if cmd_upper == "CONNECT R":
            return self.connect_r(com)
        if cmd_upper == "DISCONNECT":
            return self.disconnect(com)

        target = com.remote if com.connected else com.device
        return target.execute(cmd)

    def connect_r(self, src: ComPortSession) -> str:
        target = self.com2 if src is self.com1 else self.com1
        src.connected = True
        src.remote = target.device
        target.locked = True
        if target.ui:
            target.ui.lock()
        return f"CONNECTED TO {target.name} ({target.device.name})"

    def disconnect(self, src: ComPortSession) -> str:
        if not src.connected:
            return "NO ACTIVE CONNECTION"
        target = self.com2 if src is self.com1 else self.com1
        src.connected = False
        src.remote = None
        target.locked = False
        if target.ui:
            target.ui.unlock()
        return "DISCONNECTED. LOCAL CONTROL RESTORED"

# -------------------------------
# GUI терминал
# -------------------------------
class Terminal(tk.Toplevel):
    def __init__(self, master, manager: ComPortManager, com: ComPortSession, prompt="CP_01_1_MM>"):
        super().__init__(master)
        self.title(com.name)
        self.geometry("800x500")
        self.manager = manager
        self.com = com
        self.prompt = prompt
        self.input_start = "1.0"

        self.text = tk.Text(self, bg="black", fg="white", insertbackground="white")
        self.text.pack(fill="both", expand=True)

        self.text.bind("<Key>", self.on_key)
        self.text.bind("<BackSpace>", self.backspace)
        self.text.bind("<Return>", self.enter)

        self.manager.register_ui(com, self)
        self.put_prompt()

    def put_prompt(self):
        self.text.insert("end", f"\n{self.prompt}")
        self.text.see("end")
        self.input_start = self.text.index("end-1c")

    def get_input(self):
        return self.text.get(self.input_start, "end-1c")


    def on_key(self, event):
        cursor = self.text.index("insert")
        if getattr(self, 'locked', False):
            # игнорируем все нажатия клавиш
            return "break"
        if self.text.compare(cursor, "<", self.input_start):
            return "break"
        return None

    def backspace(self, event):
        if getattr(self, 'locked', False):
            return "break"
        cursor = self.text.index("insert")
        if self.text.compare(cursor, "<=", self.input_start):
            return "break"
        return None

    def enter(self, event):
        cmd = self.get_input().strip()
        self.text.insert("end", "\n")
        if cmd == "":
            self.text.insert("end", "(empty command)\n")
        else:
            resp = self.manager.send_command(self.com, cmd)
            self.text.insert("end", f"{resp}\n")
        self.put_prompt()
        return "break"

    def lock(self):
    # Оставляем Text в normal, чтобы курсор мигал
        self.locked = True
        self.text.mark_set("insert", "end-1c")
        self.text.see("insert")

    def unlock(self):
        self.locked = False
        self.put_prompt()
        self.text.see("end")

# -------------------------------
# Главное окно с кнопками COM1 и COM2
# -------------------------------
def main():
    root = tk.Tk()
    root.title("Megatrans Manager")
    root.geometry("400x150")

    manager = ComPortManager()

    tk.Label(root, text="Open COM Terminal:").pack(pady=10)

    tk.Button(root, text="COM1", width=20,
              command=lambda: Terminal(root, manager, manager.com1)).pack(pady=5)
    tk.Button(root, text="COM2", width=20,
              command=lambda: Terminal(root, manager, manager.com2)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()