import run
from tkinter import *
from tkinter import ttk
from tkinter_control import center_window
import urllib
import base64
import json
import sys

def save_credentials(credentials):
    with open("credentials.json", "w") as f:
        json.dump(credentials, f)

def get_credentials():
    try:
        with open("credentials.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        default_credentials = {"username": "", "password": ""}
        with open("credentials.json", "w") as f:
            json.dump(default_credentials, f)
        return default_credentials

def input_data(*event):
    save_credentials({"username": username.get(), "password": password.get()})
    run.main()

    
window = Tk()

img_url = "https://github.com/moordo91/Eclass_Lectures_Cleaner/blob/main/applicator.png?raw=true"
with urllib.request.urlopen(img_url) as url:
    raw_data = url.read()

b64_data = base64.encodebytes(raw_data)
image = PhotoImage(data=b64_data)

window.tk.call('wm', 'iconphoto', window._w, image)

window.update()
center_window(window)

window.title("Cleaner")
title = ttk.Label(window, text="Eclass Lectures Cleaner", font=("맑은 고딕", 10))
title.pack(padx=15, pady=(15, 5))

frame1 = ttk.LabelFrame(window, text="Info")
frame1.pack(padx=10, pady=5)

username, password = StringVar(), StringVar()

credentials = get_credentials()
if credentials is not None:
    username.set(credentials["username"])
    password.set(credentials["password"])

ttk.Label(frame1, text="아이디 :").grid(row=1, column=0, padx=10, pady=5, sticky="E")
ttk.Label(frame1, text="비밀번호 :").grid(row=2, column=0, padx=10, pady=5, sticky="E")
ttk.Entry(frame1, textvariable=username).grid(row=1, column=1, padx=(1, 10), pady=5)

pw_entry = ttk.Entry(frame1, textvariable=password, show='*')
pw_entry.grid(row=2, column=1, padx=(1, 10), pady=(5, 10))
pw_entry.bind("<Return>", input_data)

frame2 = ttk.Frame(window)
frame2.pack(padx=10, pady=5)

ttk.Button(frame2, text="Run", command=input_data, width=13).grid(row=0, column=0, padx=20, pady=(0, 5))
ttk.Button(frame2, text="Exit", command=sys.exit, width=7).grid(row=0, column=1, padx=20, pady=(0, 5))

window.mainloop()