import tkinter as tk
import tkinter.filedialog as filedialog, \
        tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import json
from imgs import icon_imgs
import socket, struct, random, threading


class OppositeGobangUI:
    """反五子棋游戏UI"""
    tool_icons = [] # 图标

    def __init__(self, parent):
        self.cell = 30          # 每个方块大小

        # 游戏状态
        self.gobang = None  # 棋盘数据
        self.player = 1                 # 初始棋手为黑棋
        self.moveing = False            # 移动棋子状态
        self.mode = '单机'              # 游戏模式
        self.puting = False             # 放置模式

        # 游戏数据 每一步对应一个棋子、坐标、历史图信息，分支-步数加后缀，元组
        self.step = (0,0)           # 当前步数
        self.piece = {0:[]}         # 记录棋子
        self.record = {0:[]}        # 记录坐标
        self.record_id = {0:[]}     # 记录历史图
        self.time = [1200, 1200]    # 计时

        # 主框架
        win_main = tk.Frame(parent)
        win_main.grid(row=0, column=0)
        win_info = tk.PanedWindow(parent, orient=tk.VERTICAL, sashrelief='sunken',
                    width=self.cell*12)
        win_info.grid(row=0, column=1, padx=10)
        width = (14+2)*self.cell

        # 工具栏
        self.tools = tk.Canvas(win_main, width = width, height=self.cell*1.5)
        self.toolbar(width)
        self.tools.bind('<Button-1>', self.click_tool)
        self.tools.pack()

        # 画布
        self.canvas = tk.Canvas(win_main, height = width)
        self.board()
        self.canvas.bind("<Button-1>", self.call_alone)
        self.canvas.pack(fill='x')

        # 信息框
        tk.Frame(parent) 
        self.info_win = tk.Canvas(win_info, height= self.cell*3, bg='whitesmoke')
        self.information(self.info_win)
        win_info.add(self.info_win)

        # 聊天框
        chat_win = tk.Text(win_info, height = 10)
        win_info.add(chat_win)

        # 注释框
        notes_win = tk.Text(win_info, height = 10)
        win_info.add(notes_win)

        # 历史框
        self.record_win = tk.Canvas(win_info, height = self.cell*4, bg='whitesmoke')
        win_info.add(self.record_win)
        self.record_pt = (0,0) # 定位

    def toolbar(self, width):
        '''工具栏 使用Canvas'''
        w = width//8; y1 = self.cell//2; y2 = self.cell*1.2

        for i in range(7):
            name = ('打开', '保存', '单机', '网络', '打谱', '说明', '悔棋')[i]
            img = Image.fromarray(icon_imgs[i])             # numpy数组转PIL图像对象
            self.tool_icons.append(ImageTk.PhotoImage(img)) # 按钮图标为全局变量
            x = w*(i+1); x2 = w//3
            self.tools.create_image(x, y1, image=self.tool_icons[i])
            self.tools.create_rectangle(x-x2, self.cell*0.9, x+x2, self.cell*1.5,
                        tags=name, fill='', outline='')
            self.tools.create_text(x, y2, text = name)
        # 默认为单机模式
        self.tools.itemconfig('单机', fill='orange')

    def board(self):
        '''绘制棋盘UI'''
        # 格线、坐标
        ptx = int(1.5*self.cell); pty = self.cell
        for i in range(15):
            self.canvas.create_line(ptx, pty+i*self.cell, ptx+14*self.cell,
                        pty+i*self.cell, width=1)
            self.canvas.create_text(self.cell, pty+i*self.cell, text=f'{15-i}')
            self.canvas.create_line(ptx+i*self.cell, pty, ptx+i*self.cell,
                        pty+14*self.cell, width=1)
            self.canvas.create_text(ptx+i*self.cell, pty+14.5*self.cell,
                        text=f'{chr(65+i)}')
        # 星位
        ns = (2,7,12) ; r = 3
        for x in ns:
            for y in ns:
                px = ptx+x*self.cell; py = pty+y*self.cell
                self.canvas.create_oval(px-r,py-r,px+r,py+r, fill='black')

    def information(self, info_win):
        '''信息面板'''
        x1 = 2*self.cell; x2 = 10*self.cell
        info_win.create_text(x1, self.cell, font=('微软雅黑',12),
                    text='玩家1', tags='player1')
        info_win.create_text(x2, self.cell, font=('微软雅黑',12),
                    text='玩家2', tags='player2')
        y = 2*self.cell; r =10
        info_win.create_oval(x1-r, y-r, x1+r, y+r, fill='black')
        info_win.create_oval(x2-r, y-r, x2+r, y+r, fill='white')
        info_win.create_text(6*self.cell, y, font=('微软雅黑',12),
                    text='20:00        20:00', tags='time')

    def board_pt(self, event):
        '''换算棋盘坐标'''
        x = (event.x-self.cell)//self.cell
        y = (event.y-self.cell//2)//self.cell
        return x,y

    def click_tool(self, event):
        '''菜单'''
        x = int(event.x/self.cell-1.25)//2  # 换算棋盘坐标
        if x<0 or x>6:
            return
        name = ('打开', '保存', '单机', '网络', '打谱', '说明', '悔棋')[x]
        if name in ('单机', '网络', '打谱'):
            self.new_game(name)


    def new_game(self, name):
        self.tools.itemconfig(self.mode, fill='')
        self.tools.itemconfig(name, fill='orange')
        self.canvas.delete('go')
        self.canvas.delete('last')
        self.canvas.delete('aims')
        self.record_win.delete('all')
        self.drag_record(-self.record_pt[0], -self.record_pt[1])
        call_mode = {'单机': self.call_alone,
                    '网络': self.call_online,
                    '打谱': self.call_alone}
        self.canvas.bind("<Button-1>", call_mode[name])
        if self.mode == '打谱':
            p = messagebox.askquestion(title='新游戏',
                        message='是否保存当前游戏数据?')
            if p == 'yes':
                self.save()
        # 初始化游戏
        self.mode = name        # 游戏模式
        self.player = 1         # 初始棋手为黑棋
        self.puting = False
        self.moveing = False    # 移动棋子状态
        self.step = (0,0)       # 当前步数
        self.piece = {0:[]}     # 记录棋子
        self.record = {0:[]}    # 记录坐标
        self.record_id = {0:[]} # 记录历史图
        self.time = [1200,1200] # 计时
        if name == '网络':
            self.info_win.itemconfig('player1', text='玩家1')
            self.info_win.itemconfig('player2', text='玩家2')
            self.info_win.unbind("<Button-1>")
            self.creat_client()

    def creat_client(self):
        for i in range(4):
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.bind(('127.0.0.1', random.randint(7000, 39999)))
                self.client.connect(('127.0.0.1', 6688))
                if self.recv() == 'success':
                    break
            except:
                pass
        if self.recv() == '请输入姓名':
            win = tk.Toplevel(self.canvas)
            paddict = {'padx':20, 'pady':5}
            tk.Label(win, text='请输入姓名:').grid(row=0, column=0, **paddict)
            tk.Label(win, text='创建房间 执黑(1)？执白(2):').grid(row=1, column=0, **paddict)
            tk.Label(win, text='加入房间:').grid(row=2, column=0, **paddict)
            t1 = tk.StringVar(); t1.set('')
            t2 = tk.StringVar(); t2.set('')
            t3 = tk.StringVar(); t3.set('')
            tk.Entry(win, textvariable=t1).grid(row=0, column=1, **paddict)
            tk.Entry(win, textvariable=t2).grid(row=1, column=1, **paddict)
            tk.Entry(win, textvariable=t3).grid(row=2, column=1, **paddict)
            def get_name():
                self.send(t1.get())
                if len(t3.get()) >= 4:
                    self.send(f'room_in{t3.get()}')
                else:
                    if t2.get() == '2':
                        self.send('room_new2')
                    else:
                        self.send('room_new1')
                threading.Thread(target=self.recv_pt).start()
                win.destroy()
            tk.Button(win, text='确定', command=get_name).grid(row=4, column=0, columnspan=2, **paddict)

    def call_online(self, event):
        '''在线模式'''
        x,y = self.board_pt(event)
        if x<0 or x>14 or y<0 or y>14:
            return
        self.send(f'put_{[x,y]}')

    def recv_pt(self):
        while True:
            re = self.recv()
            print('接收:',re)
            if re == 'out':
                text = '加入失败，请重新点击 "网络" 进入网络模式。'
                messagebox.showinfo(title='网络', message = text)
                self.client.close()
                break
            elif re[:3] == 'in_':
                pass
            elif re[:5] == 'name_':
                names = json.loads(re[5:])
                self.info_win.itemconfig('player1', text=f'{names[0]}')
                self.info_win.itemconfig('player2', text=f'{names[1]}')
            elif re[:5] == 'room_':
                self.info_win.itemconfig('time', text=f'房间号：{re[5:]}')
            elif re[:4] == 'put_':
                pt_color = ('orange', 'red', 'green') # 标识颜色
                if re[4] == '3':
                    continue
                if re[4] == '4':
                    pts = json.loads(re[6:])
                    self.opt_pts(pts, pt_color[0])
                    continue

                self.restep(0, '+'); self.restep(0, '+')
                self.canvas.delete('last')
                self.canvas.delete('aims')
                pts = json.loads(re[6:])
                if len(pts) == 2:
                    self.put_piece(self.step, (pts[0], pts[1], pt_color[1]))
                    self.record[0].append((*pts[1], pts[0]))
                else:
                    self.put_piece(self.step, (pts[0], pts[1], pt_color[2]),
                                            (pts[2], pts[3], pt_color[1]))
                    self.record[0].append((*pts[1], pts[0], *pts[3], pts[2]))
                self.draw_record(self.step)

            elif re[:4] == 'win_':
                pts = json.loads(re[4:])
                pt1 = self.repair(pts[1][:2]); pt2 = self.repair(pts[1][2:])
                self.canvas.create_line(*pt1, *pt2, fill='red',width=2, tags='last')
                self.win_msg(pts[0])
                self.client.close()
                break

    def call_alone(self, event):
        '''单机模式落子 player：黑(1)、白(2)'''
        pass

    def win_msg(self, op):
        self.canvas.unbind("<Button-1>")
        player = '黑方' if op == 2 else '白方'
        messagebox.showinfo(title='游戏结束', message = f'{player}获胜！')

    def put_piece(self, step, piece, move=tuple()):
        '''落子'''
        def _draw(player, pt, color, step):
            if self.puting:  
                colors = ('dimgray', 'lightgrey') # 棋子颜色
            else:
                colors = ('black', 'white') # 棋子颜色
            r = 12; r2 = 6 # 棋子半径、标识半径
            pt1 = self.repair(pt, -r); pt2 = self.repair(pt, r)
            id1 = self.canvas.create_oval(*pt1, *pt2, fill=colors[player-1], tags='go')
            pt1 = self.repair(pt, -r2); pt2 = self.repair(pt, r2)
            self.canvas.create_oval(*pt1, *pt2, fill=color, outline='', tags='last')
            if self.puting:
                return (id1,)
            else:
                pt1 = self.repair(pt); op = 1 if player==1 else 0
                id2 = self.canvas.create_text(*pt1, fill=colors[op],
                            text=step[1]+1, tags='go')
                return id1,id2
        if move:
            self.piece[step[0]].append((*_draw(*piece, step), *_draw(*move, step)))
            self.canvas.create_line(*self.repair(piece[1]), *self.repair(move[1]),
                fill='blue', arrow='first', width=2, tags='last')
        else:
            self.piece[step[0]].append(_draw(*piece, step))

    def opt_pts(self, pts, color):
        # 绘制可选点--------------------------------------
        self.canvas.delete('last')
        self.canvas.delete('aims')
        r = 6
        for pt in pts:
            p1 = self.repair(pt, -r); p2 = self.repair(pt, r)
            self.canvas.create_oval(*p1, *p2, fill=color,
                        outline='', tags='aims')

    def draw_record(self, step):
        '''绘制历史图'''
        self.record_win.delete('last')
        colors = ('black', 'white') # 棋子颜色
        r = 8; r2 = 4 # 棋子半径、标识半径
        m = 1 if isinstance(step[0], int) else len(step[0])
        px = (step[1]+1)*self.cell; py = m+1*self.cell # 高度, 宽度
        info = self.record[step[0]][step[1]]
        id1 = self.record_win.create_line(px-self.cell+r,py, px-r,py)
        id2 = self.record_win.create_oval(px-r,py-r,px+r,py+r, fill=colors[info[-1]-1])
        text = f'{step[1]+1}' if len(info) == 3  else f'{step[1]+1}(移)'
        id3 = self.record_win.create_text(px,py+r*2, text=text)
        self.record_win.create_oval(px-r2,py-r2,px+r2,py+r2, fill='red',
                    outline='', tags='last')
        self.record_id[step[0]].append((id1, id2, id3))
        # 移动
        if px > 8*self.cell:
            self.drag_record(-self.cell, 0)

    def drag_record(self, x, y):
        self.record_win.scan_mark(0, 0)
        self.record_win.scan_dragto(x, y, gain=1)
        self.record_pt = (self.record_pt[0]+x, self.record_pt[1]+y)
        while self.record_pt[0] >0 or self.record_pt[1] >0:
            self.drag_record(-self.record_pt[0], -self.record_pt[1])

    def send(self, data):
        data = data.encode("utf-8")
        send_len = struct.pack('i',len(data))
        self.client.send(send_len)
        self.client.send(data)

    def recv(self):
        data_len = struct.unpack('i', self.client.recv(4))[0]
        data = self.client.recv(data_len)
        return data.decode()

    def repair(self, pts, d=0):
        # --------------------------------------------------
        if isinstance(pts, tuple) or isinstance(pts, list):
            x = int((pts[0]+1.5)*self.cell+d)
            y = (pts[1]+1)*self.cell+d
            return x,y
        elif isinstance(pts, int) or isinstance(pts, float):
            return int((pts+1.5)*self.cell+d)

    def restep(self, n, s='+'):
        p = 1 if s == '+' else -1
        self.step = (n,len(self.record[n])+p-1)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('+300+50')
    root.title('反五子棋')
    root.resizable(0,0)
    gb = OppositeGobangUI(root)
    tk.mainloop()