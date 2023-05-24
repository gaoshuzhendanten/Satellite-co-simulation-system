#@Time : 2023/5/14 19:16
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog,messagebox,scrolledtext
import tkinter.font as tkFont
import os
import time
import threading
import sim_panel

class Config():
    def __init__(self,height=2000,samples_times=100,length=3000,radius=6371,speed=7900,num_satellites=3,area=[39,42,115,120],
                 num_generations=100, population_size=100, mutation_rate=0.2):
        self.HEIGHT = height  # 轨道高度
        self.SAMPLES_TIMES = samples_times  # 均匀随机抽样个数
        self.LENGTH = length  # 探测覆盖半径
        self.RADIUS = radius  # 地球半径
        self.SPEED = speed  # 总速度

        self.flag = True   #采样方法 True：均匀随机抽样
        self.path = "C:/Users/Administrator/PycharmProjects/Satellite co-simulation system/my_scenarios/"
        self.savename = "three_satellite.osf"
        self.area = area  # 探测区域范围
        self.area_name = "beijin"

        self.num_satellites = num_satellites  # 部署卫星个数
        self.satellites_names = ["x1","x2","x3"]

        self.num_generations = num_generations
        self.population_size = population_size
        self.mutation_rate = mutation_rate

        self.need_export_fun = False

class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)

