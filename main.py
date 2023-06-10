import codecs
import threading
import subprocess
import os
import time
import json
from tkinter import filedialog

import customtkinter
from configparser import ConfigParser


config = ConfigParser()
config.add_section("config")

with codecs.open("config.ini", "r", encoding="utf-8") as config_file:
    config.read_file(config_file)

filename = config["config"]["filename"]


def browse():
    global filename
    filename = filedialog.askopenfilename(
        initialdir="/", title="Выберите лаунчер",
        filetypes=(("Java ланучер", "*.jar*"),
                   ("Exe лаунчер", "*.exe*")))


def get_dir():
    for rootdir, dirs, files in os.walk("C:/"):
        for file in files:
            if ((file.split('.')[-1]) == 'launcher'):
                if rootdir.find("cristalix") != -1:
                    rootdir = rootdir.replace(
                        "/", "\\").replace("\\", "\\\\")

                    return rootdir


def login(nick, token):
    dir = get_dir()
    with codecs.open("default_config.txt", "r", encoding="utf-8") as launcher_config:
        lc = launcher_config.read()
        lc = lc.replace("NICK", nick).replace("TOKEN", token).replace(
            "UPDATESDIR", dir + "\\\\updates")

    with codecs.open(f"{dir}/.launcher", "w", encoding="utf-8") as launcher_file:
        launcher_file.write(lc)

    if filename.endswith("jar"):
        threading.Thread(target=lambda: subprocess.call(
            ["java", "-jar", filename])).start()
    else:
        threading.Thread(
            target=lambda: os.startfile(filename)).start()


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
        self.state = customtkinter.DISABLED

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
            self, text="Запустить", width=100, height=25, state=self.state,
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

    def start(self, button):
        id = self.start_buttons.index(button)
        nick = self.nick_entrys[id].get()
        token = self.token_entrys[id].get()

        login(nick, token)

    def enable_buttons(self):
        for button in self.start_buttons:
            button.configure(state=customtkinter.NORMAL)

        self.state = customtkinter.NORMAL

    def get_all_values(self):
        def get_values(entrys_list):
            l = []
            for i in range(len(entrys_list)):
                value = entrys_list[i].get()
                l.append(value)

            return l

        nicks = get_values(self.nick_entrys)
        tokens = get_values(self.token_entrys)

        return nicks, tokens


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("ACCOUNT CHANGER by matswuuu")
        self.geometry("600x400")
        self.iconbitmap("images\logo.ico")

        self.frame = Scrollable_Frame(self)
        self.frame.place(x=10, y=70)

        self.browse_label = customtkinter.CTkLabel(
            self, text=f"Лаунчер: {filename}", width=160, height=20)
        self.browse_label.place(x=90, y=40)

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

        for i in range(int(config["config"]["amount"])):
            nick = config["config"][f"{i}_nick"]
            token = config["config"][f"{i}_token"]
            self.frame.add(nick, token)

        if filename != "":
            self.enable()

    def get_token(self):
        dir = get_dir()
        with codecs.open(f"{dir}/.launcher", encoding="utf-8") as f:
            lc = json.loads(f.read())
            account = lc["currentAccount"]
            token = lc["accounts"][account]

            self.frame.add(account, token)

    def enable(self):
        self.start_all_button.configure(state=customtkinter.NORMAL)
        self.frame.enable_buttons()

    def browse_files(self):
        browse()

        self.browse_label.configure(text=f"Лаунчер: {filename}")

        if filename != "":
            self.enable()

    def start_all(self):
        nicks, tokens = self.frame.get_all_values()

        for i in range(len(nicks)):
            login(nicks[i], tokens[i])
            time.sleep(10)

    def save(self):
        nicks, tokens = self.frame.get_all_values()
        length = len(nicks)

        for i in range(length):
            config.set("config", "amount", str(length))
            config.set("config", "filename", filename)
            config.set("config", f"{i}_nick", nicks[i])
            config.set("config", f"{i}_token", tokens[i])

            with codecs.open("config.ini", "w", encoding="utf-8") as config_file:
                config.write(config_file)

        self.destroy()


app = App()
app.protocol("WM_DELETE_WINDOW", app.save)
app.mainloop()
