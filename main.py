import codecs
import threading
import subprocess
import os
import time
import json
import platform
import shutil
from tkinter import filedialog
from PIL import Image

import customtkinter

system = platform.system()
if system == "Linux":
    d = "/"
elif system == "Windows":
    d = "C:/"

with open("config.json", "r") as f:
    config = json.load(f)

filename = config["fileName"]
groups = []
all_settings = {}
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

                    global updates_dir
                    updates_dir = cristalix_dir + "/updates/Minigames"

                    shutil.copy(updates_dir + "/options.txt", "graphics settings/user")
                    shutil.copy(updates_dir + "/optionsof.txt", "graphics settings/user")

threading.Thread(target=get_dir).start()


def login(self, id, nick, token):
    w = self.window_settings[id]
    if w is None:
        settings = {
            "RAM": -1,
            "minimal_graphics": False,
            "discordRPC": False,
            "auto_enter": False,
            "fullscreen": False,
            "debug_mode": False
        }
    else:
        settings = w.settings

    print(settings)

    def set_graphics(var):
        shutil.copy(f"graphics settings/{var}/options.txt", updates_dir) 
        shutil.copy(f"graphics settings/{var}/optionsof.txt", updates_dir)

    if settings["minimal_graphics"]: 
        set_graphics("minimal")
    else:
        set_graphics("user")
    
    with open(launcher_dir, "r") as f:
        launcher_dict = json.load(f)
    
        launcher_dict["accounts"] = {}
        launcher_dict["accounts"][nick] = token
        launcher_dict["currentAccount"] = nick
        launcher_dict["updatesDirectory"] = cristalix_dir
        launcher_dict["minimalGraphics"] = settings["minimal_graphics"]
        launcher_dict["fullscreen"] = settings["fullscreen"]
        launcher_dict["discordRPC"] = settings["discordRPC"]
        launcher_dict["autoEnter"] = settings["auto_enter"]
        launcher_dict["debugMode"] = settings["debug_mode"]
        launcher_dict["memoryAmount"] = settings["RAM"]
        
        with open(launcher_dir, "w") as f:
            json.dump(launcher_dict, f)

    if filename.endswith("jar"):
        threading.Thread(target=lambda: subprocess.call(
            ["java", "-jar", filename])).start()
    else:
        threading.Thread(
            target=lambda: os.startfile(filename)).start()


def start_all(self):
    def get_values(entrys_list):
        l = []
        for i in range(len(entrys_list)):
            value = entrys_list[i].get()
            l.append(value)

        return l

    nicks = get_values(self.nick_entrys)
    tokens = get_values(self.token_entrys)

    for i in range(len(nicks)):
        login(self, i, nicks[i], tokens[i])
        time.sleep(10)


def start(self, button):
    id = self.start_buttons.index(button)
    nick = self.nick_entrys[id].get()
    token = self.token_entrys[id].get()

    login(self, id, nick, token)


class Scrollable_Frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.configure(width=630, height=340)
        self.nick_entrys = []
        self.token_entrys = []
        self.start_buttons = []
        self.delete_buttons = []
        self.settings_buttons = []
        self.window_settings = []
        self.all_settings = []
        self.row = 0

    def add_group(self, name="", default_add=False):
        group = Group_Frame(self, name)
        if default_add:
            group.add()
        group.grid(row=self.row, column=0, pady=(   
            15, 15), padx=(10, 10), columnspan=5)
        groups.append(group)

        self.row = self.row + 1

    def add(self, nick="", token="", 
            settings = {
                "RAM": -1,
                "minimal_graphics": False,
                "discordRPC": False,
                "auto_enter": False,
                "fullscreen": False,
                "debug_mode": False
            }):
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
        
        image = customtkinter.CTkImage(
            dark_image=Image.open("images/settings_gear.png"), size=(18, 18))
        
        settings_button = customtkinter.CTkButton(
            self, text="", width=18, height=18, 
            image=image, border_spacing=0, border_width=0,
            fg_color="#ffffff", hover_color="#ffffff",
            command=lambda: self.open_settings(settings_button))
        settings_button.grid(row=self.row, column=2, pady=(10, 0), padx=(0, 0))
        self.settings_buttons.append(settings_button)

        settings_window = None
        self.window_settings.append(settings_window)
        self.all_settings.append(settings)

        start_button = customtkinter.CTkButton(
            self, text="Запустить", width=100, height=25, state=state,
            command=lambda: start(self, start_button))
        start_button.grid(row=self.row, column=3, pady=(10, 0), padx=(10, 10))
        self.start_buttons.append(start_button)

        delete_button = customtkinter.CTkButton(
            self, text="-", width=20, height=25, command=lambda: self.delete(delete_button))
        delete_button.grid(row=self.row, column=4, pady=(10, 0), padx=(0, 5))
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
        self.window_settings.pop(id)
        
    def open_settings(self, button):
        id = self.settings_buttons.index(button)
        
        for w in self.window_settings:
            if w is not None and w.winfo_exists():
                w.focus()
                return

        settings_window = self.window_settings[id]
        if settings_window is None:
            self.window_settings[id] = Settings_Window(master=self, 
                                                       settings=self.all_settings[id])
        else:
            self.window_settings[id] = Settings_Window(master=self, 
                                                       settings=self.window_settings[id])


