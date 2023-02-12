import tkinter as tk
from PIL import ImageTk, Image
import random

class SaoLei:
    '''扫雷游戏地图数据, 0-8, 9'''
    def remap(self, x:int, y:int, mine_num:int) -> list[list[int]]:
        '''生成地图'''
        # 生成雷
        mines = random.sample(range(x*y), mine_num)
        self.mines = [(mine//x, mine%x) for mine in mines] # (y,x)
        # 打印地图
        self.data = [[0]*(x+2) for i in range(y+2)] # 地图扩大
        for j,i in self.mines:
            self[i+1,j+1] = 8
            for a in range(3):
                for b in range(3):
                    self[i+a,j+b] += 1

    def __getitem__(self, it:tuple[int]) -> int:
        return self.data[it[1]][it[0]]

    def __setitem__(self, it:tuple[int], value:int):
        self.data[it[1]][it[0]] = value


class SaoLeiUI:
    """扫雷游戏UI"""
    def __init__(self, parent):
        # 地图数据
        self.cell = 20          # 每个方块大小
        self.map = SaoLei()     # 数据
        self.level = 0          # 关卡


        # 界面
        self.menu(parent)       # 菜单栏
        self.canvas = tk.Canvas(parent)
        self.canvas.pack()
        # 图标资源
        imgs0 = [Image.open(f'images/type{i}.jpg').resize((20,20)) for i in range(9)]
        imgs1 = [Image.open(f'images/mine{i}.jpg').resize((20,20)) for i in range(4)]
        self.type_imgs = [ImageTk.PhotoImage(img) for img in imgs0]
        self.mine_imgs = [ImageTk.PhotoImage(img) for img in imgs1]

        # 新游戏
        self.new_game()        # 默认地图
        self.keep()            # 计时
        

    def menu(self, root):
        # 主菜单
        self.menubar = tk.Menu(root)
        menu_new = tk.Menu(self.menubar, tearoff=False)
        grade = ('初级10x10','中级20x20','高级50x25')
        menu_new.add_command(label=grade[0], command = lambda *e: self.new_game(0))
        menu_new.add_command(label=grade[1], command = lambda *e: self.new_game(1))
        menu_new.add_command(label=grade[2], command = lambda *e: self.new_game(2))
        self.menubar.add_cascade(label="新游戏", menu=menu_new)
        root['menu'] = self.menubar

    def new_game(self, difficulty=0):
        '''新游戏'''
        # 游戏初始数据
        self.size = ((10,10),(20,20),(50,25))[difficulty]   # 尺寸
        self.mine_num = (10, 50, 400)[difficulty]           # 雷总数
        self.map.remap(*self.size, self.mine_num)           # 刷新地图数据
        self.mines = self.map.mines                         # 地图数据
        self.label_pt = ((3,9),(3,19),(9,44))[difficulty]   # 标签位置
        self.board()                                        # 绘制地图
        # 鼠标事件
        self.canvas.bind("<Button-1>", self.call_lift)
        self.canvas.bind("<Button-3>", self.call_right)
        # 游戏进行数据
        self.bolck_rest = self.size[0]*self.size[1]         # 剩余方块个数
        self.time = 0                                       # 用时
        self.flags = {}                                     # 记录旗帜标记

    def board(self):
        '''绘制地图 格子 边框：1*cell 状态栏：2*cell'''
        cell = self.cell
        # 初始化画布
        self.canvas.delete('all')
        self.canvas['width'] = (self.size[0]+2)*self.cell
        self.canvas['height'] = (self.size[1]+4)*self.cell
        
        # 绘制地图
        self.image_map = [[None]*self.size[0] for i in range(self.size[1])]
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                self.image_map[j][i] = self.canvas.create_image((i+1.5)*self.cell,
                        (j+3.5)*self.cell, image=self.mine_imgs[-1])

        # 绘制状态栏
        y = self.cell*1.5
        x1 = (self.label_pt[0])*self.cell; x2 = (self.label_pt[1])*self.cell
        self.canvas.create_text(x1,y, font="SimHei 18 bold", text='00:00', 
                            fill='red', tags='time')
        self.canvas.create_text(x2,y, font="SimHei 18 bold", fill='red',
                            text=f'00{self.mine_num}'[-3:], tags='mines')

    def call_lift(self, event):
        '''鼠标左键事件'''
        x = event.x//self.cell-1  # 换算坐标
        y = event.y//self.cell-3
        
        if x<0 or x>=self.size[0] or y<0 or y>=self.size[1] or (x,y) in self.flags:
            return
        self.canvas.delete(self.image_map[y][x])
        self.bolck_rest -= 1
        self.image_map[y][x] = None
        val = self.map[x+1,y+1]
        if val<8:
            self.canvas.create_image(((x+1.5)*self.cell,
                (y+3.5)*self.cell), image=self.type_imgs[val])
            # 清除所有0方块
            if val == 0:
                self.clear_zero(x+1, y+1)
            # 判断是否获胜：如果剩余方块等于雷数量
            if self.bolck_rest == self.mine_num:
                self.game_over('胜利！')
        else:
            self.canvas.create_image(((x+1.5)*self.cell,
                            (y+3.5)*self.cell), image=self.mine_imgs[1])
            self.game_over('失败！')

    def clear_zero(self, x, y):
        '''删除所有0方块'''
        nbo= lambda pt:[(pt[0]-1,pt[1]),(pt[0]+1,pt[1]),(pt[0],pt[1]-1),
                        (pt[0],pt[1]+1),(pt[0]-1,pt[1]-1),(pt[0]+1,pt[1]-1),
                        (pt[0]+1,pt[1]+1),(pt[0]-1,pt[1]+1)]
        stack = [] # 栈
        stack.append((x,y))
        while stack:
            pt = stack.pop()
            for p in nbo(pt):
                if 0<p[0]<=self.size[0] and 0<p[1]<=self.size[1]:
                    i,j = p; val = self.map[p]
                    if self.image_map[j-1][i-1]:
                        if not val: stack.append(p)
                        self.canvas.delete(self.image_map[j-1][i-1])
                        self.bolck_rest -= 1
                        self.image_map[j-1][i-1] = None
                        self.canvas.create_image(((i+0.5)*self.cell,
                                (j+2.5)*self.cell), image=self.type_imgs[val])

    def call_right(self, event):
        '''鼠标右键事件'''
        x = event.x//self.cell-1  # 换算坐标
        y = event.y//self.cell-3

        if x<0 or x>=self.size[0] or y<0 or y>=self.size[1] or \
                        self.image_map[y][x] == None:
            return
        if (x,y) in self.flags:
            self.canvas.delete(self.flags[(x,y)])
            del self.flags[(x,y)]
        else:
            self.flags[(x,y)] = self.canvas.create_image(((x+1.5)*self.cell,
                            (y+3.5)*self.cell), image=self.mine_imgs[2])
        if self.mine_num<len(self.flags):
            self.game_over('失败！')
            return
        mine_rest = '00'+str(self.mine_num-len(self.flags))
        self.canvas.itemconfig('mines', text=mine_rest[-3:])

    def keep(self):
        '''计时'''
        self.canvas.after(1000, self.keep)
        self.time += 1
        s = ('0'+str(self.time%60))[-2:]; m = ('0'+str(self.time//60))[-2:]
        self.canvas.itemconfig('time', text=f'{m}:{s}')

    def game_over(self, text):
        font = "SimHei 30 bold"
        x,y = self.size[0]*self.cell*0.6, self.size[1]*self.cell*0.6
        self.canvas.create_text(x, y, text=text, fill = 'red', font=font)
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")

if __name__ == '__main__':
    win = tk.Tk()
    SaoLeiUI(win)
    tk.mainloop()