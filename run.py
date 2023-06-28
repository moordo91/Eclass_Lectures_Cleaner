from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import tkinter as tk
from tkinter import messagebox
import json

def run_selenium():
    options = Options()
    options.add_experimental_option('detach', True) # 브라우저 바로 닫힘 방지
    options.add_experimental_option("excludeSwitches", ['enable-logging']) # 불필요한 메시지 제거

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://eclass.seoultech.ac.kr/ilos/main/member/login_form.acl")
    driver.implicitly_wait(time_to_wait=1)
    
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
            return
    messagebox.showinfo("확인", "모든 강의를 수강하셨습니다!")

def check_video(driver):
    def time2seconds(time_string):
        parts = time_string.split(":")
        return int(parts[0]) * 60 + int(parts[1]);
    
    elements = driver.find_elements(By.ID, "per_text")
    for element in elements:
        if "100%" in element.get_attribute("innerText"):
            continue
        target = element.find_element(By.XPATH, "../..")
        time_ratio = target.find_element(By.XPATH, "./child::*[2]/child::*[3]").get_attribute("innerText")
        times = time_ratio.split(" / ")
        current_time = time2seconds(times[0])    
        total_time = time2seconds(times[1])
        time_info = [current_time, total_time]
        target.find_element(By.CLASS_NAME, "site-mouseover-color").click()
        return time_info
    driver.get("https://eclass.seoultech.ac.kr/ilos/main/main_form.acl")


    
def main():
    driver = run_selenium()
    login(driver)
    check_class(driver)
    time_info = check_video(driver)
    
if __name__ == "__main__":
    main()