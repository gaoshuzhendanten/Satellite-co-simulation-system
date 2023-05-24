#@Time : 2023/5/17 8:56
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog,messagebox
import main
import os

DEAUFT_PATH = "C:/Users/Administrator/PycharmProjects/Satellite co-simulation system/my_scenarios/"

class SIM_GUI():
    def __init__(self):
        self.root = tk.Tk()

    def mainloop(self):
        self.root.mainloop()

    def set_init_window(self):

        def use_load_window():

            def get_path():
                path = filedialog.askopenfilename(title='请选择文件', initialdir=DEAUFT_PATH, defaultextension=".osf")
                path_text.insert('0', path)

            def save_load_set():
                temp_path = path_text.get()
                if not os.path.exists(temp_path):
                    messagebox.showinfo(title='error', message='路径不存在!')
                    return
                load_window.destroy()
                self.root.destroy()
                main.import_scenario(temp_path)

            load_window = tk.Tk()
            load_window.title("加载环境")
            # load_window.iconphoto(False, tk.PhotoImage(file='data/images/icon.png'))
            input_frame = ttk.Frame(load_window, padding=(5, 5, 5, 5))

            path_label = tk.Label(input_frame, text="加载路径: ")
            path_label.grid(row=1, column=0)
            path_text = tk.Entry(input_frame, width=50, state='normal')
            path_text.grid(row=1, column=1, columnspan=4)
            button = tk.Button(input_frame, text='选择路径', command=get_path)
            button.grid(row=1, column=5)

            ok_button = tk.Button(input_frame, text="确认", command=lambda: save_load_set())
            ok_button.config(width=15, height=1)
            ok_button.grid(row=2, column=2)

            no_button = tk.Button(input_frame, text="取消", command=load_window.destroy)
            no_button.config(width=15, height=1)
            no_button.grid(row=2, column=4)

            input_frame.grid(row=0, column=0, columnspan=15)

        def use_create_window():
            self.root.destroy()
            main.main()

        def use_config_window():
            main.configure_sim()

        self.root.title("仿真系统")
        self.root.iconphoto(False, tk.PhotoImage(file='data/images/icon.png'))
        input_frame = ttk.Frame(self.root, padding=(5, 5, 5, 5))
        load_button = tk.Button(input_frame, text="加载环境", command=lambda: use_load_window())
        load_button.config(width=20, height=2)
        load_button.grid(row=1, column=0)
        creat_button = tk.Button(input_frame, text="创建环境", command=lambda: use_create_window())
        creat_button.config(width=20, height=2)
        creat_button.grid(row=2, column=0)
        config_button = tk.Button(input_frame, text="设置", command=lambda: use_config_window())
        config_button.config(width=20, height=2)
        config_button.grid(row=3, column=0)
        input_frame.grid(row=0, column=0, columnspan=15)


def sim_gui_start():
    sim_gui = SIM_GUI()
    sim_gui.set_init_window()
    sim_gui.mainloop()

# sim_gui_start()
