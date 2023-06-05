import codecs
import threading
import subprocess
import os
import time
import json
import platform
from tkinter import filedialog

import customtkinter
from configparser import ConfigParser


system = platform.system()
if system == "Linux":
    d = "/"
elif system == "Windows":
    d = "C:/"

config = ConfigParser()
config.add_section("config")

with codecs.open("config.ini", "r", encoding="utf-8") as config_file:
    config.read_file(config_file)

filename = config["config"]["filename"]
groups = []
state = customtkinter.DISABLED

def get_dir():
    for rootdir, dirs, files in os.walk(d):
        for file in files:
            if ((file.split('.')[-1]) == 'launcher'):
                if rootdir.find("cristalix") != -1:
                    global cristalix_dir
                    cristalix_dir = rootdir   
                    
                    global launcher_dir
                    launcher_dir = cristalix_dir + "/.launcher"

threading.Thread(target=get_dir).start()


def login(nick, token):
    with open(launcher_dir, "r") as f:
        launcher_dict = json.load(f)

        launcher_dict["accounts"] = {}
        launcher_dict["accounts"][nick] = token
        launcher_dict["currentAccount"] = nick
        launcher_dict["updatesDirectory"] = dir

        with open(launcher_dir, "w") as f:
            json_dump = json.dumps(launcher_dict)
            f.write(json_dump)

    if filename.endswith("jar"):
        threading.Thread(target=lambda: subprocess.call(
            ["java", "-jar", filename])).start()
    else:
        threading.Thread(
            target=lambda: os.startfile(filename)).start()


def start_all(self):
    nicks, tokens = self.frame.get_all_values()

    for i in range(len(nicks)):
        login(nicks[i], tokens[i])
        time.sleep(10)

def start(self, button):
    id = self.start_buttons.index(button)
    nick = self.nick_entrys[id].get()
    token = self.token_entrys[id].get()

    login(nick, token)


class Scrollable_Frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.configure(width=610, height=340)
        self.nick_entrys = []
        self.token_entrys = []
        self.start_buttons = []
        self.delete_buttons = []
        self.settings_buttons = []
        self.windows_settings = []
        self.row = 0

    def add_group(self, name="", default_add=False):
        group = Group_Frame(self, name)
        if default_add:
            group.add()
        group.grid(row=self.row, column=0, pady=(
            15, 15), padx=(10, 10), columnspan=4)
        groups.append(group)

        self.row = self.row + 1

    def add(self, nick="", token=""):
        nick_entry = customtkinter.CTkEntry(
            self, placeholder_text="Ник", width=180, height=25)
        nick_entry.grid(row=self.row, column=0, pady=(10, 0), padx=(10, 10))
        if nick != "":
            nick_entry.insert(0, nick)
        self.nick_entrys.append(nick_entry)

        token_entry = customtkinter.CTkEntry(
            self, placeholder_text="Токен", width=230, height=25)
        token_entry.grid(row=self.row, column=1, pady=(10, 0), padx=(10, 10))
        if token != "":
            token_entry.insert(0, token)
        self.token_entrys.append(token_entry)
        
        settings_button = customtkinter.CTkButton(
            self, text="Настройки", width=100, height=25, 
            command=lambda: self.open_settings(settings_button))
        settings_button.grid(row=self.row, column=2, pady=(10, 0), padx=(10, 10))
        self.settings_buttons.append(settings_button)
        
        self.settings_window = None
        self.windows_settings.append(self.settings_window)

        start_button = customtkinter.CTkButton(
            self, text="Запустить", width=100, height=25, state=state,
            command=lambda: start(self, start_button))
        start_button.grid(row=self.row, column=3, pady=(10, 0), padx=(10, 10))
        self.start_buttons.append(start_button)

        delete_button = customtkinter.CTkButton(
            self, text="-", width=20, height=25, command=lambda: self.delete(delete_button))
        delete_button.grid(row=self.row, column=4, pady=(10, 0), padx=(10, 5))
        self.delete_buttons.append(delete_button)

        self.row = self.row + 1

    def delete(self, button):
        id = self.delete_buttons.index(button)
        self.forget(id)

    def forget(self, id):
        self.nick_entrys[id].grid_forget()
        self.token_entrys[id].grid_forget()
        self.start_buttons[id].grid_forget()
        self.delete_buttons[id].grid_forget()
        self.settings_buttons[id].grid_forget()

        self.nick_entrys.pop(id)
        self.token_entrys.pop(id)
        self.start_buttons.pop(id)
        self.delete_buttons.pop(id)
        self.settings_buttons.pop(id)
        self.windows_settings.pop(id)
        
    def open_settings(self, button):
        id = self.settings_buttons.index(button)
        self.windows_settings.pop(id)
        
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = Settings_Window(self)
        else:
            self.settings_window.focus()
            
        self.windows_settings.append(self.settings_window)

