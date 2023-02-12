import time
import tkinter as tk, tkinter.messagebox as messagebox
from threading import Timer
from connect import Connect

class ConnectUI:
    '''连连看'''
    timer_interval = 0.1  # 连线延迟时间
    imgs = None # 图片对象

    def __init__(self, parent, size = (10,10), animals = 19):
        self.cell = 45

        # 地图数据
        self.connect = Connect(*size, animals)
        self.size = self.connect.w, self.connect.h
        self.num = self.connect.num
        self.map = self.connect.map
        self.level = 1

        # 主框架
        frame = tk.Frame(parent)
        frame.pack()
        w = self.cell*(self.size[0]+1); h = self.cell*(self.size[1]+1)
        self.canvas = tk.Canvas(frame, background='lightblue', width=w, height=h)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)  # 鼠标左键事件
        self.label = tk.Label(frame, text='连连看', bd=1, anchor='w')
        self.label.pack(side="bottom", fill='x')

        # 所有图标图案
        self.imgs = [tk.PhotoImage(file=f'images\\animal ({i}).png') for i in range(19)]

        # 绘制地图
        self.draw_map()
        self.set_label_text()
        self.menu(parent)

    def draw_map(self):
        '''绘制地图'''
        self.canvas.delete('all')
        self.has_first = False          # 是否已选择第一个图案
        self.choices = [(0, 0),(0, 0)]   # 被选中图案坐标
        self.begin = int(time.time())

        self.image_map = [[None]*self.size[1] for x in range(self.size[0])]
        for x in range(1, self.size[0]+1):
            for y in range(1, self.size[1]+1):
                if self.map[x][y]:
                    img = self.imgs[int(self.map[x][y]-1)]
                    self.image_map[x-1][y-1] = self.canvas.create_image(
                            (x*self.cell, y*self.cell), image=img)

    def click(self, event):
        '''鼠标左键事件代码'''
        half = self.cell//2
        x = (event.x+half)//self.cell # 换算棋盘坐标
        y = (event.y+half)//self.cell
        print("点击：", x, y)

        if not self.map[x][y]:
            return
        if not self.has_first:
            self.choices[0] = (x, y)
            # 画 第一处 的框线
            self.canvas.create_rectangle(x*self.cell-half, y*self.cell-half, x*self.cell+half,
                        y*self.cell+half, width=2, outline="blue", tags='choice')
            self.has_first = True
        else:
            self.choices[1] = (x, y)
            if self.choices[1] == self.choices[0]:
                return
            # 画 第二处 的框线
            self.canvas.create_rectangle(x*self.cell-half, y*self.cell-half, x*self.cell+half,
                        y*self.cell+half, width=2, outline="blue", tags='choice')
            self.has_first = False
            self.canvas.pack()
            # 判断是否连通
            pts = self.connect.removed(*self.choices[0], *self.choices[1])
            if pts:
                # 画选中方块之间连接线
                lpts = [i*self.cell if i else 0.1*self.cell for i in pts[1]]
                self.lines = self.canvas.create_line(*lpts, width=3, fill='red', tags='lines')
                # 定时删除画线
                Timer(self.timer_interval, self.clear).start()
                if self.connect.is_win():
                    Timer(self.timer_interval, self.win).start()
            else:
                self.canvas.delete('choice')

    def clear(self):
        '''清除连线及方块'''
        self.canvas.delete('choice')
        self.canvas.delete(self.image_map[self.choices[0][0]-1][self.choices[0][1]-1])
        self.canvas.delete(self.image_map[self.choices[1][0]-1][self.choices[1][1]-1])
        self.canvas.delete('lines')

    def next_level(self, size=None):
        '''跳过本关卡'''
        if size:
            self.size = size
        else:
            self.size = self.size[0]+1,self.size[1]+1
        self.num = self.num+1 if self.num<10 else self.num
        self.connect = Connect(self.size[1],self.size[0], self.num)
        self.size = self.connect.w, self.connect.h
        self.num = self.connect.num
        self.map = self.connect.map
        self.canvas['width'] = self.cell*(self.size[0]+1)
        self.canvas['height'] = self.cell*(self.size[1]+1)
        self.draw_map()

    def set_size(self):
        '''自定义地图大小'''
        win = tk.Toplevel(self.canvas)
        paddict = {'padx':20, 'pady':5}
        l1 = tk.Label(win, text='请输入宽度:').grid(row=0, column=0, **paddict)
        l2 = tk.Label(win, text='请输入高度:').grid(row=1, column=0, **paddict)
        t1 = tk.IntVar(); t1.set(self.size[0])
        t2 = tk.IntVar(); t2.set(self.size[1])
        tk.Entry(win, textvariable=t1).grid(row=0, column=1, **paddict)
        tk.Entry(win, textvariable=t2).grid(row=1, column=1, **paddict)
        def get_size():
            if t1.get() >=2 and t2.get() >=2:
                self.next_level((t1.get(),t2.get()))
                win.destroy()
        tk.Button(win, text='确定', command=get_size).grid(row=3, column=0, columnspan=2, **paddict)

    def win(self):
        messagebox.showinfo(title='获胜', message = '挑战成功！ 进入下一关。')
        # 下一关
        self.level += 1
        self.next_level()

    def set_label_text(self):
        '''更新信息栏'''
        try:
            dtime = int(time.time() - self.begin)
            self.label['text'] = f"第{self.level}关   地图大小: {self.size}   用时: {dtime}s"
            Timer(1, self.set_label_text).start()
        except:
            print('程序结束')

    def menu(self, root):
        # 创建菜单栏
        menubar = tk.Menu(root)

        # 设置菜单选项
        editmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='游戏设置', menu=editmenu)

        name = ['跳过本关', '自定义地图大小']
        func = [self.next_level, self.set_size]
        for i in range(len(name)):
            editmenu.add_command(label=name[i], command=func[i])

        # 为窗口添加主菜单
        root.config(menu=menubar)


def app():
    win = tk.Tk()
    win.title('tkinter连连看')

    ConnectUI(win, (9,7), 16)
    win.mainloop()

if __name__ == '__main__':
    app()