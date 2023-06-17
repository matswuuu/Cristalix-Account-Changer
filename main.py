import codecs
import threading
import subprocess
import os
import time
import json
from tkinter import filedialog

import customtkinter

state = customtkinter.DISABLED


def get_dir():
    for rootdir, dirs, files in os.walk("C:/"):
        for file in files:
            if ((file.split('.')[-1]) == 'launcher'):
                if rootdir.find("cristalix") != -1:
                    global cristalix_dir
                    cristalix_dir = rootdir

                    global launcher_dir
                    launcher_dir = cristalix_dir + "/.launcher"


threading.Thread(target=get_dir).start()


class Scrollable_Frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.configure(width=560, height=340)
        self.nick_entrys = []
        self.token_entrys = []
        self.start_buttons = []
        self.delete_buttons = []
        self.row = 0

    def add(self, nick="", token=""):
        self.row = self.row + 1

        nick_entry = customtkinter.CTkEntry(
            self, placeholder_text="Ник", width=180, height=25)
        nick_entry.grid(row=self.row, column=0, pady=(10, 0), padx=(10, 10))
        nick_entry.insert(0, nick)
        self.nick_entrys.append(nick_entry)

        token_entry = customtkinter.CTkEntry(
            self, placeholder_text="Токен", width=230, height=25)
        token_entry.grid(row=self.row, column=1, pady=(10, 0), padx=(10, 10))
        token_entry.insert(0, token)
        self.token_entrys.append(token_entry)

        start_button = customtkinter.CTkButton(
            self, text="Запустить", width=100, height=25, state=state,
            command=lambda: self.start(start_button))
        start_button.grid(row=self.row, column=2, pady=(10, 0), padx=(10, 10))
        self.start_buttons.append(start_button)

        delete_button = customtkinter.CTkButton(
            self, text="-", width=20, height=25, command=lambda: self.delete(delete_button))
        delete_button.grid(row=self.row, column=3, pady=(10, 0), padx=(10, 5))
        self.delete_buttons.append(delete_button)

    def delete(self, button):
        id = self.delete_buttons.index(button)

        self.nick_entrys[id].grid_forget()
        self.token_entrys[id].grid_forget()
        self.start_buttons[id].grid_forget()
        self.delete_buttons[id].grid_forget()

        self.nick_entrys.pop(id)
        self.token_entrys.pop(id)
        self.start_buttons.pop(id)
        self.delete_buttons.pop(id)

    def login(self, nick, token):
        with codecs.open(launcher_dir, "r", encoding="utf-8") as f:
            launcher_dict = json.load(f)

            launcher_dict["accounts"] = {}
            launcher_dict["accounts"][nick] = token
            launcher_dict["currentAccount"] = nick

            with codecs.open(launcher_dir, "w", encoding="utf-8") as f:
                json.dump(launcher_dict, f)

        if filename.endswith("jar"):
            threading.Thread(target=lambda: subprocess.call(
                ["java", "-jar", filename])).start()
        else:
            threading.Thread(
                target=lambda: os.startfile(filename)).start()

    def start(self, button):
        id = self.start_buttons.index(button)
        nick = self.nick_entrys[id].get()
        token = self.token_entrys[id].get()

        self.login(nick, token)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("ACCOUNT CHANGER")
        self.geometry("600x400")
        self.iconbitmap("images/logo.ico")

        self.frame = Scrollable_Frame(self)
        self.frame.place(x=10, y=70)

        self.browse_files_button = customtkinter.CTkButton(
            self, text="Выбрать", width=60, height=20, command=self.browse_files)
        self.browse_files_button.place(x=10, y=40)

        self.start_all_button = customtkinter.CTkButton(
            self, text="Запустить все", width=100, height=20, state=customtkinter.DISABLED,
            command=lambda: threading.Thread(target=self.start_all).start())
        self.start_all_button.place(x=10, y=10)

        self.get_token_button = customtkinter.CTkButton(
            self, text="Токен", width=40, height=20, command=self.get_token)
        self.get_token_button.place(x=120, y=10)

        self.add_button = customtkinter.CTkButton(
            self, text="+", width=20, height=20, command=self.frame.add)
        self.add_button.place(x=570, y=10)

        self.switch = customtkinter.CTkSwitch(
            self, text="Тема", command=self.set_theme)
        self.switch.place(x=520, y=40)

        with codecs.open("config.json", "r", encoding="utf-8") as f:
            config_dict = json.load(f)

        global filename
        filename = config_dict["fileName"]
        if filename != "":
            self.enable()

        self.browse_label = customtkinter.CTkLabel(
            self, text=f"Лаунчер: {filename}", width=160, height=20)
        self.browse_label.place(x=90, y=40)

        if config_dict["theme"]:
            self.switch.select()
        self.set_theme()

        accounts_amount = len(config_dict["accounts"])
        accounts = config_dict["accounts"]
        for i in range(accounts_amount):
            a = accounts[str(i)]
            nick = a["nick"]
            token = a["token"]

            self.frame.add(nick, token)

    def set_theme(self):
        if bool(self.switch.get()):
            customtkinter.set_appearance_mode("light")
        else:
            customtkinter.set_appearance_mode("dark")

    def get_token(self):
        with codecs.open(launcher_dir, encoding="utf-8") as f:
            lc = json.loads(f.read())
            account = lc["currentAccount"]
            token = lc["accounts"][account]

            self.frame.add(account, token)

    def enable(self):
        global state
        state = customtkinter.NORMAL

        self.start_all_button.configure(state=state)
        for button in self.frame.start_buttons:
            button.configure(state=state)

    def disable(self):
        global state
        state = customtkinter.DISABLED

        self.start_all_button.configure(state=state)
        for button in self.frame.start_buttons:
            button.configure(state=state)

    def browse_files(self):
        global filename
        filename = filedialog.askopenfilename(
            initialdir="/", title="Выберите лаунчер",
            filetypes=(("Java ланучер", "*.jar*"),
                       ("Exe лаунчер", "*.exe*")))

        self.browse_label.configure(text=f"Лаунчер: {filename}")

        if filename != "":
            self.enable()
        else:
            self.disable()

    def start_all(self):
        length = len(self.frame.nick_entrys)
        for i in range(length):
            nick = self.frame.nick_entrys[i].get()
            token = self.frame.token_entrys[i].get()

            self.frame.login(nick, token)
            time.sleep(10)

    def save(self):
        with codecs.open("config.json", "r", encoding="utf-8") as f:
            config_dict = json.load(f)

        accounts = {}
        length = len(self.frame.nick_entrys)
        for i in range(length):
            nick = self.frame.nick_entrys[i].get()
            token = self.frame.token_entrys[i].get()

            if not nick or not token:
                continue

            accounts[len(accounts)] = {
                "nick": nick,
                "token": token,
            }

            theme = bool(self.switch.get())

            config_dict["theme"] = theme
            config_dict["fileName"] = filename
            config_dict["accounts"] = accounts

            with codecs.open("config.json", "w", encoding="utf-8") as f:
                json.dump(config_dict, f)

        self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.save)
    app.mainloop()