class Group_Frame(Scrollable_Frame):
    def __init__(self, master, name):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.configure(width=560, height=100,
                    border_color="#ffffff", border_width=1)
        self.nick_entrys = []
        self.token_entrys = []
        self.start_buttons = []
        self.delete_buttons = []
        self.settings_buttons = []
        self.window_settings = []
        self.row = 1

        self.name_entry = customtkinter.CTkEntry(
            self, placeholder_text="Имя группы", width=160, height=20,
            border_color="#ffffff", border_width=1)
        if name != "":
            self.name_entry.insert(0, name)
        self.name_entry.grid(row=0, column=0, pady=(10, 0), padx=(5, 5))

        self.start_all_button = customtkinter.CTkButton(
            self, text="Запустить все", width=100, height=20, state=state,
            command=lambda: threading.Thread(target=start_all, args=(self,)).start())
        self.start_all_button.grid(row=0, column=2, pady=(10, 0), padx=(5, 5))

        self.add_button = customtkinter.CTkButton(
            self, text="+", width=20, height=20, command=self.add)
        self.add_button.grid(row=0, column=3, pady=(10, 0), padx=(10, 5))

    def delete(self, button):
        id = self.delete_buttons.index(button)
        if len(self.nick_entrys) == 1:
            group_id = groups.index(self)
            groups.pop(group_id)
            
            self.grid_forget()

        self.forget(id)



