import run
from tkinter import *
from tkinter import ttk
import json

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

def check_data(username, password):
    save_credentials({"username": username.get(), "password": password.get()})
    run.main()
    
window = Tk()
window.title("Cleaner")
title = ttk.Label(window, text="e-Class 강의 클리너", font=("나눔고딕", 12, "bold"))
title.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 5), sticky="W")

frame = ttk.LabelFrame(window, text="Info")
frame.grid(row=1, column=0, padx=10, pady=5)

username, password = StringVar(), StringVar()

credentials = get_credentials()
if credentials is not None:
    username.set(credentials["username"])
    password.set(credentials["password"])

ttk.Label(frame, text="아이디 :").grid(row=0, column=0, padx=10, pady=5, sticky="E")
ttk.Label(frame, text="비밀번호 :").grid(row=1, column=0, padx=10, pady=5, sticky="E")
ttk.Entry(frame, textvariable=username).grid(row=0, column=1, padx=(1, 10), pady=5)
ttk.Entry(frame, textvariable=password, show='*').grid(row=1, column=1, padx=(1, 10), pady=(5, 10))
ttk.Button(window, text="Run", command=lambda: check_data(username, password), width=13).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()