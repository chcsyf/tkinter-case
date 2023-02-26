import tkinter as tk
import tkinter.colorchooser as colorchooser, \
        tkinter.filedialog as filedialog, \
        tkinter.messagebox as messagebox

class MainFrame:
    """游戏主框架"""
    def __init__(self):
        # 属性
        self.cell = 25
        self.width = 20*self.cell
        self.mode = '规则'
        self.board_mode = ''
        self.color = 'white'

        # 主窗口、菜单、棋盘框架、信息框架
        self.main_win = tk.Tk()
        self.main_win.resizable(0,0)
        self.menubar = tk.Menu(self.main_win)
        self.board_frame = tk.Frame(self.main_win)
        self.info_frame = tk.Frame(self.main_win, width = self.width//2, bg='whitesmoke')
        self.main_win['menu'] = self.menubar
        self.board_frame.pack(side='left')
        self.info_frame.pack(side='left', fill='y')

        self.board_win()
        self.info_win()
        self.menu_win()
        self.main_win.mainloop()

    def board_win(self):
        '''棋盘框架'''
        # 工具栏
        self.board_tool = tk.Frame(self.board_frame, width = self.width, height = 2*self.cell)
        self.board_tool.pack()
        # 信息栏
        self.board_info = tk.Canvas(self.board_frame, height = 2*self.cell)
        self.board_info.pack(fill='x')
        # 面板栏
        self.board_panel = tk.Canvas(self.board_frame, height = self.width)
        self.board_panel.pack(fill='x')
        self.board_panel.bind('<Button-1>', self.redraw_board)
        # 状态栏
        self.board_status = tk.Label(self.board_frame)
        self.board_status.pack(fill='x')

    def info_win(self):
        '''信息框架'''
        win = self.info_frame
        pads = {'padx':10, 'pady':7}
        font = ('微软雅黑', 10)

        # 基本参数
        self.board_data = {'size':[None,None], 'ids':None, 'color':None}
        self.chess_data = {'num':0, 'name':None, 'road':None, 'pts':None}

        if self.mode == '规则':
            # 棋盘设置
            tk.Label(win, text='棋盘设置:', font=font, bg='orange').grid(row=0, column=0, **pads)
            tk.Label(win, text='棋盘大小:', font=font).grid(row=1, column=0, **pads)
            tk.Label(win, text='宽:', font=font).grid(row=1, column=1, **pads)
            tk.Label(win, text='高:', font=font).grid(row=1, column=3, **pads)
            t1 = tk.StringVar(); t2 = tk.StringVar()
            et1 = tk.Entry(win, textvariable=t1, font=font, width=3)
            et2 = tk.Entry(win, textvariable=t2, font=font, width=3)
            et1.grid(row=1, column=2, **pads)
            et2.grid(row=1, column=4, **pads)
            tk.Button(win, text='确定', font=font, command=lambda: self.draw_board(et1, et2)
                        ).grid(row=1, column=5, **pads)
            tk.Label(win, text='棋盘修改:', font=font).grid(row=2, column=0, **pads)
            def board_mode(mode):
                if self.board_mode == mode:
                    self.board_mode = ''
                else:
                    self.board_mode = mode
                    if mode == '填色':
                        self.color = colorchooser.askcolor()[1]
            tk.Button(win, text='删除格子', font=font, command=lambda: board_mode('删除')
                        ).grid(row=2, column=1, columnspan=2, **pads)
            tk.Button(win, text='填充颜色', font=font, command=lambda: board_mode('填色')
                        ).grid(row=2, column=3, columnspan=2, **pads)

            # 棋子设置
            tk.Label(win, text='棋子设置:', font=font, bg='orange').grid(row=3, column=0, **pads)
            tk.Label(win, text='棋子种类:', font=font).grid(row=4, column=0, **pads)
            tk.Label(win, text='种', font=font).grid(row=4, column=3, **pads)
            t3 = tk.IntVar(); t3.set(2)
            tk.Entry(win, textvariable=t3, font=font, width=3).grid(row=4, column=2, **pads)
            tk.Label(win, text='特征区分:', font=font).grid(row=5, column=0, **pads)
            tk.Label(win, text='棋子名称:', font=font).grid(row=6, column=0, **pads) # 下拉设置 横竖斜 h,v,x 0-6
            names = ['黑棋', '白棋']
            spin1 = tk.Spinbox(win, values=names, width=8, command=lambda: ... )
            spin1.grid(row=6, column=1, columnspan=2, **pads)
            names = ['黑棋', '白棋']
            tk.Label(win, text='行棋路线:', font=font).grid(row=7, column=0, **pads) # 下拉设置 横竖斜 h,v,x 0-6
            spin2 = tk.Spinbox(win, values=names, width=8, command=lambda: ...)
            spin2.grid(row=7, column=1, columnspan=2, **pads)
            tk.Label(win, text='吃子规则:', font=font).grid(row=8, column=0, **pads) # 下拉设置 输入序号 -1-n
            spin3 = tk.Spinbox(win, values=names, width=8, command=lambda: ...)
            spin3.grid(row=8, column=1, columnspan=2, **pads)
            tk.Label(win, text='默认布局:', font=font).grid(row=9, column=0, **pads) # 下拉设置，点击放置
            spin4 = tk.Spinbox(win, values=names, width=8, command=lambda: ...)
            spin4.grid(row=9, column=1, columnspan=2, **pads)

            t4 = tk.IntVar(); t4.set(1)
            tk.Radiobutton(win, text='名称', variable=t4, value=1, command=lambda:
                self.return_chess(spin1,spin2,spin3,spin4)).grid(row=5, column=1, columnspan=2, **pads)
            tk.Radiobutton(win, text='颜色', variable=t4, value=2, command=lambda:
                self.return_chess(spin1,spin2,spin3,spin4)).grid(row=5, column=3, columnspan=2, **pads)

            # 行棋方式
            tk.Label(win, text='行棋方式:', font=font, bg='orange').grid(row=10, column=0, **pads)
            tk.Label(win, text='放置:', font=font).grid(row=11, column=0, **pads) # 是否吃子
            tk.Label(win, text='删除:', font=font).grid(row=12, column=0, **pads) # 是否吃子
            tk.Label(win, text='移动:', font=font).grid(row=13, column=0, **pads) # 是否吃子
            tk.Label(win, text='跳跃:', font=font).grid(row=14, column=0, **pads) # 是否吃子


    def draw_board(self, *ids):
        '''绘制棋盘'''
        for i in range(2):
            _id = ids[i]
            if _id.get().isdigit() and 3<=int(_id.get())<=49:
                _id['bg'] = 'orange'
                self.board_data['size'][i] = int(_id.get())
            else:
                _id['bg'] = 'white'
                self.board_data['size'][i] = None
        a,b = self.board_data['size'][0],self.board_data['size'][1]
        if a is not None and b is not None:
            self.board_panel.delete('all')
            x = int(self.width/(a+2)); y = int(self.width/(b+2))
            self.board_data['ids'] = [None]*a
            for i in range(a):
                self.board_data['ids'][i] = [None]*b
                for j in range(b):
                    self.board_data['ids'][i][j] = self.board_panel.create_rectangle(
                            (i+1)*x, (j+1)*y, (i+2)*x, (j+2)*y)

    def redraw_board(self, event):
        '''修改棋盘'''
        a,b = self.board_data['size'][0],self.board_data['size'][1]
        if a is not None and b is not None:
            x = int(event.x/int(self.width/(a+2)))-1
            y = int(event.y/int(self.width/(b+2)))-1
            if self.board_mode == '删除':
                self.board_panel.delete(self.board_data['ids'][x][y])
            elif self.board_mode == '填色':
                self.board_panel.itemconfig(self.board_data['ids'][x][y], fill=self.color)

    def return_chess(self,  *ids):
        '''调整棋子'''
        l = len(ids)
        for i in range(l):
            ids[i]['values'] = [f'棋子{j+1}' for j in range(l)]

    def menu_win(self):
        '''菜单框架'''
        # 规则
        menus1 = [self.rule_open, self.rule_save, self.rule_saveas]
        menusn1 = ("加载规则","保存规则","规则另存为")
        rulesmenu = tk.Menu(self.menubar, tearoff=False)
        for i in range(len(menus1)):
            rulesmenu.add_command(label=menusn1[i], command=menus1[i])
        self.menubar.add_cascade(label="规则", menu=rulesmenu)
        # 对局
        menus2 = [self.chess_new, self.chess_open, self.chess_save, self.chess_saveas]
        menusn2 = ("新建对局","打开棋谱","保存棋谱","棋谱另存为")
        chessmenu = tk.Menu(self.menubar, tearoff=False)
        for i in range(len(menus2)):
            chessmenu.add_command(label=menusn2[i], command=menus2[i])
        self.menubar.add_cascade(label="对局", menu=chessmenu)

    def rule_new(self):
        '''新建规则'''
        pass

    def rule_open(self):
        '''新建规则'''
        pass

    def rule_save(self):
        '''新建规则'''
        pass

    def rule_saveas(self):
        '''新建规则'''
        pass

    def chess_new(self):
        '''新建规则'''
        pass

    def chess_open(self):
        '''新建规则'''
        pass

    def chess_save(self):
        '''新建规则'''
        pass

    def chess_saveas(self):
        '''新建规则'''
        pass

if __name__ == '__main__':
    win = MainFrame()