class Settings_Window(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Настройки")
        self.geometry("520x190")
        self.iconbitmap("images/logo.ico")
        
        self.slider = customtkinter.CTkSlider(
            self, width=500, height=18, from_=512, 
            to=8192, number_of_steps=10, command=self.slider_RAM)
        self.slider.place(x=10, y=10)
        
        self.RAM_label = customtkinter.CTkLabel(
            self, text="RAM для игры: автоматически")
        self.RAM_label.place(x=25, y=30)
        
        self.autoRAM_checkbox = customtkinter.CTkCheckBox(
            self, text="Автоматически", checkbox_height=20, 
            checkbox_width=20, command=self.autoRAM)
        self.autoRAM_checkbox.select()
        self.autoRAM_checkbox.place(x=360, y=30)

        self.minimal_graphics_checkbox = customtkinter.CTkCheckBox(
            self, text="Минимальные настройки графики",
            checkbox_height=20, checkbox_width=20)
        self.minimal_graphics_checkbox.place(x=30, y=70)
        
        self.discordRPC_checkbox = customtkinter.CTkCheckBox(
            self, text="Отключить Discord RPC",
            checkbox_height=20, checkbox_width=20)
        self.discordRPC_checkbox.place(x=30, y=110)
        
        self.auto_enter_checkbox = customtkinter.CTkCheckBox(
            self, text="Автовход на сервер",
            checkbox_height=20, checkbox_width=20)
        self.auto_enter_checkbox.place(x=30, y=150)

        self.fullscreen_checkbox = customtkinter.CTkCheckBox(
            self, text="Клиент в полный экран",
            checkbox_height=20, checkbox_width=20)
        self.fullscreen_checkbox.place(x=300, y=110)

        self.debug_mode_checkbox = customtkinter.CTkCheckBox(
            self, text="Режим отладки",
            checkbox_height=20, checkbox_width=20)
        self.debug_mode_checkbox.place(x=300, y=150)

    def slider_RAM(self, value):
        value = round(value)
        self.RAM_label.configure(text=f"RAM для игры: {value}")
        
    def autoRAM(self):
        if self.autoRAM_checkbox.get() == 0:
            self.slider.configure(state=customtkinter.NORMAL)
            value = self.slider.get()
            value = round(value)
            self.RAM_label.configure(text=f"RAM для игры: {value}")
        else:
            self.slider.configure(state=customtkinter.DISABLED)
            self.RAM_label.configure(text="RAM для игры: автоматически")
        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("ACCOUNT CHANGER by matswuuu")
        self.geometry("650x430")
        self.iconbitmap("images/logo.ico")

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
            command=lambda: threading.Thread(target=start_all, args=(self,)).start())
        self.start_all_button.place(x=10, y=10)

        self.get_token_button = customtkinter.CTkButton(    
            self, text="Токен", width=40, height=20, command=self.get_token)
        self.get_token_button.place(x=120, y=10)

        self.add_button = customtkinter.CTkButton(
            self, text="+", width=20, height=20, command=self.frame.add)
        self.add_button.place(x=590, y=10)

        self.add_group_button = customtkinter.CTkButton(
            self, text="+", width=20, height=20, fg_color="#8b02fa",
            hover_color="#5e00ab", command=lambda: self.frame.add_group(default_add=True))
        self.add_group_button.place(x=620, y=10)

        accounts_amount = config["config"]["amount"]
        accounts_amount = int(accounts_amount)
        
        for i in range(accounts_amount):
            nick = config["accounts_config"][f"{i}_nick"]
            token = config["accounts_config"][f"{i}_token"]
            self.frame.add(nick, token)
            
        groups_amount = config["config"]["groups_amount"]
        groups_amount = int(groups_amount)
            
        for g in range(groups_amount):
            group_config = f"{g}_group_config"
            name = config[group_config]["group_name"]
            group_length = config[group_config]["group_length"]
            group_length = int(group_length)
            
            self.frame.add_group(name)
            
            for i in range(group_length):
                n = config[group_config][f"{i}_group_nick"]
                t = config[group_config][f"{i}_group_token"]
                groups[g].add(n, t)
            
        if filename != "":
            self.enable()

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

        for group in groups:
            group.start_alfl_button.configure(state=state)
            for button in group.start_buttons:
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

    def save(self):
        def get_values(entrys_list):
            l = []
            for i in range(len(entrys_list)):
                value = entrys_list[i].get()
                l.append(value)

            return l

        nicks = get_values(self.frame.nick_entrys)
        tokens = get_values(self.frame.token_entrys)
        
        group_nicks = []
        group_tokens = []
        groups_names = []
        groups_RAM = []
        groups_minimal_graphics = []
        groups_discordRPC = []
        groups_auto_enter = []
        groups_fullscreen = []
        groups_debug_mode = []
        
        for i, group in enumerate(groups):
            n = get_values(group.nick_entrys)
            group_nicks.append(n)
            t = get_values(group.token_entrys)
            group_tokens.append(t)
            
            groups_names.append(group.name_entry.get())
            
            windows_settings = group.windows_settings[i]

            autoRAM = windows_settings.autoRAM_checkbox.get()
            autoRAM = bool(autoRAM)
            if autoRAM:
                RAM = -1
            else:
                RAM = windows_settings.slider.get()
            groups_RAM.append(RAM)
            minimal_graphics = windows_settings.minimal_graphics_checkbox.get()
            minimal_graphics = bool(minimal_graphics)
            groups_minimal_graphics.append(minimal_graphics)
            discordRPC = windows_settings.discordRPC_checkbox.get()
            discordRPC = bool(discordRPC)
            groups_discordRPC.append(discordRPC)
            auto_enter = windows_settings.auto_enter_checkbox.get()
            auto_enter = bool(auto_enter)
            groups_auto_enter.append(auto_enter)
            fullscreen = windows_settings.fullscreen_checkbox.get()
            fullscreen = bool(fullscreen)
            groups_fullscreen.append(fullscreen)
            debug_mode = windows_settings.debug_mode_checkbox.get()
            debug_mode = bool(debug_mode)
            groups_debug_mode.append(debug_mode)
            
        length = len(nicks)
        groups_length = len(groups)

        with codecs.open("config.ini", "r", encoding="utf-8") as config_file:
            config_file.read()
            
        for config_section in config.sections():
            config.remove_section(config_section)
            
        config.add_section("config")
        
        config.set("config", "amount", str(length))
        config.set("config", "groups_amount", str(groups_length))
        config.set("config", "filename", filename)
        
        config.add_section("accounts_config")
        for i in range(length):
            config.set("accounts_config", f"{i}_nick", nicks[i])
            config.set("accounts_config", f"{i}_token", tokens[i])
        
        for g, group in enumerate(group_nicks):
            group_config = f"{g}_group_config"
            config.add_section(group_config)
            
            group_length = len(group)
            for i in range(group_length):
                config.set(group_config, "group_length", str(group_length))
                config.set(group_config, "group_name", groups_names[g])
                config.set(group_config, f"{i}_group_nick", group_nicks[g][i])
                config.set(group_config, f"{i}_group_token", group_tokens[g][i])

        with codecs.open("config.ini", "w", encoding="utf-8") as config_file:
            config.write(config_file)

        self.destroy()


app = App()
app.protocol("WM_DELETE_WINDOW", app.save)
app.mainloop()
