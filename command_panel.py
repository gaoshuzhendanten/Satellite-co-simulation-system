import tkinter as tk

# There are probably better ways to code this, but it works just as well as you'd want.
# For loops create evil bugs for some reason, so I just did a lot of copy-pasting as a substitude.

def use_command_panel(vessels, bodies, surface_points, barycenters, maneuvers, radiation_pressures, atmospheric_drags, projections, plots, auto_dt_buffer,
                      sim_time, delta_t, cycle_time, output_rate, cam_strafe_speed, cam_rotate_speed, rapid_compute_buffer, scene_lock):
    command_buffer = []

    def on_panel_close():
        root.destroy()
        return command_buffer

    def clear_command_buffer():
        for i in range(len(command_buffer)):
            remove_from_buffer(0)

    def generate_objects_text():
        objects_text = ""
        
        for v in vessels:
            objects_text += "卫星: " + v.get_name() + "\n"

        for b in bodies:
            objects_text += "中心天体: " + b.get_name() + "\n"
            
        for sp in surface_points:
            objects_text += "探测区域: " + sp.get_name() + "\n"

        for bc in barycenters:
            objects_text += "引力中心: " + bc.get_name() + "\n"

        for m in maneuvers:
            objects_text += "加速器: " + m.get_name() + "\n"

        for rp in radiation_pressures:
            objects_text += "辐射压力: " + rp.get_name() + "\n"

        for ad in atmospheric_drags:
            objects_text += "大气阻力: " + ad.get_name() + "\n"
            
        for p in projections:
            objects_text += "PROJECTION: " + p.get_name() + "\n"
            
        for pl in plots:
            objects_text += "PLOTTER: " + pl.get_name() + "\n"
            
        return objects_text

    def set_objects_text():
        objects_panel.config(state="normal")
        obj_text = generate_objects_text()
        objects_panel.delete(1.0, "end")
        objects_panel.insert(1.0, obj_text)
        objects_panel.config(state="disabled")

    def set_buffer_field():
        cbx.config(state="normal")
        cb_out = ""
        for i in range(len(command_buffer)):
            cb_out += str(i) + ": " + command_buffer[i] + "\n"

        cbx.delete(1.0, "end")
        cbx.insert(1.0, cb_out)
        cbx.config(state="disabled")

    def set_vars_field():
        sim_variables_field.config(state="normal")
        vars_text = "同步时间: " + str(sim_time) + "\n"
        vars_text += "时间间隔: " + str(delta_t) + "\n"
        vars_text += "周期: " + str(cycle_time) + "\n"
        vars_text += "仿真帧率: " + str(output_rate) + "\n"
        vars_text += "\n观察角度平移速度: " + str(cam_strafe_speed) + "\n"
        vars_text += "观察角度旋转速度: " + str(cam_rotate_speed) + "\n"
        if scene_lock:
            vars_text += "锁定设置: " + str(scene_lock.get_name()) + "\n"
        else:
            vars_text += "锁定设置: None\n"
        sim_variables_field.delete(1.0, "end")
        sim_variables_field.insert(1.0, vars_text)
        sim_variables_field.config(state="disabled")

    def add_to_buffer(command):
        command_buffer.append(command)
        set_buffer_field()

    def remove_from_buffer(cmd_index):
        if len(command_buffer):
            cmd_index = int(cmd_index)

            cmd_index = min(cmd_index, len(command_buffer)-1)
            command_buffer.remove(command_buffer[cmd_index])
            set_buffer_field()

    def use_command_delete_window():

        if len(command_buffer):

            deletion_window = tk.Tk()
            deletion_window.title("撤销指令")

            deletion_label = tk.Label(deletion_window, text="键入要从缓冲区中撤销指令的索引号.")
            deletion_label.grid(row=0, column=0, columnspan=10)

            deletion_input = tk.Text(deletion_window, width=20, height=1)
            deletion_input.grid(row=1, column=4)

            deletion_button = tk.Button(deletion_window, text="撤销", command=lambda:remove_from_buffer(deletion_input.get("1.0","end-1c")))
            deletion_button.grid(row=2, column=4)

    def use_command_window():

        def on_command_window_close():
            cmd_window.destroy()

        def enter_cmd(cmd_a):
            entry_panel = tk.Tk()
            entry_panel.title(cmd_a)

            # SHOW COMMAND
            if cmd_a == "show":
                show_help = tk.Label(entry_panel, text="'输出'命令将一个输出元素添加到命令提示符/终端.")
                show_help.grid(row=0, column=0, columnspan=10)
                # option 1
                show_traj_button = tk.Button(entry_panel, text="输出轨道", command=lambda:add_to_buffer("show traj"))
                show_traj_button.grid(row=1, column=0)
                show_traj_button.config(width=20,height=1)

                # option 2
                show_s1t1_label = tk.Label(entry_panel, text="对象")
                show_s1t2_label = tk.Label(entry_panel, text="变量")
                show_s1t3_label = tk.Label(entry_panel, text="标签")
                show_s1t1_label.grid(row=2, column=1)
                show_s1t2_label.grid(row=2, column=2)
                show_s1t3_label.grid(row=2, column=3)
                
                show_s1t1 = tk.Text(entry_panel, width=20, height=1)
                show_s1t2 = tk.Text(entry_panel, width=20, height=1)
                show_s1t3 = tk.Text(entry_panel, width=20, height=1)
                show_s1t1.grid(row=3, column=1)
                show_s1t2.grid(row=3, column=2)
                show_s1t3.grid(row=3, column=3)

                def generate_s1():
                    if show_s1t1.get("1.0","end-1c") and show_s1t2.get("1.0","end-1c") and show_s1t3.get("1.0","end-1c"):
                        command = "show " + show_s1t1.get("1.0","end-1c") + " " + show_s1t2.get("1.0","end-1c") + " " + show_s1t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s1_button = tk.Button(entry_panel, text="输出全局变量", command=generate_s1)
                show_s1_button.grid(row=3, column=0)
                show_s1_button.config(width=20,height=1)

                # option 3
                show_s2t1_label = tk.Label(entry_panel, text="对象")
                show_s2t2_label = tk.Label(entry_panel, text= "变量")
                show_s2t3_label = tk.Label(entry_panel, text="引用帧")
                show_s2t4_label = tk.Label(entry_panel, text="标签")
                show_s2t1_label.grid(row=4, column=1)
                show_s2t2_label.grid(row=4, column=2)
                show_s2t3_label.grid(row=4, column=3)
                show_s2t4_label.grid(row=4, column=4)

                show_s2t1 = tk.Text(entry_panel, width=20, height=1)
                show_s2t2 = tk.Text(entry_panel, width=20, height=1)
                show_s2t3 = tk.Text(entry_panel, width=20, height=1)
                show_s2t4 = tk.Text(entry_panel, width=20, height=1)
                show_s2t1.grid(row=5, column=1)
                show_s2t2.grid(row=5, column=2)
                show_s2t3.grid(row=5, column=3)
                show_s2t4.grid(row=5, column=4)

                def generate_s2():
                    if show_s2t1.get("1.0","end-1c") and show_s2t2.get("1.0","end-1c") and show_s2t3.get("1.0","end-1c") and show_s2t4.get("1.0","end-1c"):
                        command = "show " + show_s2t1.get("1.0","end-1c") + " " + show_s2t2.get("1.0","end-1c") + " " + show_s2t3.get("1.0","end-1c") + " " + show_s2t4.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s2_button = tk.Button(entry_panel, text="输出关联变量", command=generate_s2)
                show_s2_button.grid(row=5, column=0)
                show_s2_button.config(width=20,height=1)

                # option 4
                show_s3t1_label = tk.Label(entry_panel, text="加速器")
                show_s3t2_label = tk.Label(entry_panel, text="数据 ('活动'/'状态'/'参数')")
                show_s3t3_label = tk.Label(entry_panel, text="标签")
                show_s3t1_label.grid(row=6, column=1)
                show_s3t2_label.grid(row=6, column=2)
                show_s3t3_label.grid(row=6, column=3)

                show_s3t1 = tk.Text(entry_panel, width=20, height=1)
                show_s3t2 = tk.Text(entry_panel, width=20, height=1)
                show_s3t3 = tk.Text(entry_panel, width=20, height=1)
                show_s3t1.grid(row=7, column=1)
                show_s3t2.grid(row=7, column=2)
                show_s3t3.grid(row=7, column=3)

                def generate_s3():
                    if show_s3t1.get("1.0","end-1c") and show_s3t2.get("1.0","end-1c") and show_s3t3.get("1.0","end-1c"):
                        command = "show " + show_s3t1.get("1.0","end-1c") + " " + show_s3t2.get("1.0","end-1c") + " " + show_s3t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s3_button = tk.Button(entry_panel, text="输出加速器数据", command=generate_s3)
                show_s3_button.grid(row=7, column=0)
                show_s3_button.config(width=20,height=1)

                # option 5
                show_s4t1_label = tk.Label(entry_panel, text="辐射压力")
                show_s4t2_label = tk.Label(entry_panel, text="数据 ('参数')")
                show_s4t3_label = tk.Label(entry_panel, text="显示标签")
                show_s4t1_label.grid(row=8, column=1)
                show_s4t2_label.grid(row=8, column=2)
                show_s4t3_label.grid(row=8, column=3)

                show_s4t1 = tk.Text(entry_panel, width=20, height=1)
                show_s4t2 = tk.Text(entry_panel, width=20, height=1)
                show_s4t3 = tk.Text(entry_panel, width=20, height=1)
                show_s4t1.grid(row=9, column=1)
                show_s4t2.grid(row=9, column=2)
                show_s4t3.grid(row=9, column=3)

                def generate_s4():
                    if show_s4t1.get("1.0","end-1c") and show_s4t2.get("1.0","end-1c") and show_s4t3.get("1.0","end-1c"):
                        command = "show " + show_s4t1.get("1.0","end-1c") + " " + show_s4t2.get("1.0","end-1c") + " " + show_s4t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s4_button = tk.Button(entry_panel, text="输出辐射压力数据", command=generate_s4)
                show_s4_button.grid(row=9, column=0)
                show_s4_button.config(width=20,height=1)

                # option 6
                show_s5t1_label = tk.Label(entry_panel, text="大气阻力")
                show_s5t2_label = tk.Label(entry_panel, text="数据 ('参数')")
                show_s5t3_label = tk.Label(entry_panel, text="显示标签")
                show_s5t1_label.grid(row=10, column=1)
                show_s5t2_label.grid(row=10, column=2)
                show_s5t3_label.grid(row=10, column=3)

                show_s5t1 = tk.Text(entry_panel, width=20, height=1)
                show_s5t2 = tk.Text(entry_panel, width=20, height=1)
                show_s5t3 = tk.Text(entry_panel, width=20, height=1)
                show_s5t1.grid(row=11, column=1)
                show_s5t2.grid(row=11, column=2)
                show_s5t3.grid(row=11, column=3)

                def generate_s5():
                    if show_s5t1.get("1.0","end-1c") and show_s5t2.get("1.0","end-1c") and show_s5t3.get("1.0","end-1c"):
                        command = "show " + show_s5t1.get("1.0","end-1c") + " " + show_s5t2.get("1.0","end-1c") + " " + show_s5t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s5_button = tk.Button(entry_panel, text="输出大气阻力数据", command=generate_s5)
                show_s5_button.grid(row=11, column=0)
                show_s5_button.config(width=20,height=1)

                # option 7
                show_s6t1_label = tk.Label(entry_panel, text="投影")
                show_s6t2_label = tk.Label(entry_panel, text="数据 (属性/'参数')")
                show_s6t3_label = tk.Label(entry_panel, text="显示标签")
                show_s6t1_label.grid(row=12, column=1)
                show_s6t2_label.grid(row=12, column=2)
                show_s6t3_label.grid(row=12, column=3)

                show_s6t1 = tk.Text(entry_panel, width=20, height=1)
                show_s6t2 = tk.Text(entry_panel, width=20, height=1)
                show_s6t3 = tk.Text(entry_panel, width=20, height=1)
                show_s6t1.grid(row=13, column=1)
                show_s6t2.grid(row=13, column=2)
                show_s6t3.grid(row=13, column=3)

                def generate_s6():
                    if show_s6t1.get("1.0","end-1c") and show_s6t2.get("1.0","end-1c") and show_s6t3.get("1.0","end-1c"):
                        command = "show " + show_s6t1.get("1.0","end-1c") + " " + show_s6t2.get("1.0","end-1c") + " " + show_s6t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s6_button = tk.Button(entry_panel, text="输出投影数据", command=generate_s6)
                show_s6_button.grid(row=13, column=0)
                show_s6_button.config(width=20,height=1)

                # option 7
                show_labels_button = tk.Button(entry_panel, text="输出标签", command=lambda:add_to_buffer("show labels"))
                show_labels_button.grid(row=14, column=0)
                show_labels_button.config(width=20,height=1)

            elif cmd_a == "hide":
                hide_help = tk.Label(entry_panel, text="'删除' 命令从命令提示符/终端删除一个输出元素.")
                hide_help.grid(row=0, column=0, columnspan=10)
                
                hide_s1_button = tk.Button(entry_panel, text="删除轨道", command=lambda:add_to_buffer("hide traj"))
                hide_s1_button.grid(row=1, column=0)
                hide_s1_button.config(width=20,height=1)

                hide_s2t1_label = tk.Label(entry_panel, text="显示标签")
                hide_s2t1_label.grid(row=2, column=1)

                hide_s2t1 = tk.Text(entry_panel, width=20, height=1)
                hide_s2t1.grid(row=3, column=1)

                def generate_s2():
                    if hide_s2t1.get("1.0","end-1c"):
                        command = "hide " + hide_s2t1.get("1.0","end-1c")
                        add_to_buffer(command)

                hide_s2_button = tk.Button(entry_panel, text="删除输出", command=generate_s2)
                hide_s2_button.grid(row=3, column=0)
                hide_s2_button.config(width=20,height=1)

                hide_s3_button = tk.Button(entry_panel, text="删除标签", command=lambda:add_to_buffer("hide labels"))
                hide_s3_button.grid(row=4, column=0)
                hide_s3_button.config(width=20,height=1)

            elif cmd_a == "clear":
                clear_help = tk.Label(entry_panel, text="'清空' 命令可以从命令提示符/终端中删除所有输出元素，\n从仿真环境中删除所有对象，或者清除直到当前模拟时间的轨迹.")
                clear_help.grid(row=0, column=0, columnspan=10)
                
                clear_s1_button = tk.Button(entry_panel, text="清空输出", command=lambda:add_to_buffer("clear output"))
                clear_s2_button = tk.Button(entry_panel, text="清空对象", command=lambda:add_to_buffer("clear scene"))
                clear_s3_button = tk.Button(entry_panel, text="清空轨迹", command=lambda:add_to_buffer("clear traj_visuals"))
                clear_s1_button.grid(row=1, column=0)
                clear_s2_button.grid(row=2, column=0)
                clear_s3_button.grid(row=3, column=0)
            
            elif cmd_a == "create_vessel":
                cv_help = tk.Label(entry_panel, text="'创建卫星' 命令在仿真环境中添加了一颗新卫星.")
                cv_help.grid(row=0, column=0, columnspan=10)
                # option 1
                cv_s1t1_label = tk.Label(entry_panel, text="卫星ID")
                cv_s1t2_label = tk.Label(entry_panel, text="3D模型ID")
                cv_s1t3_label = tk.Label(entry_panel, text="颜色")
                cv_s1t4_label = tk.Label(entry_panel, text="空间坐标")
                cv_s1t5_label = tk.Label(entry_panel, text="速度向量")
                cv_s1t1_label.grid(row=1, column=1)
                cv_s1t2_label.grid(row=1, column=2)
                cv_s1t3_label.grid(row=1, column=3)
                cv_s1t4_label.grid(row=1, column=4)
                cv_s1t5_label.grid(row=1, column=5)
                
                cv_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t2 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t3 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t4 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t5 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t1.grid(row=2, column=1)
                cv_s1t2.grid(row=2, column=2)
                cv_s1t3.grid(row=2, column=3)
                cv_s1t4.grid(row=2, column=4)
                cv_s1t5.grid(row=2, column=5)

                def generate_s1():
                    if cv_s1t1.get("1.0","end-1c") and cv_s1t2.get("1.0","end-1c") and cv_s1t3.get("1.0","end-1c") and cv_s1t4.get("1.0","end-1c") and cv_s1t5.get("1.0","end-1c"):
                        command = "create_vessel " + cv_s1t1.get("1.0","end-1c") + " " + cv_s1t2.get("1.0","end-1c") + " " + cv_s1t3.get("1.0","end-1c") + " " + cv_s1t4.get("1.0","end-1c") + " " + cv_s1t5.get("1.0","end-1c")
                        add_to_buffer(command)

                cv_s1_button = tk.Button(entry_panel, text="创建卫星", command=generate_s1)
                cv_s1_button.grid(row=2, column=0)

                # option 2
                cv_s2t1_label = tk.Label(entry_panel, text="卫星ID")
                cv_s2t2_label = tk.Label(entry_panel, text="3D模型ID")
                cv_s2t3_label = tk.Label(entry_panel, text="颜色")
                cv_s2t4_label = tk.Label(entry_panel, text="引用帧")
                cv_s2t5_label = tk.Label(entry_panel, text="球面坐标")
                cv_s2t6_label = tk.Label(entry_panel, text="速度向量")
                cv_s2t1_label.grid(row=3, column=1)
                cv_s2t2_label.grid(row=3, column=2)
                cv_s2t3_label.grid(row=3, column=3)
                cv_s2t4_label.grid(row=3, column=4)
                cv_s2t5_label.grid(row=3, column=5)
                cv_s2t6_label.grid(row=3, column=6)

                cv_s2t1 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t2 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t3 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t4 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t5 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t6 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t1.grid(row=4, column=1)
                cv_s2t2.grid(row=4, column=2)
                cv_s2t3.grid(row=4, column=3)
                cv_s2t4.grid(row=4, column=4)
                cv_s2t5.grid(row=4, column=5)
                cv_s2t6.grid(row=4, column=6)

                def generate_s2():
                    if cv_s2t1.get("1.0","end-1c") and cv_s2t2.get("1.0","end-1c") and cv_s2t3.get("1.0","end-1c") and cv_s2t4.get("1.0","end-1c") and cv_s2t5.get("1.0","end-1c") and cv_s2t6.get("1.0","end-1c") :
                        command = "create_vessel " + cv_s2t1.get("1.0","end-1c") + " " + cv_s2t2.get("1.0","end-1c") + " " + cv_s2t3.get("1.0","end-1c") + " " + cv_s2t4.get("1.0","end-1c") + " " + cv_s2t5.get("1.0","end-1c") + " " + cv_s2t5.get("1.0","end-1c")
                        add_to_buffer(command)

                cv_s2_button = tk.Button(entry_panel, text="创建卫星", command=generate_s1)
                cv_s2_button.grid(row=4, column=0)

            elif cmd_a == "delete_vessel":
                dv_help = tk.Label(entry_panel, text="'删除卫星' 命令从仿真环境中删除一颗卫星.")
                dv_help.grid(row=0, column=0, columnspan=10)
                
                dv_s1t1_label = tk.Label(entry_panel, text="卫星ID")
                dv_s1t1_label.grid(row=1, column=1)

                dv_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dv_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dv_s1t1.get("1.0","end-1c"):
                        command = "delete_vessel " + dv_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dv_s1_button = tk.Button(entry_panel, text="删除卫星", command=generate_s1)
                dv_s1_button.grid(row=2, column=0)

            elif cmd_a == "fragment":
                frag_help = tk.Label(entry_panel, text="'解体' 命令在仿真环境中模拟卫星解体产生碎片\n.")
                frag_help.grid(row=0, column=0, columnspan=10)

                frag_s1t1_label = tk.Label(entry_panel, text="碎片ID")
                frag_s1t1_label.grid(row=1, column=1)
                frag_s1t2_label = tk.Label(entry_panel, text="碎片数量")
                frag_s1t2_label.grid(row=1, column=2)
                frag_s1t3_label = tk.Label(entry_panel, text="解体卫星ID")
                frag_s1t3_label.grid(row=1, column=3)

                frag_s1t1 = tk.Text(entry_panel, width=20, height=1)
                frag_s1t1.grid(row=2, column=1)
                frag_s1t2 = tk.Text(entry_panel, width=20, height=1)
                frag_s1t2.grid(row=2, column=2)
                frag_s1t3 = tk.Text(entry_panel, width=20, height=1)
                frag_s1t3.grid(row=2, column=3)

                def generate_s1():
                    if frag_s1t1.get("1.0","end-1c") and frag_s1t2.get("1.0","end-1c") and frag_s1t3.get("1.0","end-1c"):
                        command = "fragment " + frag_s1t1.get("1.0","end-1c") + " " + frag_s1t2.get("1.0","end-1c") + " " + frag_s1t3.get("1.0","end-1c")
                        add_to_buffer(command)

                frag_s1_button = tk.Button(entry_panel, text="解体", command=generate_s1)
                frag_s1_button.grid(row=2, column=0)

                # s2 ---
                frag_s2t1_label = tk.Label(entry_panel, text="碎片ID")
                frag_s2t1_label.grid(row=3, column=1)
                frag_s2t2_label = tk.Label(entry_panel, text="碎片数量")
                frag_s2t2_label.grid(row=3, column=2)

                frag_s2t1 = tk.Text(entry_panel, width=20, height=1)
                frag_s2t1.grid(row=4, column=1)
                frag_s2t2 = tk.Text(entry_panel, width=20, height=1)
                frag_s2t2.grid(row=4, column=2)

                def generate_s2():
                    if frag_s2t1.get("1.0","end-1c") and frag_s2t2.get("1.0","end-1c"):
                        command = "fragment " + frag_s2t1.get("1.0","end-1c") + " " + frag_s2t2.get("1.0","end-1c")
                        add_to_buffer(command)

                frag_s2_button = tk.Button(entry_panel, text="解体", command=generate_s2)
                frag_s2_button.grid(row=4, column=0)

                # s3 ---
                frag_s3t1_label = tk.Label(entry_panel, text="碎片ID")
                frag_s3t1_label.grid(row=5, column=1)

                frag_s3t1 = tk.Text(entry_panel, width=20, height=1)
                frag_s3t1.grid(row=6, column=1)

                def generate_s3():
                    if frag_s3t1.get("1.0","end-1c"):
                        command = "fragment " + frag_s3t1.get("1.0","end-1c")
                        add_to_buffer(command)

                frag_s3_button = tk.Button(entry_panel, text="解体", command=generate_s3)
                frag_s3_button.grid(row=6, column=0)

            elif cmd_a == "create_maneuver":
                cm_help = tk.Label(entry_panel, text="'创建加速器' 命令对指定卫星添加动力装置.")
                cm_help.grid(row=0, column=0, columnspan=10)
                
                # option 1
                cm_s1t1_label = tk.Label(entry_panel, text="加速器ID")
                cm_s1t2_label = tk.Label(entry_panel, text="卫星ID")
                cm_s1t3_label = tk.Label(entry_panel, text="引用帧")
                cm_s1t4_label = tk.Label(entry_panel, text="方向")
                cm_s1t5_label = tk.Label(entry_panel, text="加速度")
                cm_s1t6_label = tk.Label(entry_panel, text="开始时间")
                cm_s1t7_label = tk.Label(entry_panel, text="持续时间")
                cm_s1t1_label.grid(row=1, column=1)
                cm_s1t2_label.grid(row=1, column=2)
                cm_s1t3_label.grid(row=1, column=3)
                cm_s1t4_label.grid(row=1, column=4)
                cm_s1t5_label.grid(row=1, column=5)
                cm_s1t6_label.grid(row=1, column=6)
                cm_s1t7_label.grid(row=1, column=7)

                cm_s1t1 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t2 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t3 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t4 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t5 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t6 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t7 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t1.grid(row=2, column=1)
                cm_s1t2.grid(row=2, column=2)
                cm_s1t3.grid(row=2, column=3)
                cm_s1t4.grid(row=2, column=4)
                cm_s1t5.grid(row=2, column=5)
                cm_s1t6.grid(row=2, column=6)
                cm_s1t7.grid(row=2, column=7)

                def generate_s1():
                    if cm_s1t1.get("1.0","end-1c") and cm_s1t2.get("1.0","end-1c") and cm_s1t3.get("1.0","end-1c") and cm_s1t4.get("1.0","end-1c") and cm_s1t5.get("1.0","end-1c") and cm_s1t6.get("1.0","end-1c") and cm_s1t7.get("1.0","end-1c"):
                        command = "create_maneuver " + cm_s1t1.get("1.0","end-1c") + " const_accel " + cm_s1t2.get("1.0","end-1c") + " " + cm_s1t3.get("1.0","end-1c") + " " + cm_s1t4.get("1.0","end-1c") + " " + cm_s1t5.get("1.0","end-1c") + " " + cm_s1t6.get("1.0","end-1c") + " " + cm_s1t7.get("1.0","end-1c")
                        add_to_buffer(command)

                cm_s1_button = tk.Button(entry_panel, text="创建恒定加速度加速器", command=generate_s1)
                cm_s1_button.grid(row=2, column=0)

                # option 2
                cm_s2t1_label = tk.Label(entry_panel, text="加速器ID")
                cm_s2t2_label = tk.Label(entry_panel, text="卫星ID")
                cm_s2t3_label = tk.Label(entry_panel, text="引用帧")
                cm_s2t4_label = tk.Label(entry_panel, text="方向")
                cm_s2t5_label = tk.Label(entry_panel, text="推力")
                cm_s2t6_label = tk.Label(entry_panel, text="初始质量")
                cm_s2t7_label = tk.Label(entry_panel, text="质量流量")
                cm_s2t8_label = tk.Label(entry_panel, text="开始时间")
                cm_s2t9_label = tk.Label(entry_panel, text="持续时间")
                cm_s2t1_label.grid(row=3, column=1)
                cm_s2t2_label.grid(row=3, column=2)
                cm_s2t3_label.grid(row=3, column=3)
                cm_s2t4_label.grid(row=3, column=4)
                cm_s2t5_label.grid(row=3, column=5)
                cm_s2t6_label.grid(row=3, column=6)
                cm_s2t7_label.grid(row=3, column=7)
                cm_s2t8_label.grid(row=3, column=8)
                cm_s2t9_label.grid(row=3, column=9)

                cm_s2t1 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t2 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t3 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t4 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t5 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t6 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t7 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t8 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t9 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t1.grid(row=4, column=1)
                cm_s2t2.grid(row=4, column=2)
                cm_s2t3.grid(row=4, column=3)
                cm_s2t4.grid(row=4, column=4)
                cm_s2t5.grid(row=4, column=5)
                cm_s2t6.grid(row=4, column=6)
                cm_s2t7.grid(row=4, column=7)
                cm_s2t8.grid(row=4, column=8)
                cm_s2t9.grid(row=4, column=9)

                def generate_s2():
                    if cm_s2t1.get("1.0","end-1c") and cm_s2t2.get("1.0","end-1c") and cm_s2t3.get("1.0","end-1c") and cm_s2t4.get("1.0","end-1c") and cm_s2t5.get("1.0","end-1c") and cm_s2t6.get("1.0","end-1c") and cm_s2t7.get("1.0","end-1c") and cm_s2t8.get("1.0","end-1c") and cm_s2t9.get("1.0","end-1c"):
                        command = "create_maneuver " + cm_s2t1.get("1.0","end-1c") + " const_thrust " + cm_s2t2.get("1.0","end-1c") + " " + cm_s2t3.get("1.0","end-1c") + " " + cm_s2t4.get("1.0","end-1c") + " " + cm_s2t5.get("1.0","end-1c") + " " + cm_s2t6.get("1.0","end-1c") + " " + cm_s2t7.get("1.0","end-1c") + " " + cm_s2t8.get("1.0","end-1c") + " " + cm_s2t9.get("1.0","end-1c")
                        add_to_buffer(command)

                cm_s2_button = tk.Button(entry_panel, text="创建恒定推力加速器", command=generate_s2)
                cm_s2_button.grid(row=4, column=0)

                # option 3
                cm_s3t1_label = tk.Label(entry_panel, text="加速器ID")
                cm_s3t2_label = tk.Label(entry_panel, text="卫星ID")
                cm_s3t3_label = tk.Label(entry_panel, text="引用帧")
                cm_s3t4_label = tk.Label(entry_panel, text="方向")
                cm_s3t5_label = tk.Label(entry_panel, text="速度变化量")
                cm_s3t6_label = tk.Label(entry_panel, text="执行时间")
                cm_s3t1_label.grid(row=5, column=1)
                cm_s3t2_label.grid(row=5, column=2)
                cm_s3t3_label.grid(row=5, column=3)
                cm_s3t4_label.grid(row=5, column=4)
                cm_s3t5_label.grid(row=5, column=5)
                cm_s3t6_label.grid(row=5, column=6)

                cm_s3t1 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t2 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t3 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t4 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t5 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t6 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t1.grid(row=6, column=1)
                cm_s3t2.grid(row=6, column=2)
                cm_s3t3.grid(row=6, column=3)
                cm_s3t4.grid(row=6, column=4)
                cm_s3t5.grid(row=6, column=5)
                cm_s3t6.grid(row=6, column=6)

                def generate_s3():
                    if cm_s3t1.get("1.0","end-1c") and cm_s3t2.get("1.0","end-1c") and cm_s3t3.get("1.0","end-1c") and cm_s3t4.get("1.0","end-1c") and cm_s3t5.get("1.0","end-1c") and cm_s3t6.get("1.0","end-1c"):
                        command = "create_maneuver " + cm_s3t1.get("1.0", "end-1c") + " impulsive " + cm_s3t2.get("1.0","end-1c") + " " + cm_s3t3.get("1.0","end-1c") + " " + cm_s3t4.get("1.0","end-1c") + " " + cm_s3t5.get("1.0","end-1c") + " " + cm_s3t6.get("1.0","end-1c")
                        add_to_buffer(command)

                cm_s3_button = tk.Button(entry_panel, text="创建冲量加速器.", command=generate_s3)
                cm_s3_button.grid(row=6, column=0)
                
            elif cmd_a == "delete_maneuver":
                dm_help = tk.Label(entry_panel, text="'删除加速器' 命令从仿真环境中移除加速器.")
                dm_help.grid(row=0, column=0, columnspan=10)
                
                dm_s1t1_label = tk.Label(entry_panel, text="加速器ID")
                dm_s1t1_label.grid(row=1, column=1)

                dm_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dm_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dm_s1t1.get("1.0","end-1c"):
                        command = "delete_maneuver " + dm_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dm_s1_button = tk.Button(entry_panel, text="删除加速器", command=generate_s1)
                dm_s1_button.grid(row=2, column=0)

            elif cmd_a == "apply_radiation_pressure":
                arp_help = tk.Label(entry_panel, text="'施加辐射压力' 命令在仿真环境中对卫星设置辐射压力效应.")
                arp_help.grid(row=0, column=0, columnspan=10)

                arp_s1t1_label = tk.Label(entry_panel, text="辐射压力ID")
                arp_s1t2_label = tk.Label(entry_panel, text="卫星ID")
                arp_s1t3_label = tk.Label(entry_panel, text="辐射天体ID")
                arp_s1t4_label = tk.Label(entry_panel, text="辐射面积")
                arp_s1t5_label = tk.Label(entry_panel, text="辐射天体自转方向")
                arp_s1t6_label = tk.Label(entry_panel, text="作用方向")
                arp_s1t7_label = tk.Label(entry_panel, text="卫星质量")
                arp_s1t8_label = tk.Label(entry_panel, text="自动更新质量(0/1)")
                arp_s1t1_label.grid(row=1, column=1)
                arp_s1t2_label.grid(row=1, column=2)
                arp_s1t3_label.grid(row=1, column=3)
                arp_s1t4_label.grid(row=1, column=4)
                arp_s1t5_label.grid(row=1, column=5)
                arp_s1t6_label.grid(row=1, column=6)
                arp_s1t7_label.grid(row=1, column=7)
                arp_s1t8_label.grid(row=1, column=8)

                arp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t2 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t3 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t4 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t5 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t6 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t7 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t8 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t1.grid(row=2, column=1)
                arp_s1t2.grid(row=2, column=2)
                arp_s1t3.grid(row=2, column=3)
                arp_s1t4.grid(row=2, column=4)
                arp_s1t5.grid(row=2, column=5)
                arp_s1t6.grid(row=2, column=6)
                arp_s1t7.grid(row=2, column=7)
                arp_s1t8.grid(row=2, column=8)

                def generate_s1():
                    if (arp_s1t1.get("1.0", "end-1c") and arp_s1t2.get("1.0", "end-1c") and arp_s1t3.get("1.0", "end-1c") and arp_s1t4.get("1.0", "end-1c") and
                        arp_s1t5.get("1.0", "end-1c") and arp_s1t6.get("1.0", "end-1c") and arp_s1t7.get("1.0", "end-1c") and arp_s1t8.get("1.0", "end-1c")):
                        command = "apply_radiation_pressure " + arp_s1t1.get("1.0", "end-1c") + " " + arp_s1t2.get("1.0", "end-1c") + " " + arp_s1t3.get("1.0", "end-1c") + " " + arp_s1t4.get("1.0", "end-1c") + " " + arp_s1t5.get("1.0", "end-1c") + " " + arp_s1t6.get("1.0", "end-1c") + " " + arp_s1t7.get("1.0", "end-1c") + " " + arp_s1t8.get("1.0", "end-1c")
                        add_to_buffer(command)

                arp_s1_button = tk.Button(entry_panel, text="施加辐射压力", command=generate_s1)
                arp_s1_button.grid(row=2, column=0)

            elif cmd_a == "remove_radiation_pressure":
                rrp_help = tk.Label(entry_panel, text="'移除辐射压力' 命令在仿真环境中移除辐射压力效应.")
                rrp_help.grid(row=0, column=0, columnspan=10)
                
                rrp_s1t1_label = tk.Label(entry_panel, text="辐射压力ID")
                rrp_s1t1_label.grid(row=1, column=1)

                rrp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                rrp_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if rrp_s1t1.get("1.0","end-1c"):
                        command = "remove_radiation_pressure " + rrp_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                rrp_s1_button = tk.Button(entry_panel, text="移除辐射压力", command=generate_s1)
                rrp_s1_button.grid(row=2, column=0)

            elif cmd_a == "apply_atmospheric_drag":
                aad_help = tk.Label(entry_panel, text="'施加大气阻力' 命令在仿真环境中对卫星设置大气阻力效应.")
                aad_help.grid(row=0, column=0, columnspan=10)

                aad_s1t1_label = tk.Label(entry_panel, text="大气阻力ID")
                aad_s1t2_label = tk.Label(entry_panel, text="卫星ID")
                aad_s1t3_label = tk.Label(entry_panel, text="天体ID")
                aad_s1t4_label = tk.Label(entry_panel, text="压力面积")
                aad_s1t5_label = tk.Label(entry_panel, text="压力系数")
                aad_s1t6_label = tk.Label(entry_panel, text="卫星质量")
                aad_s1t7_label = tk.Label(entry_panel, text="自动更新质量(0/1)")
                aad_s1t1_label.grid(row=1, column=1)
                aad_s1t2_label.grid(row=1, column=2)
                aad_s1t3_label.grid(row=1, column=3)
                aad_s1t4_label.grid(row=1, column=4)
                aad_s1t5_label.grid(row=1, column=5)
                aad_s1t6_label.grid(row=1, column=6)
                aad_s1t7_label.grid(row=1, column=7)

                aad_s1t1 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t2 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t3 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t4 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t5 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t6 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t7 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t1.grid(row=2, column=1)
                aad_s1t2.grid(row=2, column=2)
                aad_s1t3.grid(row=2, column=3)
                aad_s1t4.grid(row=2, column=4)
                aad_s1t5.grid(row=2, column=5)
                aad_s1t6.grid(row=2, column=6)
                aad_s1t7.grid(row=2, column=7)
                
                def generate_s1():
                    if (aad_s1t1.get("1.0", "end-1c") and aad_s1t2.get("1.0", "end-1c") and aad_s1t3.get("1.0", "end-1c") and aad_s1t4.get("1.0", "end-1c") and
                        aad_s1t5.get("1.0", "end-1c") and aad_s1t6.get("1.0", "end-1c") and aad_s1t7.get("1.0", "end-1c")):
                        command = "apply_atmospheric_drag " + aad_s1t1.get("1.0", "end-1c") + " " + aad_s1t2.get("1.0", "end-1c") + " " + aad_s1t3.get("1.0", "end-1c") + " " + aad_s1t4.get("1.0", "end-1c") + " " + aad_s1t5.get("1.0", "end-1c") + " " + aad_s1t6.get("1.0", "end-1c") + " " + aad_s1t7.get("1.0", "end-1c")
                        add_to_buffer(command)

                aad_s1_button = tk.Button(entry_panel, text="施加大气阻力", command=generate_s1)
                aad_s1_button.grid(row=2, column=0)

            elif cmd_a == "remove_atmospheric_drag":
                rad_help = tk.Label(entry_panel, text="'移除大气阻力' 命令在仿真环境中移除指定大气阻力效应.")
                rad_help.grid(row=0, column=0, columnspan=10)
                
                rad_s1t1_label = tk.Label(entry_panel, text="大气阻力ID")
                rad_s1t1_label.grid(row=1, column=1)

                rad_s1t1 = tk.Text(entry_panel, width=20, height=1)
                rad_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if rad_s1t1.get("1.0","end-1c"):
                        command = "remove_atmospheric_drag " + rad_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                rad_s1_button = tk.Button(entry_panel, text="移除大气阻力", command=generate_s1)
                rad_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_projection":
                cp_help = tk.Label(entry_panel, text="'创建投影' 命令在仿真环境中创建二体开普勒轨道投影.")
                cp_help.grid(row=0, column=0, columnspan=10)
                
                cp_s1t1_label = tk.Label(entry_panel, text="投影ID")
                cp_s1t2_label = tk.Label(entry_panel, text="卫星ID")
                cp_s1t3_label = tk.Label(entry_panel, text="中央天体ID")
                cp_s1t1_label.grid(row=1, column=1)
                cp_s1t2_label.grid(row=1, column=2)
                cp_s1t3_label.grid(row=1, column=3)

                cp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cp_s1t2 = tk.Text(entry_panel, width=20, height=1)
                cp_s1t3 = tk.Text(entry_panel, width=20, height=1)
                cp_s1t1.grid(row=2, column=1)
                cp_s1t2.grid(row=2, column=2)
                cp_s1t3.grid(row=2, column=3)

                def generate_s1():
                    if cp_s1t1.get("1.0", "end-1c") and cp_s1t2.get("1.0", "end-1c") and cp_s1t2.get("1.0", "end-1c"):
                        command = "create_projection " + cp_s1t1.get("1.0", "end-1c") + " " + cp_s1t2.get("1.0", "end-1c") + " " + cp_s1t3.get("1.0", "end-1c")
                        add_to_buffer(command)

                cp_s1_button = tk.Button(entry_panel, text="创建投影", command=generate_s1)
                cp_s1_button.grid(row=2, column=0)
                
            elif cmd_a == "delete_projection":
                dp_help = tk.Label(entry_panel, text="'删除投影' 命令在仿真环境中移除指定开普勒轨道投影.")
                dp_help.grid(row=0, column=0, columnspan=10)
                
                dp_s1t1_label = tk.Label(entry_panel, text="投影ID")
                dp_s1t1_label.grid(row=1, column=1)

                dp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dp_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dp_s1t1.get("1.0", "end-1c"):
                        command = "delete_projection " + dp_s1t1.get("1.0", "end-1c")
                        add_to_buffer(command)

                dp_s1_button = tk.Button(entry_panel, text="删除投影", command=generate_s1)
                dp_s1_button.grid(row=2, column=0)

            elif cmd_a == "update_projection":
                up_help = tk.Label(entry_panel, text="'更新投影' 命令在仿真环境中更新当前投影.")
                up_help.grid(row=0, column=0, columnspan=10)

                up_s1t1_label = tk.Label(entry_panel, text="投影ID")
                up_s1t1_label.grid(row=1, column=1)

                up_s1t1 = tk.Text(entry_panel, width=20, height=1)
                up_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if up_s1t1.get("1.0", "end-1c"):
                        command = "update_projection " + up_s1t1.get("1.0", "end-1c")
                        add_to_buffer(command)

                up_s1_button = tk.Button(entry_panel, text="更新投影", command=generate_s1)
                up_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_plot":
                cpl_help = tk.Label(entry_panel, text="'创建绘图仪' 命令在仿真环境中添加绘图仪，以根据模拟时间绘制某些变量.")
                cpl_help.grid(row=0, column=0, columnspan=10)
                # option 1
                cpl_s1t1_label = tk.Label(entry_panel, text="绘图仪ID")
                cpl_s1t2_label = tk.Label(entry_panel, text="变量")
                cpl_s1t3_label = tk.Label(entry_panel, text="对象 1")
                cpl_s1t4_label = tk.Label(entry_panel, text="对象 2")
                cpl_s1t1_label.grid(row=1, column=1)
                cpl_s1t2_label.grid(row=1, column=2)
                cpl_s1t3_label.grid(row=1, column=3)
                cpl_s1t4_label.grid(row=1, column=4)

                cpl_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cpl_s1t2 = tk.Text(entry_panel, width=20, height=1)
                cpl_s1t3 = tk.Text(entry_panel, width=20, height=1)
                cpl_s1t4 = tk.Text(entry_panel, width=20, height=1)
                cpl_s1t1.grid(row=2, column=1)
                cpl_s1t2.grid(row=2, column=2)
                cpl_s1t3.grid(row=2, column=3)
                cpl_s1t4.grid(row=2, column=4)

                def generate_s1():
                    if cpl_s1t1.get("1.0","end-1c") and cpl_s1t2.get("1.0","end-1c") and cpl_s1t3.get("1.0","end-1c") and cpl_s1t4.get("1.0","end-1c"):
                        command = "create_plot " + cpl_s1t1.get("1.0","end-1c") + " " + cpl_s1t2.get("1.0","end-1c") + " " + cpl_s1t3.get("1.0","end-1c") + " " + cpl_s1t4.get("1.0","end-1c")
                        add_to_buffer(command)

                cpl_s1_button = tk.Button(entry_panel, text="创建绘图仪 (默认时间)", command=generate_s1)
                cpl_s1_button.grid(row=2, column=0)

                # option 2
                cpl_s2t1_label = tk.Label(entry_panel, text="绘图仪ID")
                cpl_s2t2_label = tk.Label(entry_panel, text="变量")
                cpl_s2t3_label = tk.Label(entry_panel, text="对象 1")
                cpl_s2t4_label = tk.Label(entry_panel, text="对象 2")
                cpl_s2t5_label = tk.Label(entry_panel, text="开始时间")
                cpl_s2t6_label = tk.Label(entry_panel, text="结束时间")
                cpl_s2t1_label.grid(row=3, column=1)
                cpl_s2t2_label.grid(row=3, column=2)
                cpl_s2t3_label.grid(row=3, column=3)
                cpl_s2t4_label.grid(row=3, column=4)
                cpl_s2t5_label.grid(row=3, column=5)
                cpl_s2t6_label.grid(row=3, column=6)

                cpl_s2t1 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t2 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t3 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t4 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t5 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t6 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t1.grid(row=4, column=1)
                cpl_s2t2.grid(row=4, column=2)
                cpl_s2t3.grid(row=4, column=3)
                cpl_s2t4.grid(row=4, column=4)
                cpl_s2t5.grid(row=4, column=5)
                cpl_s2t6.grid(row=4, column=6)

                def generate_s2():
                    if cpl_s2t1.get("1.0","end-1c") and cpl_s2t2.get("1.0","end-1c") and cpl_s2t3.get("1.0","end-1c") and cpl_s2t4.get("1.0","end-1c") and cpl_s2t5.get("1.0","end-1c") and cpl_s2t6.get("1.0","end-1c"):
                        command = "create_plot " + cpl_s2t1.get("1.0","end-1c") + " " + cpl_s2t2.get("1.0","end-1c") + " " + cpl_s2t3.get("1.0","end-1c") + " " + cpl_s2t4.get("1.0","end-1c") + " " + cpl_s2t5.get("1.0","end-1c") + " " + cpl_s2t6.get("1.0","end-1c")
                        add_to_buffer(command)

                cpl_s2_button = tk.Button(entry_panel, text="创建绘图仪", command=generate_s2)
                cpl_s2_button.grid(row=4, column=0)

            elif cmd_a == "delete_plot":
                dpl_help = tk.Label(entry_panel, text="'删除绘图仪' 命令在当前环境中删除绘图仪.")
                dpl_help.grid(row=0, column=0, columnspan=10)
                
                dpl_s1t1_label = tk.Label(entry_panel, text="绘图仪ID")
                dpl_s1t1_label.grid(row=1, column=1)

                dpl_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dpl_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dpl_s1t1.get("1.0","end-1c"):
                        command = "delete_plot " + dpl_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dpl_s1_button = tk.Button(entry_panel, text="删除绘图仪", command=generate_s1)
                dpl_s1_button.grid(row=2, column=0)

            elif cmd_a == "batch":
                bch_help = tk.Label(entry_panel, text="'批处理' 命令加载批处理文件，并将要发送给解释器的命令排成队列.")
                bch_help.grid(row=0, column=0, columnspan=10)
                
                bch_s1t1_label = tk.Label(entry_panel, text="批处理文件 (文件名 or 完整路径)")
                bch_s1t1_label.grid(row=1, column=1)

                bch_s1t1 = tk.Text(entry_panel, width=20, height=1)
                bch_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if bch_s1t1.get("1.0","end-1c"):
                        command = "batch " + bch_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                bch_s1_button = tk.Button(entry_panel, text="加载", command=generate_s1)
                bch_s1_button.grid(row=2, column=0)

            elif cmd_a == "export":
                exp_help = tk.Label(entry_panel, text="'导出' 命令将当前场景状态导出为OrbitSim3D场景(.osf)文件.")
                exp_help.grid(row=0, column=0, columnspan=10)

                exp_s1t1_label = tk.Label(entry_panel, text="文件名")
                exp_s1t1_label.grid(row=1, column=1)

                exp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                exp_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if exp_s1t1.get("1.0", "end-1c"):
                        command = "export " + exp_s1t1.get("1.0", "end-1c")
                        add_to_buffer(command)

                exp_s1_button = tk.Button(entry_panel, text="导出", command=generate_s1)
                exp_s1_button.grid(row=2, column=0)

            elif cmd_a == "cam_strafe_speed":
                css_help = tk.Label(entry_panel, text="'相机移动速度' 命令设置线性相机移动速度.")
                css_help.grid(row=0, column=0, columnspan=10)
                
                css_s1t1_label = tk.Label(entry_panel, text="速度")
                css_s1t1_label.grid(row=1, column=1)

                css_s1t1 = tk.Text(entry_panel, width=20, height=1)
                css_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if css_s1t1.get("1.0","end-1c"):
                        command = "cam_strafe_speed " + css_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                css_s1_button = tk.Button(entry_panel, text="设置速度", command=generate_s1)
                css_s1_button.grid(row=2, column=0)

            elif cmd_a == "cam_rotate_speed":
                crs_help = tk.Label(entry_panel, text="'相机旋转速度' 命令设置线性相机旋转速度.")
                crs_help.grid(row=0, column =0, columnspan=10)

                crs_s1t1_label = tk.Label(entry_panel, text="速度")
                crs_s1t1_label.grid(row=1, column=1)

                crs_s1t1 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if crs_s1t1.get("1.0","end-1c"):
                        command = "cam_rotate_speed " + crs_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                crs_s1_button = tk.Button(entry_panel, text="设置速度", command=generate_s1)
                crs_s1_button.grid(row=2, column=0)

            elif cmd_a == "lock_cam":
                loc_help = tk.Label(entry_panel, text="'锁定视角' 命令将活动摄像机锁定到一个对象(如果存在).")
                loc_help.grid(row=0, column=0, columnspan=10)
                
                loc_s1t1_label = tk.Label(entry_panel, text="目标对象")
                loc_s1t1_label.grid(row=1, column=1)

                loc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                loc_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if loc_s1t1.get("1.0","end-1c"):
                        command = "lock_cam " + loc_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                loc_s1_button = tk.Button(entry_panel, text="锁定", command=generate_s1)
                loc_s1_button.grid(row=2, column=0)

            elif cmd_a == "delta_t":
                det_help = tk.Label(entry_panel, text="'时间步长' 命令设置每个物理帧的时间步长.")
                det_help.grid(row=0, column=0, columnspan=10)
                
                det_s1t1_label = tk.Label(entry_panel, text="Delta T")
                det_s1t1_label.grid(row=1, column=1)

                det_s1t1 = tk.Text(entry_panel, width=20, height=1)
                det_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if det_s1t1.get("1.0","end-1c"):
                        command = "delta_t " + det_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                det_s1_button = tk.Button(entry_panel, text="设置步长", command=generate_s1)
                det_s1_button.grid(row=2, column=0)

            elif cmd_a == "cycle_time":
                cyt_help = tk.Label(entry_panel, text="'周期' 命令设置机器计算每个物理帧所需的周期.")
                cyt_help.grid(row=0, column=0, columnspan=10)
                
                cyt_s1t1_label = tk.Label(entry_panel, text="周期")
                cyt_s1t1_label.grid(row=1, column=1)

                cyt_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cyt_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if cyt_s1t1.get("1.0","end-1c"):
                        command = "cycle_time " + cyt_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                cyt_s1_button = tk.Button(entry_panel, text="设置周期", command=generate_s1)
                cyt_s1_button.grid(row=2, column=0)

            elif cmd_a == "output_rate":
                otr_help = tk.Label(entry_panel, text="'输出率' 命令设置输出缓冲区的每次更新周期数。\n(数字越大，更新间隔越长).")
                otr_help.grid(row=0, column=0, columnspan=10)
                
                otr_s1t1_label = tk.Label(entry_panel, text="输出率")
                otr_s1t1_label.grid(row=1, column=1)

                otr_s1t1 = tk.Text(entry_panel, width=20, height=1)
                otr_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if otr_s1t1.get("1.0","end-1c"):
                        command = "output_rate " + otr_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                otr_s1_button = tk.Button(entry_panel, text="设置输出率", command=generate_s1)
                otr_s1_button.grid(row=2, column=0)

            elif cmd_a == "note":
                nte_help = tk.Label(entry_panel, text="'注释' 命令在仿真环境中添加注释.")
                nte_help.grid(row=0, column=0, columnspan=10)
                
                nte_s1t1_label = tk.Label(entry_panel, text="注释标签")
                nte_s1t2_label = tk.Label(entry_panel, text="注释 (允许空格)")
                nte_s1t1_label.grid(row=1, column=1)
                nte_s1t2_label.grid(row=1, column=2)

                nte_s1t1 = tk.Text(entry_panel, width=20, height=1)
                nte_s1t2 = tk.Text(entry_panel, width=50, height=3)
                nte_s1t1.grid(row=2, column=1)
                nte_s1t2.grid(row=2, column=2)

                def generate_s1():
                    if nte_s1t1.get("1.0","end-1c") and nte_s1t2.get("1.0","end-1c"):
                        command = "note " + nte_s1t1.get("1.0","end-1c") + " " + nte_s1t2.get("1.0","end-1c")
                        add_to_buffer(command)

                nte_s1_button = tk.Button(entry_panel, text="记录注释", command=generate_s1)
                nte_s1_button.grid(row=2, column=0)

            elif cmd_a == "vessel_body_collision":
                vbc_help = tk.Label(entry_panel, text="'碰撞检测' 命令在仿真环境中激活或关闭卫星碰撞检测.")
                vbc_help.grid(row=0, column=0, columnspan=10)

                vbc_s1_button = tk.Button(entry_panel, text="激活", command=lambda:add_to_buffer("vessel_body_collision 1"))
                vbc_s1_button.config(width=15, height=1)
                vbc_s1_button.grid(row=1, column=0)

                vbc_s2_button = tk.Button(entry_panel, text="关闭", command=lambda:add_to_buffer("vessel_body_collision 0"))
                vbc_s2_button.config(width=15, height=1)
                vbc_s2_button.grid(row=1, column=1)

            elif cmd_a == "auto_dt":
                auto_dt_help = tk.Label(entry_panel, text="'智能步长' 命令是在仿真环境中根据用户设置的时刻自动调整delta_t的系统.\n通常有助于场景的高精度回放.")
                auto_dt_help.grid(row=0, column=0, columnspan=10)

                auto_dt_buffer_field_label = tk.Label(entry_panel, text="智能步长缓冲 = " + str(sim_time))
                auto_dt_buffer_field_label.grid(row=1, column=0)
                auto_dt_buffer_field = tk.Text(entry_panel, width=20, height=15)
                auto_dt_buffer_field.grid(row=2, column=0, rowspan=5)
                auto_dt_buffer_field.config(state="disabled")

                def set_auto_dt_field():
                    field_text = "Sim. Time - Delta_T\n"
                    
                    n = 0
                    for setting in auto_dt_buffer:
                        field_text += str(n) + ": " + str(setting[0]) + " - " + str(setting[1]) + "\n"
                        n += 1

                    auto_dt_buffer_field.config(state="normal")
                    auto_dt_buffer_field.delete(1.0, "end")
                    auto_dt_buffer_field.insert(1.0, field_text)
                    auto_dt_buffer_field.config(state="disabled")

                set_auto_dt_field()

                # auto_dt
                auto_dt_s1t1_label = tk.Label(entry_panel, text="开始时间")
                auto_dt_s1t2_label = tk.Label(entry_panel, text="时间步长")
                auto_dt_s1t1_label.grid(row=1, column=2)
                auto_dt_s1t2_label.grid(row=1, column=3)

                auto_dt_s1t1 = tk.Text(entry_panel, width=20, height=1)
                auto_dt_s1t2 = tk.Text(entry_panel, width=20, height=1)
                auto_dt_s1t1.grid(row=2, column=2)
                auto_dt_s1t2.grid(row=2, column=3)

                def generate_s1():
                    if auto_dt_s1t1.get("1.0","end-1c") and auto_dt_s1t2.get("1.0","end-1c"):
                        command = "auto_dt " + auto_dt_s1t1.get("1.0","end-1c") + " " + auto_dt_s1t2.get("1.0","end-1c")
                        add_to_buffer(command)

                auto_dt_s1_button = tk.Button(entry_panel, text="添加智能步长", command=generate_s1)
                auto_dt_s1_button.grid(row=2, column=1)

                # auto_dt_remove
                auto_dt_s2t1_label = tk.Label(entry_panel, text="智能步长ID")
                auto_dt_s2t1_label.grid(row=3, column=2)

                auto_dt_s2t1 = tk.Text(entry_panel, width=20, height=1)
                auto_dt_s2t1.grid(row=4, column=2)

                def generate_s2():
                    if auto_dt_s2t1.get("1.0","end-1c"):
                        command = "auto_dt_remove " + auto_dt_s2t1.get("1.0","end-1c")
                        add_to_buffer(command)

                auto_dt_s2_button = tk.Button(entry_panel, text="移除智能步长", command=generate_s2)
                auto_dt_s2_button.grid(row=4, column=1)

                # auto_dt_clear
                auto_dt_s3_button = tk.Button(entry_panel, text="情况智能步长", command=lambda:add_to_buffer("auto_dt_clear"))
                auto_dt_s3_button.grid(row=5, column=1)

            elif cmd_a == "rapid_compute":
                rapid_compute_help = tk.Label(entry_panel, text="'快速计算' 命令在仿真环境中切换模拟模式，在这种模式中，为了分配更多的资源用于轨迹计算\n，提供很少的用户输出，在不牺牲物理精度的情况下显着提高模拟进度率.")
                rapid_compute_help.grid(row=0, column=0, columnspan=10)

                rc_buffer_field_label = tk.Label(entry_panel, text="快速计算缓冲池 = " + str(sim_time))
                rc_buffer_field_label.grid(row=1, column=0)
                rc_buffer_field = tk.Text(entry_panel, width=21, height=15)
                rc_buffer_field.grid(row=2, column=0, rowspan=5)
                rc_buffer_field.config(state="disabled")

                def set_rc_field():
                    field_text = "Start Time - End Time\n"
                    
                    n = 0
                    for setting in rapid_compute_buffer:
                        field_text += str(n) + ": " + str(setting[0]) + " - " + str(setting[1]) + "\n"
                        n += 1

                    rc_buffer_field.config(state="normal")
                    rc_buffer_field.delete(1.0, "end")
                    rc_buffer_field.insert(1.0, field_text)
                    rc_buffer_field.config(state="disabled")

                set_rc_field()

                # rapid compute
                rc_s1t1_label = tk.Label(entry_panel, text="开始时间")
                rc_s1t2_label = tk.Label(entry_panel, text="结束时间")
                rc_s1t1_label.grid(row=1, column=2)
                rc_s1t2_label.grid(row=1, column=3)

                rc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                rc_s1t2 = tk.Text(entry_panel, width=20, height=1)
                rc_s1t1.grid(row=2, column=2)
                rc_s1t2.grid(row=2, column=3)

                def generate_s1():
                    if rc_s1t1.get("1.0","end-1c") and rc_s1t2.get("1.0","end-1c"):
                        command = "rapid_compute " + rc_s1t1.get("1.0","end-1c") + " " + rc_s1t2.get("1.0","end-1c")
                        add_to_buffer(command)

                rc_s1_button = tk.Button(entry_panel, text="添加快速计算", command=generate_s1)
                rc_s1_button.grid(row=2, column=1)

                # cancel
                rc_s2t1_label = tk.Label(entry_panel, text="快速计算ID")
                rc_s2t1_label.grid(row=3, column=2)

                rc_s2t1 = tk.Text(entry_panel, width=20, height=1)
                rc_s2t1.grid(row=4, column=2)

                def generate_s2():
                    if rc_s2t1.get("1.0","end-1c"):
                        command = "cancel_rapid_compute " + rc_s2t1.get("1.0","end-1c")
                        add_to_buffer(command)

                rc_s2_button = tk.Button(entry_panel, text="取消快速计算", command=generate_s2)
                rc_s2_button.grid(row=4, column=1)

                # clear
                rc_s3_button = tk.Button(entry_panel, text="清空快速计算缓冲", command=lambda:add_to_buffer("rapid_compute_clear"))
                rc_s3_button.grid(row=5, column=1)

            elif cmd_a == "create_barycenter":
                cbc_help = tk.Label(entry_panel, text="'创建重心' 在仿真环境中标记多个天体的质心，并允许相对于空间中虚拟点的计算.")
                cbc_help.grid(row=0, column=0, columnspan=10)

                cbc_s1t1_label = tk.Label(entry_panel, text="重心ID")
                cbc_s1t1_label.grid(row=1, column=1)
                cbc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cbc_s1t1.grid(row=2, column=1)

                cbc_s1t2_label = tk.Label(entry_panel, text="主体 (空格分割)")
                cbc_s1t2_label.grid(row=1, column=2)
                cbc_s1t2 = tk.Text(entry_panel, width=30, height=1)
                cbc_s1t2.grid(row=2, column=2)

                def generate_s1():
                    if cbc_s1t1.get("1.0","end-1c") and cbc_s1t2.get("1.0","end-1c"):
                        command = "create_barycenter " + cbc_s1t1.get("1.0","end-1c") + " " + cbc_s1t2.get("1.0","end-1c")
                        add_to_buffer(command)

                cbc_s1_button = tk.Button(entry_panel, text="创建重心", command=generate_s1)
                cbc_s1_button.grid(row=2, column=0)

            elif cmd_a == "delete_barycenter":
                dbc_help = tk.Label(entry_panel, text="'删除重心' 命令在仿真环境中移除先签标记的重心.")
                dbc_help.grid(row=0, column=0, columnspan=10)

                dbc_s1t1_label = tk.Label(entry_panel, text="重心ID")
                dbc_s1t1_label.grid(row=1, column=1)
                dbc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dbc_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dbc_s1t1.get("1.0","end-1c"):
                        command = "delete_barycenter " + dbc_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dbc_s1_button = tk.Button(entry_panel, text="删除重心", command=generate_s1)
                dbc_s1_button.grid(row=2, column=0)

            elif cmd_a == "draw_mode":
                draw_mode_help = tk.Label(entry_panel, text="'场景模式' 命令在仿真环境中选择场景可视化方法.")
                draw_mode_help.grid(row=0, column=0, columnspan=10)

                def generate_s1():
                    command = "draw_mode 0"
                    add_to_buffer(command)

                def generate_s2():
                    command = "draw_mode 1"
                    add_to_buffer(command)

                def generate_s3():
                    command = "draw_mode 2"
                    add_to_buffer(command)

                draw_mode_0_button = tk.Button(entry_panel, text="(0) 线框", command=generate_s1)
                draw_mode_0_button.config(width=20, height=1)
                draw_mode_0_button.grid(row=1, column=0)

                draw_mode_1_button = tk.Button(entry_panel, text="(1) 填充多边形", command=generate_s2)
                draw_mode_1_button.config(width=20, height=1)
                draw_mode_1_button.grid(row=1, column=1)

                draw_mode_2_button = tk.Button(entry_panel, text="(2) 填充 + 线框", command=generate_s3)
                draw_mode_2_button.config(width=20, height=1)
                draw_mode_2_button.grid(row=1, column=2)

            elif cmd_a == "point_size":
                psize_help = tk.Label(entry_panel, text="'像素点大小' 命令在仿真环境中设置场景表示远处物体的点的大小(以像素为单位).")
                psize_help.grid(row=0, column=0, columnspan=10)
                
                psize_s1t1_label = tk.Label(entry_panel, text="像素点大小")
                psize_s1t1_label.grid(row=1, column=1)

                psize_s1t1 = tk.Text(entry_panel, width=20, height=1)
                psize_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if psize_s1t1.get("1.0","end-1c"):
                        command = "point_size " + psize_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                psize_s1_button = tk.Button(entry_panel, text="设置像素点大小", command=generate_s1)
                psize_s1_button.grid(row=2, column=0)

            elif cmd_a == "lock_origin":
                lock_origin_help = tk.Label(entry_panel, text="'锁定原点' 命令在仿真环境中将全局坐标系统原点锁定到一个物体或容器，以优化该特定对象的精度.")
                lock_origin_help.grid(row=0, column=0, columnspan=10)

                lo_s1t1_label = tk.Label(entry_panel, text="对象ID")
                lo_s1t1_label.grid(row=1, column=1)

                lo_s1t1 = tk.Text(entry_panel, width=20, height=1)
                lo_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if lo_s1t1.get("1.0","end-1c"):
                        command = "lock_origin " + lo_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                lo_s1_button = tk.Button(entry_panel, text="锁定原点", command=generate_s1)
                lo_s1_button.grid(row=2, column=0)
                
        cmd_window = tk.Tk()
        cmd_window.protocol("WM_DELETE_WINDOW", on_command_window_close)
        cmd_window.title("命令")

        # why no 'sender' functionality, tkinter!?
        # anyway, here comes a wall of button definitions
        # it better look decent at runtime, at least...

        output_commands_label = tk.Label(cmd_window, text="输出管理系统")
        output_commands_label.grid(row=0, column=0, columnspan=3)
        show_button = tk.Button(cmd_window, text="输出", command=lambda:enter_cmd("show"))
        show_button.config(width=15,height=1)
        show_button.grid(row=1, column=0)
        hide_button = tk.Button(cmd_window, text="隐藏", command=lambda:enter_cmd("hide"))
        hide_button.config(width=15,height=1)
        hide_button.grid(row=1, column=1)
        clear_button = tk.Button(cmd_window, text="清空", command=lambda:enter_cmd("clear"))
        clear_button.config(width=15,height=1)
        clear_button.grid(row=1, column=2)

        vessel_commands_label = tk.Label(cmd_window, text="卫星")
        vessel_commands_label.grid(row=2, column=0, columnspan=3)
        create_vessel_button = tk.Button(cmd_window, text="创建卫星", command=lambda:enter_cmd("create_vessel"))
        create_vessel_button.config(width=15,height=1)
        create_vessel_button.grid(row=3, column=0)
        delete_vessel_button = tk.Button(cmd_window, text="删除卫星", command=lambda:enter_cmd("delete_vessel"))
        delete_vessel_button.config(width=15,height=1)
        delete_vessel_button.grid(row=3, column=1)
        fragment_button = tk.Button(cmd_window, text="残存部分", command=lambda:enter_cmd("fragment"))
        fragment_button.config(width=15,height=1)
        fragment_button.grid(row=3, column=2)

        mnv_commands_label = tk.Label(cmd_window, text="加速")
        mnv_commands_label.grid(row=4, column=0, columnspan=3)
        create_maneuver_button = tk.Button(cmd_window, text="创建加速器", command=lambda:enter_cmd("create_maneuver"))
        create_maneuver_button.config(width=15,height=1)
        create_maneuver_button.grid(row=5, column=0)
        delete_maneuver_button = tk.Button(cmd_window, text="删除加速器", command=lambda:enter_cmd("delete_maneuver"))
        delete_maneuver_button.config(width=15,height=1)
        delete_maneuver_button.grid(row=5, column=1)

        rad_press_commands_label = tk.Label(cmd_window, text="干扰")
        rad_press_commands_label.grid(row=6, column=0, columnspan=3)
        apply_rad_press_button = tk.Button(cmd_window, text="应用辐射压力", command=lambda:enter_cmd("apply_radiation_pressure"))
        apply_rad_press_button.config(width=15,height=1)
        apply_rad_press_button.grid(row=7, column=0)
        remove_rad_press_button = tk.Button(cmd_window, text="移除辐射压力", command=lambda:enter_cmd("remove_radiation_pressure"))
        remove_rad_press_button.config(width=15,height=1)
        remove_rad_press_button.grid(row=7, column=1)

        apply_atmo_drag_button = tk.Button(cmd_window, text="应用大气阻力", command=lambda:enter_cmd("apply_atmospheric_drag"))
        apply_atmo_drag_button.config(width=15,height=1)
        apply_atmo_drag_button.grid(row=8, column=0)
        remove_atmo_drag_button = tk.Button(cmd_window, text="移除大气阻力", command=lambda:enter_cmd("remove_atmospheric_drag"))
        remove_atmo_drag_button.config(width=15,height=1)
        remove_atmo_drag_button.grid(row=8, column=1)

        proj_commands_label = tk.Label(cmd_window, text="轨道投影")
        proj_commands_label.grid(row=9, column=0, columnspan=3)
        create_projection_button = tk.Button(cmd_window, text="创建投影", command=lambda:enter_cmd("create_projection"))
        create_projection_button.config(width=15,height=1)
        create_projection_button.grid(row=10, column=0)
        delete_projection_button = tk.Button(cmd_window, text="删除投影", command=lambda:enter_cmd("delete_projection"))
        delete_projection_button.config(width=15,height=1)
        delete_projection_button.grid(row=10, column=1)
        update_projection_button = tk.Button(cmd_window, text="更新投影", command=lambda:enter_cmd("update_projection"))
        update_projection_button.config(width=15,height=1)
        update_projection_button.grid(row=10, column=2)

        plot_commands_label = tk.Label(cmd_window, text="绘图仪")
        plot_commands_label.grid(row=11, column=0, columnspan=3)
        create_plot_button = tk.Button(cmd_window, text="创建绘图仪", command=lambda:enter_cmd("create_plot"))
        create_plot_button.config(width=15,height=1)
        create_plot_button.grid(row=12, column=0)
        delete_plot_button = tk.Button(cmd_window, text="删除绘图仪", command=lambda:enter_cmd("delete_plot"))
        delete_plot_button.config(width=15,height=1)
        delete_plot_button.grid(row=12, column=1)

        barycenter_commands_label = tk.Label(cmd_window, text="重心")
        barycenter_commands_label.grid(row=13, column=0, columnspan=3)
        create_barycenter_button = tk.Button(cmd_window, text="创建重心", command=lambda:enter_cmd("create_barycenter"))
        create_barycenter_button.grid(row=14, column=0)
        create_barycenter_button.config(width=15, height=1)
        delete_barycenter_button = tk.Button(cmd_window, text="删除重心", command=lambda:enter_cmd("delete_barycenter"))
        delete_barycenter_button.grid(row=14, column=1)
        delete_barycenter_button.config(width=15, height=1)

        batch_commands_label = tk.Label(cmd_window, text="文件操作")
        batch_commands_label.grid(row=15, column=0, columnspan=3)
        read_batch_button = tk.Button(cmd_window, text="读取批处理文件", command=lambda:enter_cmd("batch"))
        read_batch_button.config(width=15,height=1)
        read_batch_button.grid(row=16, column=0)
        export_button = tk.Button(cmd_window, text="导出场景", command=lambda:enter_cmd("export"))
        export_button.config(width=15,height=1)
        export_button.grid(row=16, column=1)

        cam_commands_label = tk.Label(cmd_window, text="相机控制")
        cam_commands_label.grid(row=17, column=0, columnspan=3)
        cam_strafe_speed_button = tk.Button(cmd_window, text="相机平移速度", command=lambda:enter_cmd("cam_strafe_speed"))
        cam_strafe_speed_button.config(width=15,height=1)
        cam_strafe_speed_button.grid(row=18, column=0)
        lock_cam_button = tk.Button(cmd_window, text="锁定相机", command=lambda:enter_cmd("lock_cam"))
        lock_cam_button.config(width=15,height=1)
        lock_cam_button.grid(row=18, column=1)
        unlock_cam_button = tk.Button(cmd_window, text="解锁相机", command=lambda:add_to_buffer("unlock_cam"))
        unlock_cam_button.config(width=15,height=1)
        unlock_cam_button.grid(row=18, column=2)
        cam_rotate_speed_button = tk.Button(cmd_window, text="相机旋转速度", command=lambda:enter_cmd("cam_rotate_speed"))
        cam_rotate_speed_button.config(width=15,height=1)
        cam_rotate_speed_button.grid(row=19, column=0)

        time_commands_label = tk.Label(cmd_window, text="时间控制")
        time_commands_label.grid(row=20, column=0, columnspan=3)
        delta_t_button = tk.Button(cmd_window, text="Delta T", command=lambda:enter_cmd("delta_t"))
        delta_t_button.config(width=15,height=1)
        delta_t_button.grid(row=21, column=0)
        cycle_time_button = tk.Button(cmd_window, text="周期时间", command=lambda:enter_cmd("cycle_time"))
        cycle_time_button.config(width=15, height=1)
        cycle_time_button.grid(row=21, column=1)
        output_rate_button = tk.Button(cmd_window, text="输出率", command=lambda:enter_cmd("output_rate"))
        output_rate_button.config(width=15, height=1)
        output_rate_button.grid(row=21, column=2)
        autodt_button = tk.Button(cmd_window, text="智能步长", command=lambda:enter_cmd("auto_dt"))
        autodt_button.config(width=15, height=1)
        autodt_button.grid(row=22, column=1)
        rapid_compute_button = tk.Button(cmd_window, text="计算速度", command=lambda:enter_cmd("rapid_compute"))
        rapid_compute_button.config(width=15, height=1)
        rapid_compute_button.grid(row=22, column=2)

        misc_commands_label = tk.Label(cmd_window, text="杂项")
        misc_commands_label.grid(row=23, column=0, columnspan=3)
        note_button = tk.Button(cmd_window, text="注释", command=lambda:enter_cmd("note"))
        note_button.config(width=15, height=1)
        note_button.grid(row=24, column=0)
        vessel_body_collision_button = tk.Button(cmd_window, text="卫星ID.", command=lambda:enter_cmd("vessel_body_collision"))
        vessel_body_collision_button.config(width=15, height=1)
        vessel_body_collision_button.grid(row=24, column=1)

        graphics_commands_label = tk.Label(cmd_window, text="画面质量")
        graphics_commands_label.grid(row=25, column=0, columnspan=3)
        draw_mode_button = tk.Button(cmd_window, text="绘图模式", command=lambda:enter_cmd("draw_mode"))
        draw_mode_button.config(width=15, height=1)
        draw_mode_button.grid(row=26, column=0)
        point_size_button = tk.Button(cmd_window, text="像素点大小", command=lambda:enter_cmd("point_size"))
        point_size_button.config(width=15, height=1)
        point_size_button.grid(row=26, column=1)

        selective_precision_commands_label = tk.Label(cmd_window, text="选择性感知")
        selective_precision_commands_label.grid(row=27, column=0, columnspan=3)
        lock_origin_button = tk.Button(cmd_window, text="锁定原点", command=lambda:enter_cmd("lock_origin"))
        lock_origin_button.config(width=15, height=1)
        lock_origin_button.grid(row=28, column=0)
        unlock_origin_button = tk.Button(cmd_window, text="解锁原点", command=lambda:add_to_buffer("unlock_origin"))
        unlock_origin_button.config(width=15, height=1)
        unlock_origin_button.grid(row=28, column=1)
    
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_panel_close)
    root.title("卫星协同仿真系统 图像命令面板")

    # COLUMN - OBJECTS
    objects_panel_label = tk.Label(root, text="仿真系统")
    objects_panel_label.grid(row=0, column=0)
    objects_panel = tk.Text(root, height=24, width=40)
    objects_panel.grid(row=1, column=0, rowspan=10)

    set_objects_text()

    # COLUMN - COMMAND BUTTONS
    command_button = tk.Button(root, text="输入指令", command=lambda:use_command_window())
    command_button.config(width=25, height=1)
    command_button.grid(row=1, column=2)
    delete_command_button = tk.Button(root, text="删除指令", command=lambda:use_command_delete_window())
    delete_command_button.config(width=25, height=1)
    delete_command_button.grid(row=2, column=2)
    confirm_and_close_button = tk.Button(root, text="确认指令", command=on_panel_close)
    confirm_and_close_button.config(width=25, height=1)
    confirm_and_close_button.grid(row=3, column=2)
    clear_button = tk.Button(root, text="清空指令", command=clear_command_buffer)
    clear_button.config(width=25, height=1)
    clear_button.grid(row=4, column=2)

    sim_variables_field_label = tk.Label(root, text="仿真变量")
    sim_variables_field_label.grid(row=5, column=2)
    sim_variables_field = tk.Text(root, width=25, height=7)
    sim_variables_field.grid(row=6, column=2, rowspan=5)

    set_vars_field()

    # COLUMN - COMMAND BUFFER
    cbx_label = tk.Label(root, text="命令列表")
    cbx_label.grid(row=0, column=7)
    cbx = tk.Text(root, height=24, width=40)
    cbx.grid(row=1, column=7, rowspan=10)
    cbx.config(state="disabled")
    
    root.mainloop()

    return command_buffer
