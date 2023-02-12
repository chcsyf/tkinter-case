import tkinter as tk
import random

class SortList:
    '''列表排序的过程记录'''
    def __init__(self, length=15, Range = (1, 32)):
        self.length = length
        self.ymax = Range[1]
        # 生成随机列表
        num = [i for i in range(*Range)]
        random.shuffle(num) # 打乱列表
        self.source = num[:length]  # 取随机数组的前length个元素
        self.list = self.source[:]  # 拷贝一份用于排序

    def bubbleSort(self):
        '''生成冒泡排序的步骤'''
        yield self.length-1,0,False
        for i in range(self.length-1, 0, -1):
            for j in range(i):
                if self.list[j] > self.list[j+1]:
                    self.list[j], self.list[j+1] = self.list[j+1], self.list[j]
                    yield i,j,True
                else:
                    yield i,j,False
    
    def selectionSort(self):
        '''生成选择排序的步骤'''
        for i in range(self.length-1, 0, -1):
            Max = 0
            yield i,0,0
            for j in range(i):
                if self.list[j+1] > self.list[Max]:
                    Max = j+1
                    yield i,j+1,0
                else:
                    yield i,j+1,2
            self.list[i], self.list[Max] = self.list[Max], self.list[i]
            yield i,Max,1

class SortAnimation:
    """排序动画"""
    def __init__(self, parent, width,height, sortList=SortList(), sort_func='bubble'):
        self.parent = parent
        self.cvs = tk.Canvas(parent, bg='white', width=width, height=height)
        self.cvs.place(x=0, y=0)
        self.sortList = sortList
        self.length = sortList.length
        # 绘图
        x0 = 50     # 矩形条x轴初始值
        y0 = 350    # 矩形条最高度
        per_w = (width-x0*2)//self.length # 矩形条宽度
        per_h = (height-80)//self.sortList.ymax
        _sleep = 100
        self.draw_source(x0,y0, per_w,per_h)
        animation = {}
        animation['bubble'] = self.bubbleSort
        animation['select'] = self.selectionSort
        self.update = animation[sort_func](per_w, _sleep).__next__
        self.update()

    def draw_source(self, x0,y0, per_w,per_h):
        '''绘制初始数组'''
        font = "time 10 bold underline"
        half_w = per_w//2
        for i in range(self.length):
            val = self.sortList.source[i]
            x = x0 + per_w*i; y = y0-val*per_h
            self.cvs.create_rectangle(x, y, x+per_w, y0,
                    width = 3, tags = f'r{i}', fill='white')
            self.cvs.create_text(x+half_w, y-half_w, font = font,
                    text = str(val), tags = f't{i}')

    def swap(self, left, right, distance):
        # 交换位置、文字、标签
        for t in ('r','t'):
            self.cvs.move(f'{t}{left}', distance,0)
            self.cvs.move(f'{t}{right}', -distance,0)
            self.cvs.itemconfig(f'{t}{left}', tags = f's{left}')
            self.cvs.itemconfig(f'{t}{right}', tags = f'{t}{left}')
            self.cvs.itemconfig(f's{left}', tags = f'{t}{right}')
    
    def bubbleSort(self, per_w, _sleep):
        '''冒泡排序'''
        for m,n,p in self.sortList.bubbleSort():
            # 修改矩形条颜色和交换位置
            self.cvs.itemconfig(f'r{n}', fill='red')
            self.cvs.itemconfig(f'r{n+1}', fill='green')
            if p: self.parent.after(_sleep, lambda: self.swap(n,n+1,per_w))
            self.parent.after(_sleep*2, self.update)
            yield
            self.cvs.itemconfig(f'r{n}', fill='white')
            self.cvs.itemconfig(f'r{n+1}', fill='white')
            if m == n+1: self.cvs.itemconfig(f'r{m}', fill='orange')
    
    def selectionSort(self, per_w, _sleep):
        '''选择排序'''
        it = 0
        for m,n,p in self.sortList.selectionSort():
            # 修改矩形条颜色和交换位置
            self.cvs.itemconfig(f'r{m}', fill='red')
            if p==0:
                if it < m: self.cvs.itemconfig(f'r{it}', fill='white')
                self.cvs.itemconfig(f'r{n}', fill='green')
                it = n
                self.parent.after(_sleep, self.update)
                yield
            elif p==2:
                self.cvs.itemconfig(f'r{n}', fill='gray')
                self.parent.after(_sleep, self.update)
                yield
                self.cvs.itemconfig(f'r{n}', fill='white')
            elif p==1:
                self.parent.after(_sleep, lambda: self.swap(m,n,per_w*(n-m)))
                self.parent.after(_sleep*2, self.update)
                yield
                # self.cvs.itemconfig(f'r{n}', fill='white')
                self.cvs.itemconfig(f'r{m}', fill='orange')


if __name__ == "__main__":
    w,h = 640,400
    win = tk.Tk()
    win.title("动画演示")
    win.geometry(f'{w}x{h}+250+150')
    win.resizable(False, False)

    SortAnimation(win, w, h, SortList(20,(1,80,3)), 'select')

    win.mainloop()