class MY_GUI():
    def __init__(self, run_fun, export_fun):
        self.config = Config()
        self.root = tk.Tk()
        self.myfont = tkFont.Font(family="宋体", size=10, slant="roman")
        self.__run_fun = run_fun
        self.__export_fun = export_fun

    def mainloop(self):
        self.root.mainloop()

    def set_init_window(self):
        def use_select_window():
            select_window = tk.Tk()
            select_window.title("选择策略")
            # select_window.iconphoto(False, tk.PhotoImage(file='data/images/icon.png'))
            input_frame = ttk.Frame(select_window, padding=(20, 0, 20, 20))

            select_label = tk.Label(input_frame, text="目前的决策算法只支持遗传算法.")
            select_label.grid(row=0, column=0, columnspan=15)

            polic_label = tk.Label(input_frame,text="策略: ")
            polic_label.grid(row=4, column=0, columnspan=5,rowspan=10)

            default_var = tk.StringVar()
            default_var.set("default")
            values = ['遗传算法','默认项']
            polic = ttk.Combobox(master=input_frame,height=3,width=20,state="readonly",cursor="arrow",
                                 textvariable=default_var,
                                 values=values)
            polic.set(values[1])
            polic.grid(row=4,column=5)

            # bl_label = tk.Label(input_frame, text="策略: ")
            # polic_label.grid(row=4, column=0, columnspan=5, rowspan=10)

            yes_button = tk.Button(input_frame, text="确认",width=15,height=1,
                                        command=lambda: select_window.destroy())
            yes_button.grid(row=15, column=2)
            no_button = tk.Button(input_frame, text="取消",width=15,height=1,
                                   command=lambda: select_window.destroy())
            no_button.grid(row=15, column=8)

            input_frame.grid(row=0, column=0, columnspan=15)

        def use_set_window():
            def use_export_window():
                def get_path():
                    path = filedialog.askdirectory(title='请选择文件',initialdir=self.config.path)
                    path_text.insert('0', path)

                def save_export_set():
                    if not os.path.exists(path_text.get()):
                        messagebox.showinfo(title='error', message='路径不存在!')
                        return
                    self.config.path = path_text.get()
                    self.config.savename = save_name_txt.get()
                    self.config.area_name = area_name_txt.get().strip()
                    self.config.satellites_names = satellites_name_txt.get().split()
                    export_window.destroy()

                export_window = tk.Tk()
                export_window.title("导出设置")
                # export_window.iconphoto(False, tk.PhotoImage(file='data/images/icon.png'))
                export_window.attributes('-topmost', 'true')
                input_frame = ttk.Frame(export_window, padding=(5, 5, 5, 5))

                path_label = tk.Label(input_frame, text="导出路径: ")
                path_label.grid(row=1, column=0)
                path_text = tk.Entry(input_frame, width=50, state='normal')
                path_text.insert('0', self.config.path)
                path_text.grid(row=1,column=1,columnspan=4)

                button = tk.Button(input_frame, text='选择路径', command=get_path)
                button.grid(row=1, column=5)

                save_name_label = tk.Label(input_frame, text="文件名称: ")
                save_name_label.grid(row=2, column=0)
                save_name_txt = tk.Entry(input_frame)
                save_name_txt.insert('0', str(self.config.savename))
                save_name_txt.grid(row=2, column=1, columnspan=2)

                area_name_label = tk.Label(input_frame, text="区域名称: ")
                area_name_label.grid(row=3, column=0)
                area_name_txt = tk.Entry(input_frame)
                area_name_txt.insert('0', str(self.config.area_name))
                area_name_txt.grid(row=3, column=1, columnspan=2)

                satellites_name_label = tk.Label(input_frame, text="卫星名称: ")
                satellites_name_label.grid(row=4, column=0)
                satellites_name_txt = tk.Entry(input_frame)
                satellites_name_txt.insert('0', ' '.join(self.config.satellites_names))
                satellites_name_txt.grid(row=4, column=1, columnspan=2)

                ok_button = tk.Button(input_frame, text="确认", command=lambda: save_export_set())
                ok_button.config(width=15, height=1)
                ok_button.grid(row=5, column=2)

                no_button = tk.Button(input_frame, text="取消", command=export_window.destroy)
                no_button.config(width=15, height=1)
                no_button.grid(row=5, column=4)

                input_frame.grid(row=0, column=0)

            def use_ok_window():
                self.config.HEIGHT = int(highe_txt.get().strip())
                self.config.SAMPLES_TIMES = int(highe_txt.get().strip())
                self.config.flag = True if sample_fun_txt.get()=="均匀随机抽样" else False
                self.config.LENGTH = int(length_txt.get().strip())
                self.config.RADIUS = int(radius_txt.get().strip())
                self.config.num_satellites = int(num_satellites_txt.get().strip())
                lot = lot_txt.get().strip().split('~')
                lat = lat_txt.get().strip().split('~')
                self.config.area = [int(lot[0]),int(lot[1]),int(lat[0]),int(lat[1])]
                self.config.num_generations = int(num_generations_txt.get().strip())
                self.config.population_size = int(population_size_txt.get().strip())
                self.config.mutation_rate = float(mutation_rate_txt.get().strip())
                set_vars_field()
                set_window.destroy()

            set_window = tk.Tk()
            set_window.title("设置参数")
            # set_window.iconphoto(False, tk.PhotoImage(file='data/images/icon.png'))
            input_frame = ttk.Frame(set_window, padding=(5, 5, 5, 5))

            highe_label = tk.Label(input_frame, text="轨道高度: ")
            smaple_label = tk.Label(input_frame, text="随机抽样数: ")
            smaple_fun_label = tk.Label(input_frame, text="抽样方法: ")
            length_label = tk.Label(input_frame, text="探测覆盖半径: ")
            radius_label = tk.Label(input_frame, text="行星半径: ")
            num_satellites_label = tk.Label(input_frame, text="部署卫星数: ")
            lot_label = tk.Label(input_frame, text="探测区域经度范围: ")
            lat_label = tk.Label(input_frame, text="纬度范围: ")
            num_generations_label = tk.Label(input_frame, text="迭代次数")
            population_size_label = tk.Label(input_frame, text="初始种群: ")
            mutation_rate_label = tk.Label(input_frame, text="学习率: ")

            highe_label.grid(row=1, column=0)
            smaple_label.grid(row=2, column=0)
            smaple_fun_label.grid(row=2, column=2)
            length_label.grid(row=3, column=0)
            radius_label.grid(row=3, column=2)
            num_satellites_label.grid(row=4, column=0)
            lat_label.grid(row=5, column=0)
            lot_label.grid(row=5, column=2)
            num_generations_label.grid(row=6, column=0)
            population_size_label.grid(row=7, column=0)
            mutation_rate_label.grid(row=8, column=0)

            highe_txt = tk.Entry(input_frame)
            highe_txt.insert(0,str(self.config.HEIGHT))
            highe_txt.grid(row=1, column=1,columnspan=1)

            sample_txt = tk.Entry(input_frame)
            sample_txt.insert(0, str(self.config.SAMPLES_TIMES))
            sample_txt.grid(row=2, column=1)

            sample_fun_values = ['均匀随机抽样', '等距随机抽样']
            sample_fun_txt = ttk.Combobox(master=input_frame, height=3, width=15, state="readonly", cursor="arrow",
                                 values=sample_fun_values)
            sample_fun_txt.set(sample_fun_values[0])
            sample_fun_txt.grid(row=2, column=3, columnspan=1)

            length_txt = tk.Entry(input_frame)
            length_txt.insert(0, str(self.config.LENGTH))
            length_txt.grid(row=3, column=1)

            radius_txt = tk.Entry(input_frame)
            radius_txt.insert(0, str(self.config.RADIUS))
            radius_txt.grid(row=3, column=3)

            num_satellites_txt = tk.Entry(input_frame)
            num_satellites_txt.insert(0, str(self.config.num_satellites))
            num_satellites_txt.grid(row=4, column=1)

            lot_txt = tk.Entry(input_frame)
            lot_txt.insert(0, str(self.config.area[0]) + '~' + str(self.config.area[1]))
            lot_txt.grid(row=5, column=1)

            lat_txt = tk.Entry(input_frame)
            lat_txt.insert(0, str(self.config.area[2]) + '~' + str(self.config.area[3]))
            lat_txt.grid(row=5, column=3)

            num_generations_txt = tk.Entry(input_frame)
            num_generations_txt.insert(0, str(self.config.num_generations))
            num_generations_txt.grid(row=6, column=1)

            population_size_txt = tk.Entry(input_frame)
            population_size_txt.insert(0, str(self.config.population_size))
            population_size_txt.grid(row=7, column=1)

            mutation_rate_txt = tk.Entry(input_frame)
            mutation_rate_txt.insert(0, str(self.config.mutation_rate))
            mutation_rate_txt.grid(row=8, column=1)

            export_button = tk.Button(input_frame, text="导出", command=lambda:use_export_window())
            export_button.config(width=15,height=1)
            export_button.grid(row=9,column=1)

            ok_button = tk.Button(input_frame, text="确认",command=lambda:use_ok_window())
            ok_button.config(width=15,height=1)
            ok_button.grid(row=9, column=2)

            input_frame.grid(row=0, column=0)

        def use_run_window():
            self.config.need_export_fun = True
            self.word_thread = ThreadWithResult(target=self.__run_fun, args=(self.config, output_txt,))
            self.word_thread.start()

        def use_sim_window():
            if self.config.need_export_fun:
                self.__export_fun(self.config.path+self.config.savename, self.word_thread.result, self.config.area, self.config.area_name)
                output_txt.insert(tk.INSERT,"INFO: export ok\n")
                output_txt.see(tk.END)
            output_txt.insert(tk.INSERT, "INFO: start simulation\n")
            output_txt.see(tk.END)
            output_txt.update()
            time.sleep(2)
            self.root.destroy()
            sim_panel.sim_gui_start()

        def set_vars_field():
            variables_field.config(state="normal")
            vars_text = f"轨道高度: {self.config.HEIGHT}\n"
            if self.config.flag:
                vars_text += f"采样方法: 均匀随机抽样\n"
            else:
                vars_text += f"采样方法: 固定等距抽样\n"
            vars_text += f"随机抽样数: {self.config.SAMPLES_TIMES}\n"
            vars_text += f"探测覆盖半径: {self.config.LENGTH}\n"
            vars_text += f"地球半径: {self.config.RADIUS}\n"
            vars_text += f"部署卫星数: {self.config.num_satellites}\n"
            vars_text += f"探测区域: {self.config.area_name}\n"
            if len(self.config.area)!=4:
                vars_text += f"探测区域坐标: \n"
            else:
                vars_text += f"探测区域经度范围: {self.config.area[0]} {self.config.area[1]}\n"
                vars_text += f"探测区域纬度范围: {self.config.area[2]} {self.config.area[3]}\n"
            vars_text += f"决策系统迭代次数: {self.config.num_generations}\n"
            vars_text += f"初始种群数: {self.config.population_size}\n"
            vars_text += f"学习率: {self.config.mutation_rate}\n"
            variables_field.delete(1.0, "end")
            variables_field.insert(1.0, vars_text)
            variables_field.config(state="disabled")

        self.root.title("多星协同决策系统")
        self.root.iconphoto(False, tk.PhotoImage(file='data/images/icon.png'))
        # column - commond
        select_button = tk.Button(self.root, text="选择策略", command=lambda: use_select_window())
        select_button.config(width=25, height=1)
        select_button.grid(row=1, column=0)
        set_button = tk.Button(self.root, text="设置参数", command=lambda: use_set_window())
        set_button.config(width=25, height=1)
        set_button.grid(row=2, column=0)
        run_button = tk.Button(self.root, text="运行决策", command=lambda: use_run_window())
        run_button.config(width=25, height=1)
        run_button.grid(row=3, column=0)
        sim_button = tk.Button(self.root, text="运行仿真", command=lambda: use_sim_window())
        sim_button.config(width=25, height=1)
        sim_button.grid(row=4, column=0)

        variables_field_label = tk.Label(self.root, text="仿真变量")
        variables_field_label.grid(row=5, column=0)
        variables_field = scrolledtext.ScrolledText(self.root, width=25, height=7)
        variables_field.grid(row=6, column=0, rowspan=5)
        set_vars_field()

        # column - output
        output_label = tk.Label(self.root, text="系统输出")
        output_label.grid(row=0, column=5)
        output_txt = tk.Text(self.root, height=24, width=40)
        output_txt.grid(row=1, column=5, rowspan=10)
        output_txt.config(state="normal", font=("Courier", 10, "roman"))

def gui_start(run_fun, export_fun):
    gui = MY_GUI(run_fun, export_fun)
    gui.set_init_window()
    gui.mainloop()


# test
# if __name__=="__main__":
#     gui_start(lambda x:x+1)
