import time
import tkinter as tk
import tkinter.colorchooser as colorchooser, \
        tkinter.filedialog as filedialog
from PIL import Image, ImageTk, ImageGrab

class Drawing:
    '''画板'''
    tool_icons = [] # 图标
    image = [None] # 图片

    def __init__(self, parent):
        width = 960
        height = 600
        tool_height = 60    # 工具栏高度

        # 主框架
        self.window = tk.Frame(parent)
        self.window.pack()

        # 工具栏
        self.tool_name = ['导入', '保存', '撤销', '清屏', '背景色', '画笔色', '填充', '虚线',
                    '铅笔', '马克笔', '直线', '矩形', '圆形', '椭圆形', '多边形', '文字']
        self.cell = width//len(self.tool_name) # 按钮宽度
        self.tools = tk.Canvas(self.window, width = width, height = tool_height, bg='white')
        self.toolBar(width, tool_height)
        self.tools.bind('<Button-1>', self.clickTool)
        self.tools.pack()

        # 画布
        self.drawing = tk.Canvas(self.window, height=height-tool_height, bg='white')
        self.drawing.bind('<Button-1>', self.onLeftDown)
        self.drawing.bind('<B1-Motion>', self.onLeftMove)
        self.drawing.bind('<ButtonRelease-1>', self.onLeftUp)
        self.drawing.pack(fill='x')

        # 画笔属性
        self.color = 'red' # 画笔颜色
        self.graph = '铅笔' # 画笔类型 '铅笔', '马克笔', '直线', '矩形', '圆形', '椭圆', '文字', '多边形'
        self.dotted = False # 是否虚线
        self.fill = True # 是否填充

        # 画笔轨迹记录
        self.on_canvas = False # 鼠标是否离开画布
        self.pts = [] # 记录所有点 自由线模式和多边形模式不同
        self.prev_pt = (0,0) # 前一个点
        self.objs = [] # 记录所有对象
        self.last_draw = ['铅笔',-1] # 上次对象

    def toolBar(self, width, height):
        '''工具栏 使用Canvas'''
        w = self.cell//2
        for i in range(len(self.tool_name)):
            name = self.tool_name[i]
            img = Image.open(f'icon/{name}.png').resize((w, w))
            self.tool_icons.append(ImageTk.PhotoImage(img))  # 按钮图标为全局变量
            w1 = w*(2*i+1); w2 = int(w*0.7)
            self.tools.create_rectangle(w1-w, w*2-w2, w1+w, height, tags=name, fill='', outline='')
            self.tools.create_image(w1, w2, image=self.tool_icons[i])
            self.tools.create_text(w1, w+w2, text=name)
        self.tools.itemconfig('背景色', fill='white')
        self.tools.itemconfig('画笔色', fill='red')
        self.tools.itemconfig('铅笔', fill='SkyBlue')
        self.tools.itemconfig('填充', fill='red')

    def clickTool(self, event):
        name = self.tool_name[event.x//self.cell]
        
        if name=='导入':
            filename = filedialog.askopenfilename(title='导入图片',
                            filetypes=[('image', '*.jpg *.png')])
            if filename:
                img = Image.open(filename).resize((960, 600))
                self.image[0] = ImageTk.PhotoImage(img)
                self.drawing.create_image(480, 300, image=self.image[0])
        elif name=='保存':
            filename = filedialog.asksaveasfilename(filetypes=[('.jpg', 'JPG')])
            ImageGrab.grab().save(filename+'.jpg')
        elif name=='清屏':
            self.drawing.delete('all')
        elif name=='撤销':
            self.last_draw = [self.graph,-1]
            self.pts = []
            if self.objs:
                self.drawing.delete(self.objs.pop()[1])
        elif name=='背景色':
            color = colorchooser.askcolor()[1]
            self.drawing['bg'] = color
            self.tools.itemconfig('背景色', fill=color)
        elif name=='画笔色':
            color = colorchooser.askcolor()[1]
            self.color = color
            self.tools.itemconfig('画笔色', fill=color)
            if self.fill:
                self.tools.itemconfig('填充', fill=self.color)
        elif name=='虚线':
            if self.dotted:
                self.tools.itemconfig('虚线', fill='')
            else:
                self.tools.itemconfig('虚线', fill='SeaGreen')
            self.dotted = not self.dotted
        elif name=='填充':
            if self.fill:
                self.tools.itemconfig('填充', fill='')
            else:
                self.tools.itemconfig('填充', fill=self.color)
            self.fill = not self.fill
        elif name in ('铅笔', '马克笔', '直线', '矩形', '圆形', '椭圆形', '多边形', '文字'):
            # 设置画笔
            self.last_draw = [name,-1]
            if self.graph != name:
                self.tools.itemconfig(self.graph, fill='')
                self.tools.itemconfig(name, fill='SkyBlue')
                self.graph = name
            if name == '多边形':
                self.pts = []

    def onLeftDown(self, event):
        self.on_canvas = True
        self.prev_pt = event.x, event.y
        if self.graph == '文字':
            self.draw_text(event)
        elif self.graph in ('铅笔','马克笔'):
            self.pts = [event.x, event.y]

    def onLeftMove(self, event):
        if not self.on_canvas:
            return
        lx,ly = self.prev_pt; x,y = event.x, event.y
        colors = {'outline':self.color, 'fill':['',self.color][self.fill]}
        self.drawing.delete(self.last_draw[1])
        if self.graph == '铅笔':
            self.pts += [x,y]
            draw = self.drawing.create_line(*self.pts, fill=self.color, width=2,
                        dash=[tuple(), (2,2)][self.dotted])
        elif self.graph == '马克笔':
            self.pts += [x,y]
            draw = self.drawing.create_line(*self.pts, fill=self.color, width=6,
                        dash=[tuple(), (12,12)][self.dotted])
        elif self.graph == '直线':
            draw = self.drawing.create_line(lx,ly,x,y, fill=self.color, width=2,
                        dash=[tuple(), (2,2)][self.dotted])
        elif self.graph == '矩形':
            draw = self.drawing.create_rectangle(lx,ly,x,y, **colors, width=2,
                        dash=[tuple(), (2,2)][self.dotted])
        elif self.graph == '椭圆形':
            draw = self.drawing.create_oval(lx,ly,x,y, **colors, width=2,
                        dash=[tuple(), (2,2)][self.dotted])
        elif self.graph == '圆形':
            y = x-lx+ly # 重新设定x,y
            draw = self.drawing.create_oval(lx,ly,x,y, **colors, width=2,
                        dash=[tuple(), (2,2)][self.dotted])
        else:
            return
            # 多边形 在 onLeftDown 实现
            # 文字 在 onLeftUp 实现
        self.last_draw[1] = draw

    def onLeftUp(self, event):
        if self.graph != '多边形':
            self.objs.append(self.last_draw) # 抬笔后添加
            self.last_draw = ['多边形',-1]
            if self.graph in ('铅笔','马克笔'):
                self.pts = []
        else:
            self.pts.append((event.x,event.y))
            self.draw_poly()

    def draw_poly(self):
        '''绘制多边形'''
        self.drawing.delete(self.last_draw[1])
        if self.last_draw[0] == '多边形' and self.last_draw[1] != -1:
            if self.objs:
                self.objs.remove(self.last_draw)
        colors = {'outline':self.color, 'fill':['',self.color][self.fill],
                'dash':[tuple(), (2,2)][self.dotted], 'width':2,}
        self.last_draw = ['多边形', self.drawing.create_polygon(*self.pts, **colors)]
        self.objs.append(self.last_draw)
        

    def draw_text(self, event):
        '''弹出文字设置框'''
        win = tk.Toplevel(self.drawing)
        paddict = {'padx':20, 'pady':5}
        l1 = tk.Label(win, text='请输入文本:').grid(row=0, column=0, **paddict)
        l2 = tk.Label(win, text='请输入大小:').grid(row=1, column=0, **paddict)
        t1 = tk.StringVar(); t1.set('文本')
        t2 = tk.IntVar(); t2.set(10)
        tk.Entry(win, textvariable=t1).grid(row=0, column=1, **paddict)
        tk.Entry(win, textvariable=t2).grid(row=1, column=1, **paddict)
        def get_size():
            if t1.get() and t2.get():
                draw = self.drawing.create_text(event.x, event.y, font=("等线", t2.get()),
                        text=t1.get(), fill=self.color)
                self.objs.append(['文字', draw])
                win.destroy()
        tk.Button(win, text='确定', command=get_size).grid(row=3, column=0,
                        columnspan=2, **paddict)


if __name__ == '__main__':
    app = tk.Tk()
    app.title('tkiner画板')
    app.resizable(0,0)
    Drawing(app)
    app.mainloop()
