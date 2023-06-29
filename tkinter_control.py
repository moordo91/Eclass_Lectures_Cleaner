from tkinter import messagebox

def center_window(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()

    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    root.geometry("+{}+{}".format(position_left, position_top))
    root.resizable(False, False)
    root.wm_attributes("-topmost", 1)
    root.wm_attributes("-topmost", 0)

def update_progress_label(progressbar):
    if progressbar['value'] < 100:
        return f"Current Progress: {progressbar['value']:.1f}%"
    else:
        return "Complete Watching."

def update_progress(root, tot_time, progressbar, value_label):
    progressbar['value'] = progressbar['value'] + (300 / (tot_time + 240))
    value_label['text'] = update_progress_label(progressbar)
    if progressbar['value'] < progressbar['maximum']:
        root.after(3000, lambda: update_progress(root, tot_time, progressbar, value_label))
    else:
        root.quit()

def close_bar(driver, root):
    msg_box = messagebox.askquestion("종료", 
                                    "프로그램을 종료하시겠습니까?\n(현재 진행 상황이 반영되지 않을 수 있습니다.)",
                                    parent=root)
    if msg_box == 'yes':
        root.destroy()
        driver.close()
    else:
        pass
    
if __name__ == "__main__":
    pass