import tkinter as tk
import tkinter.filedialog as filedialog, \
        tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import json, socket, struct, random, threading
from imgs import icon_imgs


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
            return (3,)
        elif self[pt] == opponent:
            # 移动对方棋子
            self.moveable_pts(pt) # 生成可移动位置
            if self.move_pts == []:
                return (3,) # 这个棋子不可移动
            self.move_origin = pt
            return (4,self.move_pts)
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
                    if re[0]:
                        return re
                    else:
                        return self.isLose(opponent, pt)
                else:
                    return (3,)

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

        return (0,)

    def __getitem__(self, it:tuple[int]):
        return self.data[it[0]][it[1]]

    def __setitem__(self, it:tuple[int], value:int):
        self.data[it[0]][it[1]] = value

class OppositeGobangUI:
    """反五子棋游戏UI"""
    tool_icons = [] # 图标

    def __init__(self, parent):
        self.cell = 30          # 每个方块大小

        # 游戏状态
        self.gobang = OppositeGobang()  # 棋盘数据
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
        parent.bind('<Destroy>', self.change_run)
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
        self.info_win = tk.Canvas(win_info, height= self.cell*3, bg='whitesmoke')
        self.information(self.info_win)
        win_info.add(self.info_win)
        self.keep()

        # 聊天框
        self.msg_win = tk.Text(win_info, height = 18)
        win_info.add(self.msg_win)
        chat_win = tk.Frame(win_info)
        win_info.add(chat_win)

        def sendmsg():
            msg = chat_text.get('1.0', 'end')
            self.send_msg(msg)
            chat_text.delete('1.0', 'end')
        chat_text = tk.Text(chat_win, height = 2, width=42)
        chat_text.grid(row=0, column=0)
        tk.Button(chat_win, text='发送消息', command=sendmsg).grid(row=0, column=1)

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
                self.draw_back()
    
    def draw_back(self):
        '''悔棋'''
        self.canvas.delete('last')
        self.canvas.delete('aims')
        self.record_win.delete('last')
        self.moveing = False
        if not self.record[0]:
            return
        st = 0
        self.restep(st, '-')
        info = self.record[st].pop()
        ids1 = self.piece[st].pop()
        ids2 = self.record_id[st].pop()
        self.player = info[-1]
        if len(info) == 3:
            self.gobang[info[0], info[1]] = 0
        else:
            op = 1 if self.player ==2 else 2
            self.gobang[info[0], info[1]] = 0
            self.gobang[info[3], info[4]] = op
        for i in ids1:
            self.canvas.delete(i)
        for i in ids2:
            self.record_win.delete(i)
        # 移动
        if self.step[1] > 6:
            self.drag_record(self.cell, 0)

    def new_game(self, name):
        self.tools.itemconfig(self.mode, fill='')
        self.tools.itemconfig(name, fill='orange')
        self.canvas.delete('go')
        self.canvas.delete('last')
        self.canvas.delete('aims')
        self.record_win.delete('all')
        self.drag_record(-self.record_pt[0], -self.record_pt[1])
        self.change_run()
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
        if name == '单机':
            self.gobang = OppositeGobang()  # 棋盘数据
            self.info_win.itemconfig('player1', text='玩家1')
            self.info_win.itemconfig('player2', text='玩家2')
            self.info_win.unbind("<Button-1>")
        elif name == '打谱':
            self.gobang = OppositeGobang()  # 棋盘数据
            self.info_win.itemconfig('player1', text='点击放置黑棋')
            self.info_win.itemconfig('player2', text='点击放置白棋')
            self.info_win.itemconfig('time', text='放置完成')
            self.info_win.bind("<Button-1>", self.init_picece)
        elif name == '网络':
            self.info_win.itemconfig('player1', text='玩家1')
            self.info_win.itemconfig('player2', text='玩家2')
            self.info_win.unbind("<Button-1>")
            self.creat_client()

    def creat_client(self):
        connect = False
        win = tk.Toplevel(self.canvas)
        paddict = {'padx':10, 'pady':5}
        tk.Label(win, text='用户名:').grid(row=0, column=0, **paddict)
        t1 = tk.StringVar(); t1.set('')
        tk.Entry(win, textvariable=t1).grid(row=0, column=1, columnspan=2, **paddict)
        def choiceroom():
            if t2.get() == 2:
                t3.set('    输入房间号： ')
            else:
                t3.set('执黑(1)？执白(2):')
        tk.Label(win, text='连接方式:').grid(row=1, column=0, **paddict)
        t2 = tk.IntVar(); t2.set(1)
        tk.Radiobutton(win, text='创建房间', variable=t2, value=1,
                command=choiceroom).grid(row=1, column=1, **paddict)
        tk.Radiobutton(win, text='加入房间', variable=t2, value=2,
                command=choiceroom).grid(row=1, column=2, **paddict)
        t3 = tk.StringVar(); t3.set('执黑(1)？执白(2):')
        tk.Label(win, textvariable=t3).grid(row=2, column=0, **paddict)
        t4 = tk.StringVar(); t4.set('')
        tk.Entry(win, textvariable=t4).grid(row=2, column=1, columnspan=2, **paddict)

        def sign_in(user):
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.client.connect(('120.53.124.56', 6688))
            self.client.connect(('127.0.0.1', 6688))
            if self.recv() != 'success':
                return
            self.send(f'name_{user[0]}')
            if user[1] == 2 and len(user[2]) >= 4:
                self.send(f'room_in{user[2]}')
            else:
                if user[2] == '2':
                    self.send('room_new2')
                else:
                    self.send('room_new1')
            threading.Thread(target=self.recv_pt, daemon=True).start()

        def get_name():
            user = ['匿名', 1, 1]
            if t1.get() != '':
                user[0] = t1.get()
            if t2.get() == 2:
                user[1] = 2
            user[2] = t4.get()
            win.destroy()
            sign_in(user)

        tk.Button(win, text='确定', command=get_name, bg='red').grid(row=3, column=1, **paddict)

    def change_run(self, event=None):
        try:
            self.send('goquit')
            self.client.close()
            self.recv_pt(False)
        except:
            pass

    def call_online(self, event):
        '''在线模式'''
        x,y = self.board_pt(event)
        if x<0 or x>14 or y<0 or y>14:
            return
        self.send(f'put_{[x,y]}')

    def send_msg(self, msg):
        if self.mode == '网络':
            if len(msg) > 100:
                msg = msg[:100]
            self.send(f'msg_{msg}')
            self.msg_win.insert('end', msg)

    def recv_pt(self, p=True):
        while p:
            re = self.recv()
            print('接收:',re)
            if re == 'out':
                text = '加入失败，请重新点击 "网络" 进入网络模式。'
                messagebox.showinfo(title='网络', message = text)
                self.change_run()
                break
            elif re[:3] == 'in_':
                pass
            elif re[:5] == 'name_':
                names = json.loads(re[5:])
                self.info_win.itemconfig('player1', text=f'{names[0]}')
                self.info_win.itemconfig('player2', text=f'{names[1]}')
            elif re[:5] == 'room_':
                self.info_win.itemconfig('time', text=f'房间号：{re[5:]}')
            elif re[:4] == 'msg_':
                self.msg_win.insert('end', f'收到：{re[4:]}')
            elif re == 'quit':
                messagebox.showinfo(title='结束', message = '对方离开，游戏结束。')
                self.change_run()
                break
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
                self.change_run()
                break

    def init_picece(self, event):
        '''打谱模式 放置棋子'''
        if 10<event.x<110 and 20<event.y<80:
            self.puting = True
            self.player = 1
        elif 250<event.x<350 and 20<event.y<80:
            self.puting = True
            self.player = 2
        elif 140<event.x<220 and 20<event.y<80:
            self.puting = False
            self.player = 1

    def save(self):
        '''保存棋谱'''
        record = {}
        for it in self.record:
            record[str(it)] = self.record[it]
        win = tk.Toplevel(self.canvas)
        paddict = {'padx':20, 'pady':5}
        l1 = tk.Label(win, text='棋手(黑)姓名:').grid(row=0, column=0, **paddict)
        l2 = tk.Label(win, text='棋手(白)姓名:').grid(row=1, column=0, **paddict)
        t1 = tk.StringVar(); t1.set('')
        t2 = tk.StringVar(); t2.set('')
        tk.Entry(win, textvariable=t1).grid(row=0, column=1, **paddict)
        tk.Entry(win, textvariable=t2).grid(row=1, column=1, **paddict)
        def get_name():
            filename = filedialog.asksaveasfilename(filetypes=[('json', '*.json')],
                        defaultextension='.json')
            data = {'player':[t1.get(), t2.get()], 'data': self.record}
            with open(filename, 'w') as fp:
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
        self.info_win.itemconfig('player1', text=data['player'][0])
        self.info_win.itemconfig('player2', text=data['player'][1])
        self.draw_go(data['data'])

    def keep(self):
        '''计时'''
        self.info_win.after(1000, self.keep)
        if self.mode in ('单机',) and self.time[0]>0 and self.time[1]>0:
            self.time[self.player-1] -= 1
            t1,t2 = self.time
            s1 = (f'0{t1%60}')[-2:]; m1 = (f'0{t1//60}')[-2:]
            s2 = (f'0{t2%60}')[-2:]; m2 = (f'0{t2//60}')[-2:]
            self.info_win.itemconfig('time', text=f'{m1}:{s1}        {m2}:{s2}')
            if self.time[0]<=0:
                self.win_msg(1)
            elif self.time[1]<=0:
                self.win_msg(2)

    def draw_go(self, data):
        '''绘制棋局'''
        pt_color = ('orange', 'red', 'green') # 标识颜色
        self.record = {}
        for step,pts in data.items():
            if step == '-1':
                self.record[-1] = pts
                self.piece[-1] = []
                for pt in pts:
                    self.canvas.delete('last')
                    self.gobang[pt[0], pt[1]] = pt[2]
                    self.put_piece((-1,),(pt[2], (pt[0], pt[1]), pt_color[1]))
            elif step == '0':
                step = 0
                self.record[step] = pts
                t = -1
                for pt in pts:
                    self.canvas.delete('last')
                    if len(pt) == 3:
                        self.gobang[pt[0], pt[1]] = pt[2]
                        self.put_piece((step,),(pt[2], (pt[0], pt[1]), pt_color[1]))
                    elif len(pt) == 6:
                        self.gobang[pt[0], pt[1]] = pt[2]
                        self.gobang[pt[3], pt[4]] = pt[5]
                        self.put_piece((step,),(pt[2], (pt[0], pt[1]), pt_color[1]), 
                                (pt[5], (pt[3], pt[4]), pt_color[2]))
                    t += 1
                    self.draw_record((step,t))
        self.player = 1 if self.record[0][-1][-1] == 2 else 2

    def call_alone(self, event):
        '''单机模式落子 player：黑(1)、白(2)'''
        x,y = self.board_pt(event)
        if x<0 or x>14 or y<0 or y>14:
            return

        # 放置模式
        if self.puting:
            self.canvas.delete('last')
            if -1 not in self.record:
                self.record[-1] = []; self.piece[-1] = []
            self.restep(-1, '+')
            if (x, y, self.player) in self.record[-1]:
                self.gobang[x, y] = 0
                index = self.record[-1].index((x, y, self.player))
                _id = self.piece[-1].pop(index)
                self.record[-1].pop(index)
                self.canvas.delete(_id[0])
                self.restep(-1, '-')
            else:
                op = 1 if self.player == 2 else 2
                if (x, y, op) in self.record[-1]:
                    self.gobang[x, y] = 0
                    index = self.record[-1].index((x, y, op))
                    _id = self.piece[-1].pop(index)
                    self.record[-1].pop(index)
                    self.canvas.delete(_id[0])
                    self.restep(-1, '-')
                self.gobang[x, y] = self.player
                self.put_piece(self.step, (self.player, (x,y), 'red'))
                self.record[-1].append((x,y, self.player))
            return

        # 判断落子
        re = self.gobang.go(self.player, (x,y))
        pt_color = ('orange', 'red', 'green') # 标识颜色
        if re[0] == 3:
            # 不可落子
            return 
        elif re[0] == 4:
            # 移动棋子状态
            self.opt_pts(re[1], pt_color[0])
            self.moveing = True
            return

        # 绘制棋子
        opponent = 1 if self.player ==2 else 2
        self.restep(0, '+')
        self.canvas.delete('last')
        self.canvas.delete('aims')
        if self.moveing:
            self.put_piece(self.step, (opponent, (x,y), pt_color[2]),
                        (self.player, self.gobang.move_origin, pt_color[1]))
            self.record[0].append((x,y, opponent, *self.gobang.move_origin, self.player))
            self.moveing = False
        else:
            self.put_piece(self.step, (self.player, (x,y), pt_color[1]))
            self.record[0].append((x,y, self.player))
        self.draw_record(self.step)
        self.player = opponent

        # 判断胜负
        if re[0] == 1 or  re[0] == 2:
            pt1 = self.repair(re[1][:2]); pt2 = self.repair(re[1][2:])
            self.canvas.create_line(*pt1, *pt2, fill='red',width=2, tags='last')
            if self.mode == '单机':
                self.win_msg(re[0])

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
        # 绘制可选点
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
