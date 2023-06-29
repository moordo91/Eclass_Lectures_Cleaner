from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import json
import datetime as dt
from tkinter_control import center_window

def run_selenium():
    options = Options()
    options.add_experimental_option('detach', True) # 브라우저 바로 닫힘 방지
    options.add_experimental_option("excludeSwitches", ['enable-logging']) # 불필요한 메시지 제거

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://eclass.seoultech.ac.kr/ilos/main/member/login_form.acl")
    driver.implicitly_wait(time_to_wait=1)
    
    windows = driver.window_handles
    
    for w in windows:
        if w != windows[0]:
            driver.switch_to.window(w)
            driver.close()
            
    driver.switch_to.window(windows[0])
    
    return driver

def login(driver):
    credentials = json.load(open("credentials.json", encoding = 'utf-8'))
    driver.find_element(By.ID, "usr_id").send_keys(credentials["username"])
    driver.find_element(By.ID, "usr_pwd").send_keys(credentials["password"])
    driver.find_element(By.ID, "usr_pwd")
    driver.find_element(By.CLASS_NAME, "btntype").click()

def check_class(driver):
    driver.execute_script("popTodo()")
    elements = driver.find_elements(By.CLASS_NAME, "todo_title")
    for element in elements:
        if "온라인강의" in element.get_attribute("innerText"):
            element.find_element(By.XPATH, "..").click()
            return False
    messagebox.showinfo("확인", "모든 강의를 수강하셨습니다!")
    return True

def check_video(driver):
    def time2seconds(time_str):
        if ':' not in time_str:
            return int(time_str)
        parts = time_str.split(':')
        if len(parts) == 3:
            t = dt.datetime.strptime(time_str, "%H:%M:%S")
            return int(t.hour*3600 + t.minute*60 + t.second)
        elif len(parts) == 2:
            t = dt.datetime.strptime(time_str, "%M:%S")
            return int(t.minute*60 + t.second)
    
    check_all = False
    elements = driver.find_elements(By.ID, "per_text")
    for element in elements:
        if "100%" in element.get_attribute("innerText"):
            continue
        target = element.find_element(By.XPATH, "../..")
        time_ratio = target.find_element(By.XPATH, "./child::*[2]/child::*[3]").get_attribute("innerText")
        times = time_ratio.split(" / ")
        curr_time = time2seconds(times[0])
        tot_time = time2seconds(times[1])
        
        lecture = target.find_element(By.CLASS_NAME, "site-mouseover-color")
        lec_title = lecture.get_attribute("innerText")
        lecture.click()
        driver.implicitly_wait(time_to_wait=1)

        return check_all, curr_time, tot_time, lec_title
    
    check_all = True
    if check_all:
        driver.get("https://eclass.seoultech.ac.kr/ilos/main/main_form.acl")
        return True, None, None, None

def watch_video(driver, curr_time, tot_time, lec_title):
    def update_progress_label():
        if progressbar['value'] < 100:
            return f"Current Progress: {progressbar['value']:.1f}%"
        else:
            return "Complete Watching."
    
    def update_progress():
        progressbar['value'] = progressbar['value'] + (300 / (tot_time + 240))
        value_label['text'] = update_progress_label()
        if progressbar['value'] < progressbar['maximum']:
            bar.after(3000, update_progress)
        else:
            bar.quit()
    
    def quit_program(driver):
        msg_box = messagebox.askquestion("종료", 
                                         "프로그램을 종료하시겠습니까?\n(현재 진행 상황이 반영되지 않을 수 있습니다.)",
                                         parent=bar)
        if msg_box == 'yes':
            bar.destroy()
            driver.close()
        else:
            pass
    
    bar = Tk();
    center_window(bar)
    bar.wm_attributes("-topmost", 1)
    bar.title("Progress Bar")

    title = Label(bar, text=lec_title, font=("맑은 고딕", 10, "bold"))
    title.pack(pady=(10, 0))
    
    notion = Label(bar, text="강의 진행률은 프로그램의 정확성 향상을 위해\n실제 진행률보다 보수적으로 표시됩니다.", font=("맑은 고딕", 9))
    notion.pack(padx=10, pady=5)
    
    progressbar = ttk.Progressbar(bar, maximum=100, value=(curr_time * 100 / (tot_time+240)), length=300)
    progressbar.pack(padx=10, pady=5)
    
    value_label = ttk.Label(bar, text=update_progress_label())
    value_label.pack(padx=10, pady=5)
    
    button = Button(bar, text="Quit", command=lambda: quit_program(driver), width=10)
    button.pack(pady=10)
    
    update_progress()
    bar.mainloop()
    
    return bar

def main():
    driver = run_selenium()
    login(driver)
    while check_class(driver) != True:
        while True:
            check_all, curr_time, tot_time, lec_title = check_video(driver)
            if check_all != True:
                bar = watch_video(driver, curr_time, tot_time, lec_title)
                bar.destroy()
                driver.back()
                driver.refresh()
            else:
                break
        driver.get("https://eclass.seoultech.ac.kr/ilos/main/main_form.acl")
    
if __name__ == "__main__":
    main()