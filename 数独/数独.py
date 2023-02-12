import tkinter as tk, tkinter.messagebox as messagebox

class SudokuUI:
    """数独游戏UI"""
    def __init__(self, parent, sudo):
        # 数据
        self.data = sudo    # 数据
        self.level = 0      # 关卡
        self.cell = 40      # 每个格子大小
        self.matrix = [[0]*9 for i in range(9)]         # 原数独
        self.user_matrix = [[0]*9 for i in range(9)]    # 用户填写情况
        self.slove_matrix = [[0]*9 for i in range(9)]   # 解
        self.all_notes:list[('x','y','num')] = []       # 一键笔记的数据

        # 界面
        frame = tk.Frame(parent)
        frame.pack()
        w = self.cell*11; h = self.cell*14
        self.canvas = tk.Canvas(frame, width=w, height=h)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.call_lift)
        self.label = tk.Label(frame, text='数独', bd=1, anchor='w')
        self.label.pack(side="bottom", fill='x')

        # 棋盘绘画对象 详见 self.board()
        self.blocks:list[list['rectangle']]         = [None]*9  # 每个矩形格子对象
        self.blocks_num:list[list['num']]           = [None]*9  # 每个格子内的大数字，包括题目和用户所填
        self.blocks_notes:list[list[list['num']]]   = [None]*9  # 每个格子9个笔记数字，初始为不可见
        self.option:list['num']                     = [None]*9  # 底部数字选项的数字

        # 当前游戏数据 详见 self.new_game()
        self.time = 0
        self.error_num = 0
        # self.act = None
        # self.on_note = False

        # 绘制棋盘
        self.board()
        self.keep()
        self.new_game()

    def board(self):
        '''绘制棋盘 所有的canvas.create均在此处'''
        # 坐标矩阵 matrix[i][j] = (pt_x,pt_y)
        matrix = [[(i*self.cell, j*self.cell) for j in range(14)] for i in range(11)]
        half = self.cell//2

        # 状态栏
        font1 = ("SimHei", 15)
        self.canvas.create_text(matrix[2][1][0], matrix[2][1][1]+0.3*half,
                    text='容易', font=font1, tags='difficulty')
        self.canvas.create_text(matrix[5][1][0]+half, matrix[4][1][1]+0.3*half,
                    text='错误：0/3', font=font1, tags='error_num')
        self.canvas.create_text(matrix[9][1][0], matrix[9][1][1]+0.3*half,
                    text='00:00', font=font1, tags='time')

        # 格子、文字
        font2 = ("SimHei", 25); font3 = ("SimHei",10)
        for i in range(9):
            blocks = [None]*9; nums = [None]*9; notes = [None]*9
            for j in range(9):
                x,y = matrix[i+1][j+2]
                blocks[j] = self.canvas.create_rectangle(x, y, *matrix[i+2][j+3], fill='', tags='blocks')
                nums[j] = self.canvas.create_text(x+half, y+half, text='', font=font2)
                note = [None]*9
                for k in range(9):
                    x1 = x+(k%3*0.3+0.2)*self.cell; y1 = y+(k//3*0.3+0.2)*self.cell
                    note[k] = self.canvas.create_text(x1, y1, text='', font=font3, fill='red', tags='notes')
                notes[j] = note
            self.blocks[i] = blocks; self.blocks_num[i] = nums; self.blocks_notes[i] = notes
            self.option[i] = self.canvas.create_text(matrix[i+1][13][0]+half,matrix[i+1][13][1],
                            text=f'{i+1}', font=font2, fill='gray')
        
        # 格线
        for i in range(10):
            self.canvas.create_line(*matrix[i+1][2], *matrix[i+1][11], width=2)
            self.canvas.create_line(*matrix[1][i+2], *matrix[10][i+2], width=2)
        for i in range(4):
            self.canvas.create_line(*matrix[i*3+1][2], *matrix[i*3+1][11], width=3)
            self.canvas.create_line(*matrix[1][i*3+2], *matrix[10][i*3+2], width=3)

        # 工具
        y = matrix[0][12][1]; xl = [1, 0.2, -0.7, -0.6, 0.4]
        texts = ['擦除', '笔记', '提示', '一键笔记', '重置本关']
        colors = ['blue', 'red', 'green', 'orange', 'black']
        self.canvas.create_rectangle(matrix[3][12][0]-1.3*half, y-0.8*half,
            matrix[3][12][0]+1.7*half, y+0.8*half, fill='', outline='', tags='on_note')
        for i in range(5):
            x = matrix[2*i+1][12][0]+xl[i]*half
            self.canvas.create_text(x,y, text=texts[i], font=font1, fill=colors[i])

    def new_game(self):
        '''新游戏'''
        self.act = None     # 活动的格子
        self.error_num = 0  # 错误次数
        self.time = 0       # 用时
        self.on_note = False # 是否为笔记状态

        nums = self.data[self.level-1]['Grid']
        for i in range(9):
            for j in range(9):
                n = nums[j*9+i]
                self.matrix[i][j] = int(n)
                self.slove_matrix[i][j] = self.user_matrix[i][j] = self.matrix[i][j]
                self.canvas.itemconfig(self.blocks_num[i][j], text='', fill='black')
                if n != '0':
                    self.canvas.itemconfig(self.blocks_num[i][j], text=n)

        self.slove_notes()
        self.label['text'] = f'\t第{self.level+1}关\t难度：简单\t来源：www.thesudoku.com'

    def call_lift(self, event):
        '''鼠标左键事件'''
        x = event.x//self.cell-1  # 换算棋盘坐标
        y = event.y//self.cell-2

        if x<0 or x>8 or y<0:
            return
        if y < 9:
            self.block_tags(x, y, self.user_matrix[x][y])
            # 记录选中的格子
            if self.matrix[x][y]:
                self.act = None
            else:
                self.act = (x, y)
        
        y = (event.y+self.cell//2)//self.cell
        if y == 12:
            if self.act:
                px,py = self.act
                if event.x<80:
                    # 擦除
                    self.block_tags(px,py, None)
                    self.canvas.itemconfig(self.blocks_num[px][py], text='')
                
                elif 165<=event.x<205:
                    # 提示
                    self.fill_in(px, py, self.slove_matrix[px][py], True)

            if 100<=event.x<140:
                # 开启笔记
                if self.on_note:
                    self.canvas.itemconfig('on_note', fill='')
                else:
                    self.canvas.itemconfig('on_note', fill='pink')
                self.on_note = not self.on_note
            
            elif 230<=event.x<305:
                # 一键笔记
                self.auto_notes()
            
            elif 325<=event.x:
                # 重置关卡
                self.restart()

        elif y == 13 and self.act:
            px,py = self.act; x += 1
            if self.on_note and not self.user_matrix[px][py]:
                # 笔记状态
                note = self.blocks_notes[px][py][x-1]
                if self.canvas.itemcget(note, 'text'):
                    self.canvas.itemconfig(note, text='')
                else:
                    self.canvas.itemconfig(note, text=x)
            else:
                self.fill_in(px, py, x, False)

    def fill_in(self, px, py, n, auto):
        '''填数'''
        self.block_tags(px, py, n)
        self.canvas.itemconfig(self.blocks_num[px][py], text=n, fill='green')
        for i in range(9):
            self.canvas.itemconfig(self.blocks_notes[px][py][i], text='')
        # 判断正误
        if (not auto) and self.slove_matrix[px][py] != n:
            self.canvas.itemconfig(self.blocks_num[px][py], fill='red')
            self.error_num += 1
            if self.error_num > 3:
                self.is_win(False)
            self.canvas.itemconfig('error_num', text=f'错误：{self.error_num}/3')
            return
        self.user_matrix[px][py] = n
        self.is_win()

    def block_tags(self, x, y, n):
        '''标注格子颜色'''
        self.canvas.itemconfig('blocks',  fill='')
        # 标示同宫
        lx = x//3; ly = y//3
        for k in range(9):
            i = k%3; j = k//3
            self.canvas.itemconfig(self.blocks[lx*3+i][ly*3+j], fill='pink')
            self.canvas.itemconfig(self.blocks[x][k], fill='pink')
            self.canvas.itemconfig(self.blocks[k][y], fill='pink')
        # 标示相同数字
        if n:
            for i in range(9):
                for j in range(9):
                    if self.user_matrix[i][j] == n:
                        self.canvas.itemconfig(self.blocks[i][j], fill='gray')
        # 标示当前格
        self.canvas.itemconfig(self.blocks[x][y],  fill='orange')

    def slove_notes(self):
        '''全部标注 和 回溯法解数独'''
        # 五个统计矩阵
        line = [[False] * 9 for _ in range(9)]
        column = [[False] * 9 for _ in range(9)]
        block = [[[False] * 9 for _a in range(3)] for _b in range(3)]
        spaces = [] #记录空白格子的数组

        # 统计数字
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j]:
                    t = self.matrix[i][j] -1 #按照 0~8 位置记录已经有数字。
                    line[i][t] = column[j][t] = block[i//3][j//3][t] = True
                else:
                    spaces.append((i, j))

        # 统计标注
        for i,j in spaces:
            for t in range(9):
                if line[i][t] == column[j][t] == block[i//3][j//3][t] == False:
                    self.all_notes.append((i,j,t))

        # 回溯空格部分
        def backtrack(pos: int):
            nonlocal valid
            if pos == len(spaces):
                valid = True; return
            i,j = spaces[pos]; lin,col,bl = line[i],column[j],block[i//3][j//3]
            for t in range(9):
                if lin[t] == col[t] == bl[t] == False: #全部没有数字才可以
                    lin[t] = col[t] = bl[t] = True
                    self.slove_matrix[i][j] = t+1
                    backtrack(pos + 1)
                    lin[t] = col[t] = bl[t] = False
                if valid: return

        valid = False #终止条件
        backtrack(0)

    def auto_notes(self):
        '''一键笔记'''
        for i,j,k in self.all_notes:
            if not self.user_matrix[i][j]:
                self.canvas.itemconfig(self.blocks_notes[i][j][k], text=k+1)

    def is_win(self, win=True):
        '''判断输赢'''
        if win:
            if self.user_matrix == self.slove_matrix:
                messagebox.showinfo(title='获胜', message='恭喜你，取得胜利！\n即将进入下一关。')
                self.level += 1      # 关卡
                self.new_game()
        else:
            messagebox.showinfo(title='失败', message='很遗憾，你失败了！\n请重新尝试。')
            self.restart()

    def restart(self):
        '''重置本关'''
        self.error_num = 0; self.time = 0
        self.canvas.itemconfig('error_num', text='错误：0/3')
        self.canvas.itemconfig('time', text='00:00')
        self.canvas.itemconfig('notes', text='')
        for i in range(9):
            for j in range(9):
                if not self.matrix[i][j]:
                    self.canvas.itemconfig(self.blocks_num[i][j], text='')
                    self.user_matrix[i][j] = 0

    def keep(self):
        '''计时'''
        self.canvas.after(1000, self.keep)
        self.time += 1
        s = ('0'+str(self.time%60))[-2:]; m = ('0'+str(self.time//60))[-2:]
        self.canvas.itemconfig('time', text=f'{m}:{s}')


if __name__ == '__main__':
    sudos = [{"GridID":1,"Difficulty":"Easy","Grid":"003020600900305001001806400008102900700000008006708200002609500800203009005010300"},
            {"GridID":2,"Difficulty":"Easy","Grid":"200080300060070084030500209000105408000000000402706000301007040720040060004010003"},
            {"GridID":3,"Difficulty":"Easy","Grid":"000000907000420180000705026100904000050000040000507009920108000034059000507000000"},
            {"GridID":4,"Difficulty":"Easy","Grid":"030050040008010500460000012070502080000603000040109030250000098001020600080060020"},
            {"GridID":5,"Difficulty":"Easy","Grid":"020810740700003100090002805009040087400208003160030200302700060005600008076051090"},
            {"GridID":8,"Difficulty":"Easy","Grid":"480006902002008001900370060840010200003704100001060049020085007700900600609200018"},
            {"GridID":9,"Difficulty":"Easy","Grid":"000900002050123400030000160908000000070000090000000205091000050007439020400007000"},
            {"GridID":11,"Difficulty":"Easy","Grid":"000125400008400000420800000030000095060902010510000060000003049000007200001298000"},
            {"GridID":12,"Difficulty":"Easy","Grid":"062340750100005600570000040000094800400000006005830000030000091006400007059083260"},
            {"GridID":13,"Difficulty":"Easy","Grid":"300000000005009000200504000020000700160000058704310600000890100000067080000005437"},
            {"GridID":14,"Difficulty":"Easy","Grid":"630000000000500008005674000000020000003401020000000345000007004080300902947100080"},
            {"GridID":15,"Difficulty":"Easy","Grid":"000020040008035000000070602031046970200000000000501203049000730000000010800004000"},
            {"GridID":16,"Difficulty":"Easy","Grid":"361025900080960010400000057008000471000603000259000800740000005020018060005470329"},
            {"GridID":17,"Difficulty":"Easy","Grid":"050807020600010090702540006070020301504000908103080070900076205060090003080103040"},
            {"GridID":18,"Difficulty":"Easy","Grid":"080005000000003457000070809060400903007010500408007020901020000842300000000100080"},
            {"GridID":19,"Difficulty":"Easy","Grid":"003502900000040000106000305900251008070408030800763001308000104000020000005104800"},
            {"GridID":20,"Difficulty":"Easy","Grid":"000000000009805100051907420290401065000000000140508093026709580005103600000000000"},
            {"GridID":21,"Difficulty":"Easy","Grid":"020030090000907000900208005004806500607000208003102900800605007000309000030020050"},
            {"GridID":22,"Difficulty":"Easy","Grid":"005000006070009020000500107804150000000803000000092805907006000030400010200000600"},
            {"GridID":23,"Difficulty":"Easy","Grid":"040000050001943600009000300600050002103000506800020007005000200002436700030000040"},
            {"GridID":24,"Difficulty":"Easy","Grid":"004000000000030002390700080400009001209801307600200008010008053900040000000000800"},
            {"GridID":25,"Difficulty":"Easy","Grid":"360020089000361000000000000803000602400603007607000108000000000000418000970030014"},
            {"GridID":26,"Difficulty":"Easy","Grid":"500400060009000800640020000000001008208000501700500000000090084003000600060003002"},
            {"GridID":27,"Difficulty":"Easy","Grid":"007256400400000005010030060000508000008060200000107000030070090200000004006312700"},
            {"GridID":28,"Difficulty":"Easy","Grid":"000000000079050180800000007007306800450708096003502700700000005016030420000000000"},
            {"GridID":29,"Difficulty":"Easy","Grid":"030000080009000500007509200700105008020090030900402001004207100002000800070000090"},
            {"GridID":30,"Difficulty":"Easy","Grid":"200170603050000100000006079000040700000801000009050000310400000005000060906037002"},
            {"GridID":31,"Difficulty":"Easy","Grid":"000000080800701040040020030374000900000030000005000321010060050050802006080000000"},
            {"GridID":32,"Difficulty":"Easy","Grid":"000000085000210009960080100500800016000000000890006007009070052300054000480000000"},
            {"GridID":33,"Difficulty":"Easy","Grid":"608070502050608070002000300500090006040302050800050003005000200010704090409060701"},
            {"GridID":34,"Difficulty":"Easy","Grid":"050010040107000602000905000208030501040070020901080406000401000304000709020060010"},
            {"GridID":35,"Difficulty":"Easy","Grid":"053000790009753400100000002090080010000907000080030070500000003007641200061000940"},
            {"GridID":36,"Difficulty":"Easy","Grid":"006080300049070250000405000600317004007000800100826009000702000075040190003090600"},
            {"GridID":37,"Difficulty":"Easy","Grid":"005080700700204005320000084060105040008000500070803010450000091600508007003010600"},
            {"GridID":38,"Difficulty":"Easy","Grid":"000900800128006400070800060800430007500000009600079008090004010003600284001007000"},
            {"GridID":39,"Difficulty":"Easy","Grid":"000080000270000054095000810009806400020403060006905100017000620460000038000090000"},
            {"GridID":40,"Difficulty":"Easy","Grid":"000602000400050001085010620038206710000000000019407350026040530900020007000809000"},
            {"GridID":43,"Difficulty":"Easy","Grid":"000158000002060800030000040027030510000000000046080790050000080004070100000325000"},
            {"GridID":44,"Difficulty":"Easy","Grid":"010500200900001000002008030500030007008000500600080004040100700000700006003004050"},
            {"GridID":45,"Difficulty":"Easy","Grid":"080000040000469000400000007005904600070608030008502100900000005000781000060000010"},
            {"GridID":46,"Difficulty":"Easy","Grid":"904200007010000000000706500000800090020904060040002000001607000000000030300005702"},
            {"GridID":146,"Difficulty":"Easy","Grid":"850002400720000009004000000000107002305000900040000000000080070017000000000036040"},
            {"GridID":150,"Difficulty":"Easy","Grid":"700152300000000920000300000100004708000000060000000000009000506040907000800006010"},
            {"GridID":157,"Difficulty":"Easy","Grid":"700260300000158000800340001200470108100000002078010400003000060000031740560080200"},
            {"GridID":158,"Difficulty":"Easy","Grid":"052003004041060020000008100407026058060700010005100270074600300000005000603001000"},
            {"GridID":182,"Difficulty":"Easy","Grid":"000690400048005000962070000007920060050000007000003094280060900390000040070400050"}]

    root = tk.Tk()
    SudokuUI(root, sudos)
    root.mainloop()