import tkinter as tk
from PIL import ImageTk, Image
import time, math

class Clock:
    '''
    时钟：
        1 手动校准
        2 动态指针
    '''
    tkimg = None

    def __init__(self, master, t = (0,0,0)):
        '''主框架'''
        self.master = master
        self.c = 250 # 边长一半，中心点
        self.cv = tk.Canvas(master, width=self.c*2, height=self.c*2, bg = 'white')
        self.cv.pack()

        try:
            self.t = [int(t[0])*5%60+int(t[1])//12, int(t[1]), int(t[2])]
        except:
            print('时间格式有误！')
            self.t = [0, 0, 0] # 当前时间，12进制

        # 绘制钟表
        self.draw_clock()
        self.pointer()
        self.draw_pointer()

    def draw_clock(self):
        # 绘制盘面
        clock_img = Image.open('./时钟.png').resize((400,400))
        # PhotoImage必须是全局对象。封装在函数内函数结束可能会消失导致图片不显示。
        self.tkimg = ImageTk.PhotoImage(clock_img)
        self.cv.create_image(self.c, self.c, image=self.tkimg) # 绘制盘面时间
        self.cv.create_oval(self.c-8,self.c-8,self.c+8,self.c+8, fill= 'gray') # 绘制圆心

        # 校准时间
        btn = tk.Button(self.cv, text ="校准时间", command = self.localtime)
        btn.place(x = self.c*0.87, y = self.c*1.8)

    def draw_pointer(self):
        '''绘制指针'''
        self.cv.delete('s')
        self.cv.delete('m')
        self.cv.delete('h')
        self.cv.create_line(self.c, self.c, *self.pt_data[0][self.t[2]], width = 2, tags ='s')
        self.cv.create_line(self.c, self.c, *self.pt_data[1][self.t[1]], width = 4, tags ='m')
        self.cv.create_line(self.c, self.c, *self.pt_data[2][self.t[0]], width = 6, tags ='h')
        self.master.after(1000, self.draw_pointer) # 每秒更新一次
        self.t[2] += 1
        self.t[2] %= 60
        if self.t[2] == 0:
            self.t[1] += 1
            self.t[1] %= 60
            if self.t[1]%12 == 0: # 每12分钟走1格
                self.t[0] += 1
                self.t[0] %= 60

    def pointer(self):
        '''计算指针长度'''
        R = (140, 90, 60) # 指针长度
        theta = [2*i*math.pi/60 for i in range(-15, 45)]
        theta2 = [(math.cos(i), math.sin(i)) for i in theta]
        self.pt_data = [[(self.c+round(r*th[0]), self.c+round(r*th[1])) \
                    for th in theta2] for r in R]

    def localtime(self, *arg):
        '''校准时间'''
        t = time.localtime()
        self.t[0] = t[3]%12*5%60+t[4]//12
        self.t[1] = t[4]
        self.t[2] = t[5]


if __name__ == '__main__':
    root = tk.Tk()
    Clock(root, (4,56,9))
    root.mainloop()
