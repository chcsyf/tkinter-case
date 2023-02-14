import random

class CellShape:
    '''形状类'''

    # 骨牌种类
    SHAPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    # 骨牌形状和旋转形状的坐标点集(y,x) 旋转中心为(0,0) 
    I = [[(0, -1), (0, 0), (0, 1), (0, 2)],
         [(-1, 0), (0, 0), (1, 0), (2, 0)]]
    J = [[(-1, 0), (0, 0), (1, 0), (1, -1)],
         [(-1, 0), (0, 0), (0, 1), (0, 2)],
         [(-1, 1), (-1, 0), (0, 0), (1, 0)],
         [(0, -1), (0, 0), (0, 1), (-1, 1)]]
    L = [[(-1, 0), (0, 0), (1, 0), (1, 1)],
         [(1, 0), (0, 0), (0, 1), (0, 2)],
         [(-1, -1), (-1, 0), (0, 0), (1, 0)],
         [(0, -1), (0, 0), (0, 1), (1, 1)]]
    O = [[(0, 0), (0, 1), (1, 0), (1, 1)]]
    S = [[(-1, 0), (0, 0), (0, 1), (1, 1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)]]
    T = [[(0, -1), (0, 0), (0, 1), (-1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, 1)],
         [(0, -1), (0, 0), (0, 1), (1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, -1)]]
    Z = [[(0, -1), (0, 0), (1, 0), (1, 1)],
         [(-1, 0), (0, 0), (0, -1), (1, -1)]]
    SHAPES_DIR = {'I': I, 'J': J, 'L': L, 'O': O, 'S': S, 'T': T, 'Z': Z}

    # 形状颜色
    CUBE_COLORS = ['#cc9999','#ffff99','#666699','#990066',
                    '#ffcc00','#cc0033','#ff0033','#006699',
                    '#ffff33','#990033','#ccff66','#ff9900']

    def __init__(self, width, height):
        '''数据的坐标关系是 y+: 向下，x+: 向右'''
        self.width = width                  # 屏幕宽度
        self.height = height                # 屏幕高度
        self.matrix = [['']*width for 
                    _ in range(height)]     # 已堆砌骨牌数据矩阵
        self.score = 0                      # 得分

        self.next = self.new_shape()        # 新骨牌信息

    def new_shape(self):
        '''新骨牌'''
        shape = random.choice(self.SHAPES)      # 骨牌名称
        dirs = len(self.SHAPES_DIR[shape])      # 骨牌的旋转形状个数
        _dir = random.randint(0, dirs-1)        # 骨牌的旋转形状序号
        return shape, dirs, _dir

    def init_shape(self):
        '''当前和下一个骨牌'''
        if not self.next:
            self.next = self.new_shape()
        self.shape = self.next[0]                       # 当前骨牌名称
        self.dirs = self.next[1]                        # 当前骨牌的旋转形状个数
        self.dir = self.next[2]                         # 当前骨牌的旋转形状序号
        self.color = random.choice(self.CUBE_COLORS)    # 当前骨牌颜色
        self.next = self.new_shape()                    # 新骨牌信息
        self.center = (1, self.width//2)                # 骨牌初始的位置
        return self.SHAPES_DIR[self.next[0]][0]

    def get_gridpos(self, center=None, _dir=None):
        '''当前骨牌在位置center时的点集 动态'''
        center = self.center if center is None else center
        _dir = self.dir if _dir is None else _dir
        curr_shape = self.SHAPES_DIR[self.shape][_dir]

        # 计算并判断是否超出屏幕或发生碰撞
        new_shape = []
        for cube in curr_shape:
            y = cube[0]+center[0]; x = cube[1]+center[1]
            if x < 0 or y < 0 or y >= self.height or \
                    x >= self.width or self.matrix[y][x]:
                return False
            new_shape.append((y,x))
        return new_shape

    def stop(self, shape):
        '''停止下降时 更新matrix'''
        # 绘制图形
        for y,x in shape:
            self.matrix[y][x] = self.color

        # 判断是否消除 从下往上，逐行
        y = self.height-1
        while y > 0:
            if all(self.matrix[y]):
                self.remove_line(y)
            else:
                y -= 1

    def remove_line(self, line):
        # 删除满行
        self.score += 1
        for p in range(line, 0, -1):
            if any(self.matrix[p]):
                self.matrix[p] = self.matrix[p-1][:]
            else:
                break
        self.matrix[0] = ['']*self.width

    def rotate(self):
        '''旋转'''
        new_dir = (self.dir+1) % self.dirs

        # 判断是否可以旋转
        new_shape = self.get_gridpos(_dir=new_dir)
        if new_shape:
            self.dir = new_dir
            return new_shape
        else:
            return False

    def move(self, r='d'):
        '''下降、左移动、右移动'''
        moves = {'d':(1,0),'l':(0,-1),'r':(0,1)}
        center = (self.center[0]+moves[r][0],
                  self.center[1]+moves[r][1])

        # 判断是否可以移动
        new_shape = self.get_gridpos(center=center)
        if new_shape:
            self.center = center
            return new_shape
        else:
            return False

import tkinter as tk

class Tetris:
    '''俄罗斯方块游戏'''
    def __init__(self, win, screen_width, height, info_width):
        '''初始化数据 坐标关系是 y+: 向下，x+: 向右'''
        self.width = screen_width
        self.height = height
        self.fps = (500, 300, 200, 100)
        self.level = 2      # 难度 难度越高，下落速度越快
        self.cellShape = CellShape(screen_width, height+2) # y+2
        self.game_over = False
        self.time = 0

        # 画布
        cell = 20 # 每格大小
        self.canvas = tk.Canvas(win, height=height*cell,
                        width=(screen_width+info_width)*cell, bg='#303030')
        self.canvas.pack()

        # 绘制背景纹理
        self.info_shape = [None]*3
        self.bg_cells = [[None]*screen_width for _ in range(height)]
        self.draw_background(screen_width, height, cell)
        
        # 开始游戏
        self.canvas.bind_all("<KeyPress>", self.event_move) # 按键路径
        self.new_shape()    # 初始化第一个骨牌
        self.run()          # 开始游戏


    def draw_background(self, screen_width, height, cell):
        '''绘制背景'''
        color = '#454545'
        for i in range(1, screen_width):
            self.canvas.create_line(i*cell, 0, i*cell, height*cell, fill=color)
        for i in range(1, height):
            self.canvas.create_line(0, i*cell, screen_width*cell, i*cell, fill=color)
        self.canvas.create_line(screen_width*cell, 0, screen_width*cell, height*cell,
                        width=1, fill='silver')
        self.canvas.create_line(screen_width*cell+3, 0, screen_width*cell+3, height*cell,
                        width=1, fill='silver')

        left = (screen_width+1.5)*cell; w = 15 # 每个字宽度
        style = {'font': ('微软雅黑', 12), 'fill':'#d3d3d3'}
        self.canvas.create_text(left, 2*cell, **style, text='分数')
        self.canvas.create_text(left+w, 6*cell, **style, text='最高分数')
        self.canvas.create_text(left+0.5*w, 10*cell, **style, text='下一个')
        self.canvas.create_text(left, 17*cell, **style, text='等级')
        self.canvas.create_text(left, 21*cell, **style, text='用时')

        font = ('微软雅黑', 20); left = (screen_width+3.5)*cell; w = 20 # 每个字宽度
        self.canvas.create_text(left, 4*cell, **style, text='     0', tags='score')
        self.canvas.create_text(left, 8*cell, **style, text='     0', tags='max_score')
        self.canvas.create_text(left+2*w, 19*cell, **style, text='1', tags='level')
        self.canvas.create_text(left+0.75*w, 23*cell, **style, text='00:00', tags='time')

        half = cell//2
        for y in range(11, 14):
            line = []
            for x in range(screen_width+2, screen_width+6):
                line.append(self.canvas.create_rectangle(x*cell, y*cell+half, (x+1)*cell,
                        (y+1)*cell+half, fill='', outline='', tags='info'))
            self.info_shape[y-11] = line

        for y in range(self.height):
            for x in range(self.width):
                self.bg_cells[y][x] = self.canvas.create_rectangle(x*cell, y*cell,
                                    (x+1)*cell, (y+1)*cell, fill='', outline='')

        self.canvas.create_text(screen_width//2*cell, 12*cell, font=('微软雅黑', 32), 
                    text='GAME OVER!', tags='over', fill='')

    def run(self):
        '''开始游戏'''
        if not self.game_over:
            if not self.move():
                self.stop()
                self.new_shape()
            t = self.fps[self.level-1]
            self.canvas.after(t, self.run)
            self.time += t
            # 计时
            time = self.time//1000
            m = ('00'+str(time//60))[-2:]; s = ('00'+str(time%60))[-2:]
            self.canvas.itemconfig('time', text= m+':'+s)
        else:
            self.canvas.itemconfig('over', fill= '#d3d3d3')


    def new_shape(self):
        '''生成新骨牌'''
        # 更新信息栏
        self.canvas.itemconfig('info', fill='')
        for y,x in self.cellShape.init_shape(): # 下一个图形
            self.canvas.itemconfig(self.info_shape[y+1][x+1], fill='#d3d3d3')
        # 计算新骨牌坐标
        self.gridpos = self.cellShape.get_gridpos()   # 计算骨牌初始位置
        self.game_over = not bool(self.gridpos)

    def event_move(self, event):
        '''按键操作'''
        ops = {'Left':'l', 'Right':'r', 'Down':'d', 'Up': 'u',
               'a':'l', 'd':'r', 's':'d', 'w': 'u',
               'A':'l', 'D':'r', 'S':'d', 'W': 'u'}
        if event.keysym in ops:
            self.move(ops[event.keysym])

    def move(self, r='d'):
        '''骨牌移动'''
        if r == 'u':
            new_shape = self.cellShape.rotate()
        else:
            new_shape = self.cellShape.move(r)
        if new_shape:
            for y,x in self.gridpos:
                if y>=2:
                    self.canvas.itemconfig(self.bg_cells[y-2][x], fill='')
            for y,x in new_shape:
                if y>=2:
                    self.canvas.itemconfig(self.bg_cells[y-2][x],
                                    fill=self.cellShape.color)
            self.gridpos = new_shape
            return True
        else:
            return False

    def stop(self):
        '''骨牌停止移动'''
        self.cellShape.stop(self.gridpos)
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.itemconfig(self.bg_cells[y][x],
                            fill=self.cellShape.matrix[y+2][x])
                
        # 更新分数
        s = ('     '+str(self.cellShape.score))[-6:]
        self.canvas.itemconfig('score', text=s)


def tetris_game():
    '''俄罗斯方块游戏入口'''
    HEIGHT = 25         # 高度
    SCREEN_WIDTH = 15   # 屏幕宽度
    INFO_WIDTH = 7      # 信息栏宽度

    win = tk.Tk()
    Tetris(win, SCREEN_WIDTH, HEIGHT, INFO_WIDTH)
    win.mainloop()


if __name__ == '__main__':
    tetris_game()