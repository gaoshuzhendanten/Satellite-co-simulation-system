import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import geopy.distance
import random
from math import radians, cos, sin, sqrt, ceil

HEIGHT = 2000 #轨道高度
SAMPLES_TIMES = 100 #均匀随机抽样个数
LENGTH = 3000 #探测覆盖半径
RADIUS = 6371 #地球半径
SPEED = 7900 #总速度
matplotlib.rcParams['font.sans-serif']=['SimSun']

class Satellite:
    def __init__(self, height, ascending, inclination):  # 轨道高度， 升交点， 轨道面倾角三要素 确定轨道平面
        self.height = height
        self.ascending = ascending
        self.inclination = inclination
        self.normal_vector = self.get_normal_vector()
        self.name = ""

    def __str__(self):
        B = radians(self.ascending)  # 升交点弧度数
        # return [r,g,b]|[x,y,z]|[vx,vy,vz]
        return str([random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]) + '|'\
            + str([ceil((RADIUS+self.height)*cos(B)*1000),ceil((RADIUS+self.height)*sin(B)*1000),0]) + '|'\
            + str(list(self.get_speed_direction()))

    def get_speed_direction(self):
        B = radians(self.ascending)  # 升交点弧度数
        x0,y0,z0 = self.normal_vector
        x1,y1,z1 = (cos(B), sin(B), 0)
        a,b,c = y0*z1-y1*z0,x1*z0-x0*z1,x0*y1-x1*y0
        t = SPEED/sqrt(a**2+b**2+c**2)
        return a*t,b*t,c*t


    def get_normal_vector(self):
        A = radians(self.inclination)  # 轨道面倾角弧度数
        B = radians(self.ascending)  # 升交点弧度数
        return (-sin(A) * sin(B), sin(A) * cos(B), -cos(A))

    def get_distance(self, pos):
        a, b, c = self.normal_vector  # 单位法向量
        B = radians(self.ascending)  # 升交点弧度数
        x0, y0, z0 = (cos(B), sin(B), 0)  # 轨道平面内一点（升交点）
        x, y, z = pos  # 探测点
        t = (a * x0 + b * y0 + c * z0 - (a * x + b * y + c * z)) / (a ** 2 + b ** 2 + c ** 2)
        x1, y1, z1 = x + a * t, y + b * t, z + c * t  # 投影点
        tmp1 = self.between_distance(pos, (x1, y1, z1))
        tmp2 = RADIUS + self.height - sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2)
        return sqrt(tmp1 ** 2 + tmp2 ** 2)

    def between_distance(self, pos1, pos2):
        ans = 0
        for i in range(len(pos1)):
            ans += (pos1[i] - pos2[i]) ** 2
        return sqrt(ans)


def generate_satellite():
    return Satellite(HEIGHT, random.uniform(-180, 180), random.uniform(-80, 80))


def generate_satellites(num_satellites):
    satellites = []
    for i in range(num_satellites):
       satellites.append(generate_satellite())
    return satellites

def trapeze2coord(pos):
    lot,lat = pos
    return (RADIUS*cos(lot)*cos(lat), RADIUS*sin(lot)*cos(lat), RADIUS*sin(lat))


def calc_fitness(satellites, area):
    fitness = 0
    #均匀随机抽样近似探测区域
    samples_area = []
    samples_area = [(random.uniform(area[0],area[1]),random.uniform(area[2],area[3])) for i in range(SAMPLES_TIMES)]
    # if(len(samples_area)==0):
        # for i in range(SAMPLES_TIMES):
        #     samples_area.append((random.uniform(area[0],area[1]),random.uniform(area[2],area[3])))
    for pos in samples_area:
        for satellite in satellites:
            if satellite.get_distance(trapeze2coord(pos)) < LENGTH:
                fitness+=1
                break
    return ceil(fitness*1./SAMPLES_TIMES * 100)


