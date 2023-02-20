import tkinter as tk
import tkinter.colorchooser as colorchooser, \
        tkinter.filedialog as filedialog, \
        tkinter.messagebox as messagebox
from PIL import Image, ImageTk, ImageGrab
import json


class OppositeGobang:
    """反五子棋游戏。五子连珠为输"""
    def __init__(self):
        # 棋盘 15x15, 状态：无子、黑子、白子
        self.data = [[0]*15 for i in range(15)]
        self.move_pts = []      # 可移动到的位置
        self.move_origin = None # 移动的原点

    def go(self, player:1|2, pt:tuple[int]) -> 0|1|2|3|4:
        ''' 落子和输赢判断
            落子方式：
                1 直接落子，只需要点击一个位置
                2 落子并移动对方棋子，需要点击两个位置。
            
            输入：player：黑(1)、白(2)
                  pt：落子位置(0-15, 0-15)
            返回：0：落子成功但未五子连珠，1|2：落子成功player输，
                  3：落子失败，4：移动状态
        '''
        opponent = 1 if player ==2 else 2

        if self[pt] == player:
            # 不允许移动己方棋子
            return 3
        elif self[pt] == opponent:
            # 移动对方棋子
            self.moveable_pts(pt) # 生成可移动位置
            if self.move_pts == []:
                return 3 # 这个棋子不可移动
            self.move_origin = pt
            return 4
        else:
            if self.move_pts == []:
                # 非移动状态
                self[pt] = player
                return self.isLose(player, pt)
            else:
                # 移动状态
                if pt in self.move_pts:
                    self[self.move_origin] = player
                    self[pt] = opponent
                    self.move_pts = []
                    # 判断输赢
                    re = self.isLose(player, self.move_origin)
                    if re:
                        return re
                    else:
                        return self.isLose(opponent, pt)
                else:
                    return 3

    def moveable_pts(self, pt:tuple[int]):
        '''可以移动 的位置'''
        self.move_pts = []
        r,c = pt

        # 行
        r1 = r-1; r2 = r+1
        while r1 >= 0 and self[r1,c] == 0:
            self.move_pts.append((r1,c))
            r1 -= 1
        while r2 < 15 and self[r2,c] == 0:
            self.move_pts.append((r2,c))
            r2 += 1
        # 列
        c1 = c-1; c2 = c+1
        while c1 >= 0 and self[r,c1] == 0:
            self.move_pts.append((r,c1))
            c1 -= 1
        while c2 < 15 and self[r,c2] == 0:
            self.move_pts.append((r,c2))
            c2 += 1
        # 主斜
        r1 = r-1; r2 = r+1; c1 = c-1; c2 = c+1
        while r1 >= 0 and c1 >= 0 and self[r1,c1] == 0:
            self.move_pts.append((r1,c1))
            r1 -= 1; c1 -= 1
        while r2 < 15 and c2 < 15 and self[r2,c2] == 0:
            self.move_pts.append((r2,c2))
            r2 += 1; c2 += 1
        # 反斜
        r1 = r-1; r2 = r+1; c1 = c+1; c2 = c-1 # 注意c
        while r1 >= 0 and c1 < 15 and self[r1,c1] == 0:
            self.move_pts.append((r1,c1))
            r1 -= 1; c1 += 1
        while r2 < 15 and c2 >= 0 and self[r2,c2] == 0:
            self.move_pts.append((r2,c2))
            r2 += 1; c2 -= 1

    def isLose(self, player:1|2, pt:tuple[int]) -> 0|1|2:
        ''' 输赢判断
            输入：player：黑(1)、白(2)
                  pt：落子位置(0-15, 0-15)
            返回：0：未五子连珠，1|2：player输'''
        r,c = pt

        # 行
        num = 0; r1 = r; r2 = r+1
        while r1 >= 0 and self[r1,c] == player:
            num += 1; r1 -= 1
        while r2 < 15 and self[r2,c] == player:
            num += 1; r2 += 1
        if num >= 5: return player,(r1+1,c,r2-1,c)
        # 列
        num = 0; c1 = c; c2 = c+1
        while c1 >= 0 and self[r,c1] == player:
            num += 1; c1 -= 1
        while c2 < 15 and self[r,c2] == player:
            num += 1; c2 += 1
        if num >= 5: return player,(r,c1+1,r,c2-1)
        # 斜1
        num = 0; r1 = r; r2 = r+1; c1 = c; c2 = c+1
        while r1 >= 0 and c1 >= 0 and self[r1,c1] == player:
            num += 1; r1 -= 1; c1 -= 1
        while r2 < 15 and c2 < 15 and self[r2,c2] == player:
            num += 1; r2 += 1; c2 += 1
        if num >= 5: return player,(r1+1,c1+1,r2-1,c2-1)
        # 斜2
        num = 0; r1 = r; r2 = r+1; c1 = c; c2 = c-1 # 注意c2
        while r1 >= 0 and c1 < 15 and self[r1,c1] == player:
            num += 1; r1 -= 1; c1 += 1
        while r2 < 15 and c2 >= 0 and self[r2,c2] == player:
            num += 1; r2 += 1; c2 -= 1
        if num >= 5: return player,(r1+1,c1-1,r2-1,c2+1)

        return 0

    def __getitem__(self, it:tuple[int]):
        return self.data[it[0]][it[1]]

    def __setitem__(self, it:tuple[int], value:int):
        self.data[it[0]][it[1]] = value

