def center_window(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()

    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    root.geometry("+{}+{}".format(position_left, position_top))
    root.resizable(False, False)