class Group_Frame(Scrollable_Frame):
    def __init__(self, master, name):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.configure(width=610, height=100,
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
        self.start_all_button.grid(row=0, column=3, pady=(10, 0), padx=(5, 5))

        self.add_button = customtkinter.CTkButton(
            self, text="+", width=20, height=20, command=self.add)
        self.add_button.grid(row=0, column=4, pady=(10, 0), padx=(0, 5))

    def delete(self, button):
        id = self.delete_buttons.index(button)
        if len(self.nick_entrys) == 1:
            group_id = groups.index(self)
            groups.pop(group_id)
            
            self.grid_forget()

        self.forget(id)
        

class Settings_Window(customtkinter.CTkToplevel):
    def __init__(self, master, settings):
        super().__init__(master)
        self.title("Настройки")
        self.geometry("520x190")
        self.iconbitmap("images/logo.ico")
        self.protocol("WM_DELETE_WINDOW", self.save)
        
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
        
        RAM = settings["RAM"]
        if RAM == -1:
            self.slider.configure(state=customtkinter.DISABLED)
        else:
            self.autoRAM_checkbox.deselect()
            self.slider.set(RAM)
            self.slider_RAM(RAM)

        self.minimal_graphics_checkbox = customtkinter.CTkCheckBox(
            self, text="Минимальные настройки графики",
            checkbox_height=20, checkbox_width=20)
        self.minimal_graphics_checkbox.place(x=30, y=70)
        if settings["minimal_graphics"]:
            self.minimal_graphics_checkbox.select()
        
        self.discordRPC_checkbox = customtkinter.CTkCheckBox(
            self, text="Отключить Discord RPC",
            checkbox_height=20, checkbox_width=20)
        self.discordRPC_checkbox.place(x=30, y=110)
        if settings["discordRPC"]:
            self.discordRPC_checkbox.select()
        
        self.auto_enter_checkbox = customtkinter.CTkCheckBox(
            self, text="Автовход на сервер",
            checkbox_height=20, checkbox_width=20)
        self.auto_enter_checkbox.place(x=30, y=150)
        if settings["auto_enter"]:
            self.auto_enter_checkbox.select()

        self.fullscreen_checkbox = customtkinter.CTkCheckBox(
            self, text="Клиент в полный экран",
            checkbox_height=20, checkbox_width=20)
        self.fullscreen_checkbox.place(x=300, y=110)
        if settings["fullscreen"]:
            self.fullscreen_checkbox.select()

        self.debug_mode_checkbox = customtkinter.CTkCheckBox(
            self, text="Режим отладки",
            checkbox_height=20, checkbox_width=20)
        self.debug_mode_checkbox.place(x=300, y=150)
        if settings["debug_mode"]:
            self.debug_mode_checkbox.select()

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
            
    def save(self):
        autoRAM = self.autoRAM_checkbox.get()
        autoRAM = bool(autoRAM)
        if autoRAM:
            RAM = -1
        else:
            RAM = self.slider.get()
        RAM = round(RAM)
        minimal_graphics = self.minimal_graphics_checkbox.get()
        minimal_graphics = bool(minimal_graphics)
        discordRPC = self.discordRPC_checkbox.get()
        discordRPC = bool(discordRPC)
        auto_enter = self.auto_enter_checkbox.get()
        auto_enter = bool(auto_enter)
        fullscreen = self.fullscreen_checkbox.get()
        fullscreen = bool(fullscreen)
        debug_mode = self.debug_mode_checkbox.get()
        debug_mode = bool(debug_mode)

        self.settings = {
            "RAM": RAM,
            "minimal_graphics": minimal_graphics,
            "discordRPC": discordRPC,
            "auto_enter": auto_enter,
            "fullscreen": fullscreen,
            "debug_mode": debug_mode
        }
            
        self.destroy()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("ACCOUNT CHANGER by matswuuu")
        self.geometry("670x430")
        self.iconbitmap("images/logo.ico")
        self.protocol("WM_DELETE_WINDOW", self.save)

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
            command=lambda: threading.Thread(target=start_all, args=(self.frame,)).start())
        self.start_all_button.place(x=10, y=10)

        self.get_token_button = customtkinter.CTkButton(    
            self, text="Токен", width=40, height=20, command=self.get_token)
        self.get_token_button.place(x=120, y=10)

        self.add_button = customtkinter.CTkButton(
            self, text="+", width=20, height=20, command=self.frame.add)
        self.add_button.place(x=610, y=10)

        self.add_group_button = customtkinter.CTkButton(
            self, text="+", width=20, height=20, fg_color="#8b02fa",
            hover_color="#5e00ab", command=lambda: self.frame.add_group(default_add=True))
        self.add_group_button.place(x=640, y=10)
        
        with open("config.json", "r") as f:
            config_dict = json.load(f)
            
        accounts_amount = len(config_dict["accounts"])
        accounts = config_dict["accounts"]
        for i in range(accounts_amount):
            a = accounts[str(i)]
            nick = a["nick"]
            token = a["token"]
            settings = {
                "RAM": a["RAM"],
                "minimal_graphics": a["minimalGraphics"],
                "discordRPC": a["discordRPC"],
                "auto_enter": a["autoEnter"],
                "fullscreen": a["fullscreen"],
                "debug_mode": a["debugMode"]
            }
            
            self.frame.add(nick, token, settings)
            
        groups_amount = len(config_dict["groups"])
        groups_dict = config_dict["groups"]
        for g in range(groups_amount):
            g = str(g)
            name = groups_dict[g]["name"] 
            self.frame.add_group(name)
            
            group_amount = len(groups_dict[g]) - 1
            for i in range(group_amount):
                group = groups_dict[g][str(i)]
                
                nick = group["nick"]
                token = group["token"]
                settings = {
                    "RAM": group["RAM"],
                    "minimal_graphics": group["minimalGraphics"],
                    "discordRPC": group["discordRPC"],
                    "auto_enter": group["autoEnter"],
                    "fullscreen": group["fullscreen"],
                    "debug_mode": group["debugMode"]
                }
                
                groups[int(g)].add(nick, token, settings)
            
            
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
            group.start_all_button.configure(state=state)
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
        with open("config.json", "r") as f:
            config_dict = json.load(f)

        def check_window(w):
            if w is None:
                settings = {
                    "RAM": -1,
                    "minimal_graphics": False,
                    "discordRPC": False,
                    "auto_enter": False,
                    "fullscreen": False,
                    "debug_mode": False
                }
            else:
                settings = w.settings
                
            return settings
        
        accounts = {}
        length = len(self.frame.nick_entrys)
        for i in range(length):
            nick = self.frame.nick_entrys[i].get()
            token = self.frame.token_entrys[i].get()

            if nick == "" or token == "":
                continue
            
            w = self.frame.window_settings[i]
            settings = check_window(w)
            
            accounts[len(accounts)] = {
                "nick": nick,
                "token": token,
                "RAM": settings["RAM"],
                "minimalGraphics": settings["minimal_graphics"],
                "discordRPC": settings["discordRPC"],
                "autoEnter": settings["auto_enter"],
                "fullscreen": settings["fullscreen"],
                "debugMode": settings["debug_mode"]
            }
            

        groups_accounts = {}
        for g, group in enumerate(groups):
            groups_accounts[g] = {}
            groups_accounts[g]["name"] = group.name_entry.get()
            
            length = len(group.nick_entrys)
            for i in range(length):
                nick = group.nick_entrys[i].get()
                token = group.token_entrys[i].get()

                if nick == "" or token == "":
                    continue
            
                w = group.window_settings[i]
                settings = check_window(w)
                
                groups_accounts[g][len(groups_accounts[g]) - 1] = {
                    "nick": nick,
                    "token": token,
                    "RAM": settings["RAM"],
                    "minimalGraphics": settings["minimal_graphics"],
                    "discordRPC": settings["discordRPC"],
                    "autoEnter": settings["auto_enter"],
                    "fullscreen": settings["fullscreen"],
                    "debugMode": settings["debug_mode"]
                }
                
        config_dict["fileName"] = filename       
        config_dict["accounts"] = accounts
        config_dict["groups"] = groups_accounts
        
        with open("config.json", "w") as f:
                json.dump(config_dict, f)
        
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