# # #固定抽样点
# samples_area = []
# def calc_fitness(satellites, area):
#     fitness = 0
#     if(len(samples_area)==0):
#         line0 = np.linspace(area[0],area[1],10)
#         line1 = np.linspace(area[2], area[3], 10)
#         for lon in line0:
#             for lat in line1:
#                 samples_area.append((lon, lat))
#     for pos in samples_area:
#         for satellite in satellites:
#             if satellite.get_distance(trapeze2coord(pos)) < LENGTH:
#                 fitness+=1
#                 break
#     return fitness


def genetic_algorithm(num_satellites, area, num_generations, population_size, mutation_rate):
    # 初始化适应度值和子代种群
    fitness = np.zeros(population_size)  #初始化适应度
    population = [generate_satellites(num_satellites) for i in range(population_size)]  #初始化种群

    max_score = [] #绘制迭代曲线
    for i in range(num_generations):  #迭代次数
        for j in range(population_size):  #遍历种群计算相应初始适应度
            fitness[j] = calc_fitness(population[j], area)
        # 排序保留适应度最高的四分之一种群
        sorted_population = [p for _, p in sorted(zip(fitness, population), key=lambda x: x[0], reverse=True)]
        elites = sorted_population[0:population_size // 4]
        max_score.append(calc_fitness(sorted_population[0],area))
        print(f'第{i + 1}次迭代 max_score:{max_score[i]}')
        # max_score.append(max(fitness))
        # 选择操作
        fitness_probs = fitness / np.sum(fitness)
        new_population = []
        for j in range(population_size//4 * 3):
            parent1_idx = np.random.choice(range(population_size), p=fitness_probs)
            parent2_idx = np.random.choice(range(population_size), p=fitness_probs)
            parent1 = population[parent1_idx]
            parent2 = population[parent2_idx]
            # 交叉操作
            crossover_point = np.random.choice(range(num_satellites))
            child = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
            # 变异操作
            if np.random.rand() < mutation_rate:
                mutation_point = np.random.choice(range(num_satellites))
                child[mutation_point] = generate_satellite()
            new_population.append(child)
        population = elites+new_population
    # 返回最优解
    fitness = np.zeros(population_size)
    for j in range(population_size):
        fitness[j] = calc_fitness(population[j],area)
    best_idx = np.argmax(fitness)
    max_score.append(fitness[best_idx])
    plt.plot(range(1,num_generations+2), max_score, c='blue')
    plt.xlabel("迭代次数", fontdict={'size': 16})
    plt.ylabel("得分", fontdict={'size': 16})
    plt.title("迭代次数得分曲线", fontdict={'size': 20})
    plt.savefig('data/images/适应度函数的拟合效果1.png')
    plt.show()
    return population[best_idx], fitness[best_idx]

def export_satellites(satellites, area, area_name):
    file_path = "my_scenarios/"+input("export file name :")+".osf"
    lines = ['B|Earth|data/models/miniearth.obj|5972000000000000000000000|6371000|[0.0,0.25,1.0]|[0,0,0]|[0,0,0]|[[1,0,0],[0,1,0],[0,0,1]]|86400|0|0|0|0\n']
    lines.append(f'S|{area_name}|Earth|[1,0,0]|[{(area[2]+area[3])/2.},{(area[0]+area[1])/2.},0]')
    for satellite in satellites:
        line = 'V|' + satellite.name + '|data/models/minisat.obj|' + str(satellite)
        lines.append(line + '\n')
    with open(file_path,'w',encoding='utf-8') as f:
        f.write('\n'.join(lines))

def draw_muti_stage(area):
    y = []
    x = range(1,6)
    for i in x:
        best_solution, scores = genetic_algorithm(num_satellites=i, area=area, num_generations=100, population_size=100, mutation_rate=0.2)
        y.append(scores)
    plt.plot(x, y, c='blue')
    plt.xlabel("自主单星数", fontdict={'size': 16})
    plt.ylabel("覆盖率", fontdict={'size': 16})
    plt.title("多颗自主单星协同效果曲线", fontdict={'size': 20})
    plt.savefig('data/images/多颗自主单星协同效果曲线.png')
    plt.show()



if __name__ == "__main__":
    num_satellites = int(input("部署卫星个数："))
    area = tuple(map(int,input("探测区域范围：").split()))
    # draw_muti_stage(area)
    best_solution, scores = genetic_algorithm(num_satellites=num_satellites, area=area, num_generations=100, population_size=100, mutation_rate=0.2)
    print('Best solution:', [(satellite.height, satellite.ascending, satellite.inclination) for satellite in best_solution])
    print('Scores:', scores)
    state_code = input("是否导出并运行可视化仿真系统:")
    if state_code=='q' or state_code.lower()=='no':
        pass
    else:
        for i, satellite in enumerate(best_solution):
            satellite.name = input(f'请输入第 {i + 1} 个卫星名称: ')
        area_name = input('请输入探测区域名称: ')
        export_satellites(best_solution, area, area_name)
        from main import *


"""
main.py: Initializer, command interpreter, main loop and high-level essential functionality routines.
初始化器、命令解释器、主循环和高级基本功能例程。
solver.py: Physics integrators.
物理积分器。
graphics.py: OpenGL functions for 3D rendering.
用于3D渲染的OpenGL函数。
vessel_class.py: The 'vessel' class used for representing spacecraft or small objects such as debris chunks which do not generate notable gravitational fields.
“容器”类，用于表示航天器或不产生显著引力场的碎片等小物体。
body_class.py: The 'body' class used for representing celestial bodies such as planets or asteroids, which DO generate notable gravitational fields.
“body”类，用于表示天体，如行星或小行星，它们会产生显著的引力场。
camera_class.py: The 'camera' class used for representing camera objects to move and rotate the user's point of view, as well as track objects in the 3D scene.
'camera'类，用于表示相机对象来移动和旋转用户的视角，以及在3D场景中跟踪对象。
surface_point_class.py: The 'surface_point' class used for representing points on the surfaces of celestial bodies, such as tracking stations, geographical features or landing zones.
'surface_point'类，用于表示天体表面上的点，如跟踪站、地理特征或着陆区。
barycenter_class.py: The 'barycenter' class used for marking barycenters of two or more celestial bodies and making calculations relative to them.
' barycenter_class.py '质心'类，用于标记两个或多个天体的质心并相对于它们进行计算。
maneuver.py: The 'maneuver' classes used for various types of maneuvers that can be performed by spacecraft.
“机动”类，用于航天器可以执行的各种类型的机动。
radiation_pressure.py: The 'radiation_pressure' class used to simulate the effects of radiation pressure on spacecraft.
'radiation_pressure'类，用于模拟辐射压力对航天器的影响。
atmospheric_drag.py: The 'atmospheric_drag' class used to simulate the effects of atmospheric drag on spacecraft.
'atmospheric_drag'类，用于模拟大气阻力对航天器的影响。
math_utils.py: General mathematical functions that are not provided by the math library.
数学库不提供的一般数学函数。
orbit.py: 2-body Keplerian orbit class that is used for making quick trajectory projections into the future.
 2体开普勒轨道类，用于对未来进行快速轨道预测。
plot.py: Plot class that handles plotting of variables in certain time intervals on user's demand.
绘图类，它根据用户的需要在特定的时间间隔内处理变量的绘图。
command_panel.py: Command panel window which provides a basic GUI interface for entering commands easily.
命令面板窗口，提供了一个基本的GUI界面，方便输入命令。
config_utils.py: Handles reading and editing of config files at data/config which hold values that the simulations are initialized with. More of a convenience utility rather than a necessity.
处理data/config配置文件的读取和编辑，该配置文件保存模拟初始化时使用的值。与其说是必需品，不如说是一种方便。
ui.py: Includes functions to print alphanumeric characters on 3D viewport to help out graphics.py.
包括在3D视口打印字母数字字符的函数，以帮助graphics.py。
vector3.py: 3D vector class to handle vector math/operations.
3D矢量类，用于处理矢量数学/运算。
"""