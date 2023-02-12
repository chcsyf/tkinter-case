import time, os
import tkinter as tk
import numpy as np
from PIL import Image, ImageGrab
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename
from mazeGenerator import Maze


class MazeUI:
    """迷宫游戏逻辑"""
    def __init__(self, parent, width=69, height=31):
        # 基础数据
        self.parent = parent
        self.cell = 16 # 每格边长像素
        self.rows = height if height%2 else height+1  # 高 格数
        self.cols = width if width%2 else width+1   # 宽 格数
        self.begin = int(time.time())

        # 地图数据
        self.data = Maze(self.cols, self.rows)
        self.map_generate = 0
        self.data.generate_matrix(self.map_generate)
        self.matrix = self.data.matrix

        # 玩家数据
        self.path = [] # 自动寻路的路径
        self.moves = [self.data.start] # 移动过的路径
        self.move_counter = 0 # 移动的次数
        self.back_counter = 0 # 后退的次数
        self.auto_mode = True # 局部自动寻路
        self.level = 1 # 关卡
        self.win = False

        # 地图风格
        self.colors = ("#f2f2f2",'#525288','#bc84a8','#ee3f4d')

        # 画布
        h = self.cell*self.rows; w = self.cell*self.cols
        self.canvas = tk.Canvas(self.parent, background=self.colors[0], width=w, height=h)
        self.canvas.pack()

        # 标签
        self.label = tk.Label(self.parent, text='迷宫游戏', bd=1, anchor='w')
        self.label.pack(side="bottom", fill='x')

        # 绘制初始地图
        self.draw_maze()
        self.menu()

        # 按键及事件处理
        self.canvas.bind("<Button-1>", self.auto_move)      # 自动寻路
        self.canvas.bind("<Button-3>", self.reset_move)     # 重置路径
        self.canvas.bind_all("<KeyPress>", self.event_move) # 按键路径

    def draw_maze(self):
        """ 根据数据绘制地图。 {-1:墙, 0:空白, 1:参考路径, 2: 移动过的位置} """
        # 清空画布
        self.canvas.delete("all") 
        # 绘制墙体
        for row in range(self.rows):
            for col in range(self.cols):
                if self.matrix[row, col] == 1:
                    self.draw_cell(row, col, self.colors[1])
        # 绘制起点、终点
        half = self.cell//2; d = 5
        st = self.data.start; ed = self.data.end
        self.canvas.create_rectangle(st[1]*self.cell+half-d, st[0]*self.cell+half-d,
            st[1]*self.cell+half+d, st[0]*self.cell+half+d, fill=self.colors[3], width=0)
        self.canvas.create_rectangle(ed[1]*self.cell+half-d, ed[0]*self.cell+half-d,
            ed[1]*self.cell+half+d, ed[0]*self.cell+half+d, fill=self.colors[3], width=0)
        # 绘制路径
        self.draw_path(self.path, self.colors[2], 'path')
        self.draw_path(self.moves, self.colors[3], 'moves')
        # 更新标题、标签
        self.parent.title(f"迷宫游戏   第{self.level}关")
        self.update = self.set_label_text().__next__
        self.update()

    def draw_cell(self, row, col, color):
        '''绘制方块(墙体)'''
        x, y = col*self.cell, row*self.cell
        self.canvas.create_rectangle(x, y, x+self.cell, y+self.cell, fill=color, width=0)

    def draw_path(self, path, color, tag):
        '''绘制线条(路径)。从上一个路径的中心连接到本路径中心。'''
        if path and len(path)>1:
            pts = []; half = self.cell//2
            for p in path: pts += [p[1]*self.cell+half, p[0]*self.cell+half]
            self.canvas.create_line(*pts, fill=color, width=5, tags=tag)

    def event_move(self, event):
        '''按键移动解迷宫'''
        # 判断地图状态以确定是否进入下一层
        if self.win:
            self.next_level()
            return
        # 判断是否属于移动按键以确定是否调用移动更新处理程序
        ops = {'Left':(0, -1), 'Right':(0, 1), 'Up':(-1, 0), 'Down':(1, 0),
               'a':(0, -1), 'd':(0, 1), 'w':(-1, 0), 's':(1, 0),
               'A':(0, -1), 'D':(0, 1), 'W':(-1, 0), 'S':(1, 0)}
        if event.keysym not in ops:
            return 

        prev = self.moves[-1]
        x = prev[0] + ops[event.keysym][0]; y = prev[1] + ops[event.keysym][1]
        if len(self.moves) > 1 and (x,y) == self.moves[-2]: # 回退
            self.move_counter += 1; self.back_counter += 1
            self.moves.pop()
            # 局部自动寻路
            if self.auto_mode:
                while True:
                    counter = 0 # 查找原数据两个通路的点
                    for p in self.d4(*self.moves[-1]):
                        if self.matrix[p] == 0:
                            counter += 1
                    if counter != 2:
                        break
                    self.moves.pop()
        elif x < self.rows and y < self.cols and self.matrix[x,y] == 0: # 前进
            self.move_counter += 1
            # 局部自动寻路
            pt = (x,y)
            if self.auto_mode:
                while True:
                    self.moves.append(pt)
                    temp_list = [] # 查找仅一个通路的点
                    for p in self.d4(*pt):
                        if self.matrix[p] == 0 and p != prev:
                            temp_list.append(p)
                    if len(temp_list) != 1: # pt 周围通路应该只有一个
                        break
                    prev = pt
                    pt = temp_list[0]
            else:
                self.moves.append(pt)

        # 绘制路径
        self.canvas.delete('path')
        self.canvas.delete('moves')
        self.draw_path(self.moves, self.colors[3], 'moves')

        if self.moves[-1] == self.data.end:
            x0, y0 = self.cols*self.cell //2, 30
            x1, y1 = x0 +100, y0 + 40
            self.canvas.create_rectangle(x0-100, y0, x1, y1, fill=self.colors[0],
                                outline=self.colors[1], width=3)
            self.canvas.create_text(x0, y0+20,
                text='恭喜通关！\n 按任意键进入下一关。', fill=self.colors[1])
            self.win = True

    def reset_move(self, event):
        '''重置路径'''
        self.canvas.delete('path')
        self.canvas.delete('moves')
        self.path = [] # 自动寻路的路径
        self.moves = [self.data.start] # 移动过的路径

    def auto_move(self, event):
        '''自动寻路'''
        pt = (event.y//self.cell, event.x//self.cell)
        # 判断点击处是否合法
        if self.matrix[pt] == 0:
            self.reset_move(event)
            self.path = self.data.find_path_dfs(pt)
            self.move_counter += 1
            # 绘制路径
            self.draw_path(self.path, self.colors[2], 'path')

    def set_label_text(self):
        '''更新标签'''
        while True:
            size = f'{self.cols}x{self.rows}'
            map_mode = ['Kruskal', 'DFS', 'Prim', '自定义'][self.map_generate]
            dtime = int(time.time() - self.begin)
            self.label['text'] = f"第{self.level}关   地图大小: {size}   生成算法: {map_mode}   "+\
                f"总步数: {self.move_counter}   后退步数: {self.back_counter}   用时: {dtime}s"
            self.parent.after(1000, self.update)
            yield

    def next_level(self):
        '''下一关'''
        # 地图数据
        self.map_generate %= 3
        self.data.resize_matrix(self.cols, self.rows, self.map_generate)
        self.matrix = self.data.matrix

        # 玩家数据
        self.path = [] # 自动寻路的路径
        self.moves = [self.data.start] # 移动过的路径
        self.move_counter = 0 # 移动的次数
        self.back_counter = 0 # 后退的次数
        self.level += 1 # 关卡
        self.win = False
        self.begin = int(time.time())

        # 绘制初始地图
        self.draw_maze()

    def open_map(self):
        '''读取图片格式地图数据'''
        path = askopenfilename(title='打开地图文件',initialdir='./maze_maps/',
            filetypes=[('png', '*.png'), ('All Files', '*')])
        try:
            matrix = np.asarray(Image.open(path))/255
            # 地图数据
            self.data.from_matrix(matrix) # 重置地图数据
            self.cols = self.data.width
            self.rows = self.data.height
            self.matrix = self.data.matrix
            self.map_generate = 3 # 自定义关卡

            # 玩家数据
            self.path = [] # 自动寻路的路径
            self.moves = [self.data.start] # 移动过的路径
            self.move_counter = 0 # 移动的次数
            self.back_counter = 0 # 后退的次数
            self.win = False
            self.begin = int(time.time())

            # 绘制初始地图
            self.canvas['height'] = self.cell*self.rows
            self.canvas['width'] = self.cell*self.cols
            self.draw_maze()
        except:
            showinfo(title='打开失败', message=f'打开地图失败')

    def save_map(self):
        '''保存地图数据为图片格式'''
        path = "./maze_maps/"
        if not os.path.exists(path):
            os.makedirs(path)
        image = Image.fromarray(255*self.matrix).convert('L') # 模式“L”为灰色图像
        image.save(f"{path}map{self.map_generate}_{self.cols}x{self.rows}_{time.time()}.png")
        # 展示保存成功提示
        showinfo(title='保存地图', message=f'当前地图已保存在{path}')

    def restart_level(self):
        '''重置本关卡'''
        self.reset_move('e')
        self.move_counter = 0 # 移动的次数
        self.back_counter = 0 # 后退的次数
        self.win = False
        self.begin = int(time.time())

    def to_next_level(self):
        '''跳过本关卡'''
        self.level -= 1
        self.next_level()

    def change_size(self, h, w):
        '''修改地图大小'''
        self.rows = h if h%2 else h+1  # 高 格数
        self.cols = w if w%2 else w+1   # 宽 格数
        self.canvas['height'] = self.cell*self.rows
        self.canvas['width'] = self.cell*self.cols
        self.to_next_level()

    def set_size(self, s_size):
        '''设置地图大小'''
        h,w = 11,11
        def _size():
            nonlocal h,w
            if s_size in (0,1,2):
                h,w = [(15, 19),(23, 23),(31, 59)][s_size]
                self.change_size(h, w)
            else:
                win = tk.Toplevel(self.parent)
                paddict = {'padx':20, 'pady':5}
                l1 = tk.Label(win, text='请输入宽度:').grid(row=0, column=0, **paddict)
                l2 = tk.Label(win, text='请输入高度:').grid(row=1, column=0, **paddict)
                t1 = tk.IntVar(); t1.set(self.cols)
                t2 = tk.IntVar(); t2.set(self.rows)
                tk.Entry(win, textvariable=t1).grid(row=0, column=1, **paddict)
                tk.Entry(win, textvariable=t2).grid(row=1, column=1, **paddict)
                def get_size():
                    if t1.get() >=11 and t2.get() >=11:
                        h,w = t2.get(),t1.get()
                        self.change_size(h, w)
                        win.destroy()
                tk.Button(win, text='确定', command=get_size).grid(row=3, column=0, columnspan=2, **paddict)
        return _size

    def set_auto_mode(self, auto_mode):
        '''是否开启自动寻路'''
        def fun():
            if auto_mode:
                self.auto_mode = True
            else:
                self.auto_mode = False
        return fun

    def set_map_mode(self, mode):
        '''选择算法模式'''
        def fun():
            self.map_generate = mode
            self.to_next_level()
        return fun

    def menu(self):
        # 创建菜单栏
        menubar = tk.Menu(self.parent)

        # 文件菜单选项
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='开始菜单', menu=filemenu)
        
        name1 = ['读取地图', '保存当前地图']
        func1 = [self.open_map, self.save_map]
        for i in range(len(name1)):
            filemenu.add_command(label=name1[i], command=func1[i])

        filemenu.add_separator()  # 分割线
        filemenu.add_command(label='退出游戏', command=self.parent.quit)

        # 设置菜单选项
        editmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='游戏设置', menu=editmenu)

        name2 = ['重置关卡', '跳过本关']
        func2 = [self.restart_level, self.to_next_level]
        for i in range(len(name2)):
            editmenu.add_command(label=name2[i], command=func2[i])

        # 地图大小设置菜单选项
        sizemenu = tk.Menu(editmenu, tearoff=0)
        editmenu.add_cascade(label='地图大小', menu=sizemenu)

        name21 = ['15x19', '23x23', '31x59', '自定义大小']
        func21 = [0, 1, 2, 3]
        for i in range(len(name21)):
            sizemenu.add_radiobutton(label=name21[i], command=self.set_size(func21[i]))

        # 局部自动寻路
        automenu = tk.Menu(editmenu, tearoff=0)
        editmenu.add_cascade(label='局部自动寻路', menu=automenu)

        name22 = ['局部自动寻路关', '局部自动寻路开']
        func22 = [False, True]
        for i in range(len(name22)):
            automenu.add_radiobutton(label=name22[i], command=self.set_auto_mode(func22[i]))

        # 迷宫生成算法菜单选项
        algomenu = tk.Menu(editmenu, tearoff=0)
        editmenu.add_cascade(label='生成算法', menu=algomenu)

        name23 = ['Kruskal最小生成树算法', 'dfs深度优先算法', 'prim最小生成树算法']
        func23 = [0,1,2]
        for i in range(len(name23)):
            algomenu.add_radiobutton(label=name23[i], command=self.set_map_mode(func23[i]))

        # 为窗口添加主菜单
        self.parent.config(menu=menubar)
        
    def d4(self, x, y):
        '''四向算法'''
        pts = []
        for p in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            r,c = x+p[0], y+p[1]
            if 0 < r <= self.rows-1 and 0 < c <= self.cols-1:
                pts.append((r,c))
        return pts


def main_game():
    # 创建主窗口
    windows = tk.Tk()
    windows.title("迷宫游戏")
    windows.resizable(0, 0)

    MazeUI(windows, 49,25)
    windows.mainloop()


if __name__ == '__main__':
    main_game()