class OppositeGobangUI:
    """反五子棋游戏UI"""
    tool_icons = [] # 图标

    def __init__(self, parent):
        self.cell = 30          # 每个方块大小

        # 游戏数据
        self.gobang = OppositeGobang()  # 棋盘数据
        self.player = 1         # 初始棋手为黑棋
        self.moveing = False    # 移动棋子状态
        self.mode = '单机'      # 游戏模式
        self.ui_oval = [[None]*15 for i in range(15)] # 记录落子情况
        self.order = []         # 记录落子顺序
        self.order_id = []      # 记录打谱顺序
        self.index = 0          # 当前步数

        # 主框架
        self.window = tk.Frame(parent)
        self.window.pack()
        width = (14+1.5+1.5)*self.cell

        # 工具栏
        self.tools = tk.Canvas(self.window, width = width, height = self.cell*1.5)
        self.tool_bar(width)
        self.tools.bind('<Button-1>', self.click_tool)
        self.tools.pack()

        # 画布
        self.canvas = tk.Canvas(self.window, width=width, height=width)
        self.board(width)
        self.canvas.bind("<Button-1>", self.call_alone)
        self.canvas.bind("<MouseWheel>", self.wheel_record)
        self.canvas.pack()

        # 历史记录
        self.record = tk.Canvas(self.window, height = self.cell*2.5)
        self.record.bind('<Button-1>', self.click_record)
        self.record.bind("<B1-Motion>", self.scroll_move)
        self.record.pack(fill='x')

    def tool_bar(self, width):
        '''工具栏 使用Canvas'''
        w = width//8; y1 = self.cell//2; y2 = self.cell*1.2

        for i in range(7):
            name = ('打开', '保存', '单机', '网络', '打谱', '说明', '悔棋')[i]
            size = (int(self.cell*0.9), int(self.cell*0.8))
            img = Image.open(f'icon/{name}.png').resize(size)
            self.tool_icons.append(ImageTk.PhotoImage(img))  # 按钮图标为全局变量
            x = w*(i+1); x2 = w//3
            self.tools.create_image(x, y1, image=self.tool_icons[i])
            self.tools.create_rectangle(x-x2, self.cell*0.9, x+x2, self.cell*1.5,
                        tags=name, fill='', outline='')
            self.tools.create_text(x, y2, text=name)
        # 默认为单机模式
        self.tools.itemconfig('单机', fill='orange')

    def board(self, length):
        '''绘制棋盘UI'''
        # 格线、坐标
        pt0 = 1.5*self.cell
        for i in range(15):
            self.canvas.create_line(pt0, pt0+i*self.cell, length-pt0,
                        pt0+i*self.cell, width=1)
            self.canvas.create_text(self.cell, pt0+i*self.cell, text=f'{15-i}')
            self.canvas.create_line(pt0+i*self.cell, pt0, pt0+i*self.cell,
                        length-pt0, width=1)
            self.canvas.create_text(pt0+i*self.cell, length-self.cell,
                        text=f'{chr(65+i)}')
        # 星位
        pt1 = length/2; pt2 = (3+1.5)*self.cell; r = 2
        self.canvas.create_oval(pt1-r,pt1-r,pt1+r,pt1+r, fill='black')
        self.canvas.create_oval(pt2-r,pt2-r,pt2+r,pt2+r, fill='black')
        self.canvas.create_oval(pt2-r,length-pt2-r,pt2+r,length-pt2+r, fill='black')
        self.canvas.create_oval(length-pt2-r,pt2-r,length-pt2+r,pt2+r, fill='black')
        self.canvas.create_oval(length-pt2-r, length-pt2-r, length-pt2+r,
                    length-pt2+r, fill='black')
        # 棋子、玩家
        y = self.cell*0.75; r =10
        self.canvas.create_text(3*self.cell, y, font=('微软雅黑',12),
                    text='玩家1', tags='player1')
        self.canvas.create_text(13*self.cell, y, font=('微软雅黑',12),
                    text='玩家2', tags='player2')
        x1 = 4.5*self.cell; x2 = 14.5*self.cell
        self.canvas.create_oval(x1-r, y-r, x1+r, y+r, fill='black')
        self.canvas.create_oval(x2-r, y-r, x2+r, y+r, fill='white')

    def click_tool(self, event):
        '''菜单'''
        x = int(event.x/self.cell-1.25)//2  # 换算棋盘坐标
        name = ('打开', '保存', '单机', '网络', '打谱', '说明', '悔棋')[x]
        if name == '打开':
            self.open()
        elif name == '保存':
            self.save()
        elif name in ('单机', '网络', '打谱'):
            self.new_game(name)
        elif name == '说明':
            text = '反五子棋游戏。\n 1 五子连珠的一方 输！\n 2 黑棋先行，交替落子。\n'\
                ' 3 可以在空白处落子。\n 4 点击对方棋子移动到目标点，并在原位置落子。'
            messagebox.showinfo(title='游戏规则', message = text)
        elif name == '悔棋':
            if self.mode in ('单机', '打谱'):
                if not self.order:
                    return
                self.canvas.delete('last')
                self.canvas.delete('aims')
                info = self.order.pop()
                if len(info) == 3:
                    _id = self.ui_oval[info[0]][info[1]].pop()
                    self.canvas.delete(_id)
                    self.player = info[-1]
                    self.gobang[info[0], info[1]] = 0
                else:
                    id1 = self.ui_oval[info[0]][info[1]].pop()
                    id2 = self.ui_oval[info[3]][info[4]].pop()
                    self.canvas.delete(id1)
                    self.canvas.delete(id2)
                    self.player = info[-1]
                    self.gobang[info[0], info[1]] = self.player
                    self.gobang[info[3], info[4]] = 0
                ids = self.order_id.pop()
                for i in ids:
                    self.record.delete(i)

    def new_game(self, name, msg = True):
        self.tools.itemconfig(self.mode, fill='')
        self.tools.itemconfig(name, fill='orange')
        self.canvas.unbind("<Button-1>")
        self.record.delete('all')
        self.canvas.delete('go')
        self.canvas.delete('last')
        self.canvas.delete('aims')
        call_mode = {'单机': self.call_alone,
                    '网络': self.call_online,
                    '打谱': self.call_record}
        self.canvas.bind("<Button-1>", call_mode[name])
        if msg:
            p = messagebox.askquestion(title='新游戏', message='是否保存当前游戏数据?')
            if p == 'yes':
                self.save()
        # 初始化游戏
        self.mode = name        # 游戏模式
        self.ui_oval = [[None]*15 for i in range(15)] # 记录落子情况
        self.order = []         # 记录落子顺序
        self.order_id = []
        self.player = 1         # 初始棋手为黑棋
        self.moveing = False    # 移动棋子状态
        if name == '单机':
            self.gobang = OppositeGobang()  # 棋盘数据
        elif name == '打谱':
            self.gobang = OppositeGobang()  # 棋盘数据
        elif name == '网络':
            messagebox.showinfo(title='在线对弈', message = '在线对弈未开通')

    def save(self):
        '''保存棋谱'''
        win = tk.Toplevel(self.canvas)
        paddict = {'padx':20, 'pady':5}
        l1 = tk.Label(win, text='棋手(黑)姓名:').grid(row=0, column=0, **paddict)
        l2 = tk.Label(win, text='棋手(白)姓名:').grid(row=1, column=0, **paddict)
        t1 = tk.StringVar(); t1.set('')
        t2 = tk.StringVar(); t2.set('')
        tk.Entry(win, textvariable=t1).grid(row=0, column=1, **paddict)
        tk.Entry(win, textvariable=t2).grid(row=1, column=1, **paddict)
        def get_name():
            filename = filedialog.asksaveasfilename(filetypes=[('json', '*.json')])
            data = {'player':[t1.get(), t2.get()], 'data':self.order}
            with open(f'{filename}.json', 'w') as fp:
                json.dump(data, fp, ensure_ascii = False)
            win.destroy()
        tk.Button(win, text='确定', command=get_name).grid(row=3, column=0, columnspan=2, **paddict)

    def open(self):
        '''读取棋谱'''
        self.new_game('打谱')
        filename = filedialog.askopenfilename(title='读取棋谱',
                        filetypes=[('json', '*.json')])
        if not filename:
            return
        with open(filename, 'r') as f:
            data = json.load(f)
        if 'player' not in data or 'data' not in data or not data['data']:
            return
        self.canvas.itemconfig('player1', text=data['player'][0])
        self.canvas.itemconfig('player2', text=data['player'][1])
        self.draw_go(data['data'])

    def call_alone(self, event):
        '''单机模式落子 player：黑(1)、白(2)'''
        x = event.x//self.cell-1  # 换算棋盘坐标
        y = event.y//self.cell-1

        # 落子
        if x<0 or x>14 or y<0 or y>14:
            return
        re = self.gobang.go(self.player, (x,y))
        pt_color = ('orange', 'red', 'green') # 标识颜色
        if re == 3:
            # 不可落子
            return 
        elif re == 4:
            # 移动棋子状态
            self.canvas.delete('last')
            self.canvas.delete('aims')
            for x,y in self.gobang.move_pts:
                dx = (x+1.5)*self.cell; dy = (y+1.5)*self.cell; r2 = 6
                self.canvas.create_oval(dx-r2,dy-r2,dx+r2,dy+r2, fill=pt_color[0],
                        outline='', tags='aims')
            self.moveing = True
            return

        # 绘制棋子
        opponent = 1 if self.player ==2 else 2
        if self.moveing:
            self.put(opponent, (x,y), pt_color[2])
            self.put(self.player, self.gobang.move_origin, pt_color[1])
            self.order.append((x,y, opponent, *self.gobang.move_origin, self.player))
            self.moveing = False
        else:
            self.put(self.player, (x,y), pt_color[1])
            self.order.append((x,y, self.player))
        self.draw_record(self.order[-1])
        self.player = opponent
        self.index += 1

        # 判断胜负
        if isinstance(re,tuple):
            pt = [(i+1.5)*self.cell for i in re[1]]
            self.canvas.create_line(*pt, fill='red',width=2, tags='last')
            if self.mode == '单机':
                self.canvas.unbind("<Button-1>")
                player = '黑方' if re[0] == 2 else '白方'
                messagebox.showinfo(title='游戏结束', message = f'{player}获胜！')

        return self.player

    def put(self, player, pt, color):
        '''落子'''
        self.canvas.delete('last')
        self.canvas.delete('aims')
        colors = ('black', 'white') # 棋子颜色
        r = 12; r2 = 6 # 棋子半径、标识半径
        px = (pt[0]+1.5)*self.cell; py = (pt[1]+1.5)*self.cell
        _id = self.canvas.create_oval(px-r,py-r,px+r,py+r, fill=colors[player-1], tags='go')
        if self.ui_oval[pt[0]][pt[1]] is None:
            self.ui_oval[pt[0]][pt[1]] = []
        self.ui_oval[pt[0]][pt[1]].append(_id); 
        self.canvas.create_oval(px-r2,py-r2,px+r2,py+r2, fill=color,
                    outline='', tags='last')

    def call_record(self, event):
        '''打谱模式'''
        self.call_alone(event)

    def draw_record(self, pt):
        '''绘制历史图'''
        colors = ('black', 'white') # 棋子颜色
        self.record.delete('last')
        r = 8; r2 = 4 # 棋子半径、标识半径
        n = len(self.order_id)
        px = int((n+1.5)*self.cell); py = self.cell//2
        id1 = self.record.create_line(px-self.cell+r,py, px-r,py)
        id2 = self.record.create_oval(px-r,py-r,px+r,py+r, fill=colors[pt[-1]-1])
        s = '(移)' if len(pt) == 6 else ''
        id3 = self.record.create_text(px,py+r*2, text=f'{n+1}{s}')
        self.record.create_oval(px-r2,py-r2,px+r2,py+r2, fill='red',
                    outline='', tags='last')
        self.order_id.append((id1, id2, id3))

    def scroll_move(self, event):
        self.record.scan_dragto(event.x, self.cell//2, gain=1)

    def click_record(self, event):
        '''历史记录'''        
        self.record.scan_mark(event.x, self.cell//2)
        # print(event.x)
        # if self.mode != '打谱':
        #     return
        # _id = self.record.find_closest(event.x, event.y)
        # for i in range(len(self.order_id)):
        #     if _id[0] == self.order_id[i]:
        #         order_data = self.order[:i+1]
        #         self.new_game('打谱', False)
        #         self.draw_go(order_data)
        #         return

    def draw_go(self, order_data):
        '''绘制棋局'''
        pt_color = ('orange', 'red', 'green') # 标识颜色
        for pt in order_data:
            if len(pt) == 3:
                self.gobang[pt[0], pt[1]] = pt[2]
                self.put(pt[2], (pt[0], pt[1]), pt_color[1])
                self.draw_record(pt)
            elif len(pt) == 6:
                self.gobang[pt[0], pt[1]] = pt[2]
                self.gobang[pt[3], pt[4]] = pt[5]
                self.put(pt[2], (pt[0], pt[1]), pt_color[1])
                self.put(pt[5], (pt[3], pt[4]), pt_color[1])
                self.draw_record(pt)
        self.order = order_data
        self.player = 1 if order_data[-1][-1] == 2 else 2

    def call_online(self, event):
        '''在线模式'''
        pass

    def wheel_record(self, event):
        '''滚动中键'''
        print(event.delta)
        pass

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('+300+50')
    root.title('反五子棋')
    root.resizable(0,0)
    gb = OppositeGobangUI(root)
    tk.mainloop()

'''
下期预告：
1 打谱 中键前进倒退预览，当前位置红点，落子切换，备注，添加分支，索引跳转
2 对弈 计时
3 网络对弈
'''