import tkinter as tk, tkinter.messagebox as messagebox

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
                    if self.isLose(player, self.move_origin):
                        return player
                    else:
                        return self.isLose(opponent, pt)
                else:
                    return 3

    def moveable_pts(self, pt:tuple[int]):
        '''可以移动 的位置'''
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
        if num >= 5: return player
        # 列
        num = 0; c1 = c; c2 = c+1
        while c1 >= 0 and self[r,c1] == player:
            num += 1; c1 -= 1
        while c2 < 15 and self[r,c2] == player:
            num += 1; c2 += 1
        if num >= 5: return player
        # 斜1
        num = 0; r1 = r; r2 = r+1; c1 = c; c2 = c+1
        while r1 >= 0 and c1 >= 0 and self[r1,c1] == player:
            num += 1; r1 -= 1; c1 -= 1
        while r2 < 15 and c2 < 15 and self[r2,c2] == player:
            num += 1; r2 += 1; c2 += 1
        if num >= 5: return player
        # 斜2
        num = 0; r1 = r; r2 = r+1; c1 = c; c2 = c-1 # 注意c2
        while r1 >= 0 and c1 < 15 and self[r1,c1] == player:
            num += 1; r1 -= 1; c1 += 1
        while r2 < 15 and c2 >= 0 and self[r2,c2] == player:
            num += 1; r2 += 1; c2 -= 1
        if num >= 5: return player

        return 0

    def __getitem__(self, it:tuple[int]):
        return self.data[it[0]][it[1]]

    def __setitem__(self, it:tuple[int], value:int):
        self.data[it[0]][it[1]] = value

class OppositeGobangUI:
    """五子棋游戏UI"""
    def __init__(self, parent):
        self.cell = 30          # 每个方块大小
        # 游戏数据
        self.gobang = OppositeGobang()  # 棋盘数据
        self.player = 1     # 初始棋手为黑棋
        self.moveing = False # 移动棋子状态
        # 主窗口
        length = (14+1.5+1.5)*self.cell
        self.cv = tk.Canvas(parent, width=length, height=length)
        self.cv.pack()
        # 绘制棋盘
        self.board(length)
        self.cv.bind("<Button-1>", self.call_left)
        text = '''反五子棋游戏。\n 1 五子连珠的一方 输！\n 2 黑棋先行，交替落子。
 3 可以在空白处落子。\n 4 点击对方棋子移动到目标点，并在原位置落子。'''
        messagebox.showinfo(title='游戏规则', message = text)

    def board(self, length):
        '''绘制棋盘 格子：14cellx14cell，边框：1.5cell'''
        # 格线、坐标
        pt0 = 1.5*self.cell
        for i in range(15):
            self.cv.create_line(pt0, pt0+i*self.cell, length-pt0, pt0+i*self.cell, width=1)
            self.cv.create_text(self.cell, pt0+i*self.cell, text=f'{15-i}')
            self.cv.create_line(pt0+i*self.cell, pt0, pt0+i*self.cell, length-pt0, width=1)
            self.cv.create_text(pt0+i*self.cell, length-self.cell, text=f'{chr(65+i)}')
        # 星位
        pt1 = length/2; pt2 = (3+1.5)*self.cell; r = 2
        self.cv.create_oval(pt1-r,pt1-r,pt1+r,pt1+r, fill='black')
        self.cv.create_oval(pt2-r,pt2-r,pt2+r,pt2+r, fill='black')
        self.cv.create_oval(pt2-r,length-pt2-r,pt2+r,length-pt2+r, fill='black')
        self.cv.create_oval(length-pt2-r,pt2-r,length-pt2+r,pt2+r, fill='black')
        self.cv.create_oval(length-pt2-r,length-pt2-r,length-pt2+r,length-pt2+r, fill='black')

    def call_left(self, event):
        '''鼠标左键落子 player：黑(1)、白(2)'''
        x = event.x//self.cell-1  # 换算棋盘坐标
        y = event.y//self.cell-1

        # 落子
        color = ('black', 'white'); pt_color = ('orange', 'red', 'green') # 棋子颜色，标识颜色
        r = 12; r2 = 6 # 棋子半径、标识半径
        if x<0 or x>14 or y<0 or y>14:
            return
        re = self.gobang.go(self.player, (x,y))
        print(re)
        if re == 3:
            # 不可落子
            return 
        elif re == 4:
            # 移动棋子状态
            for x,y in self.gobang.move_pts:
                self.cv.delete('last')
                dx = (x+1.5)*self.cell; dy = (y+1.5)*self.cell
                self.cv.create_oval(dx-r2,dy-r2,dx+r2,dy+r2, fill=pt_color[0],
                        outline='', tags='aims')
            self.moveing = True
            return

        # 绘制棋子
        self.cv.delete('last')
        self.cv.delete('aims')
        opponent = 1 if self.player ==2 else 2
        dx = (x+1.5)*self.cell; dy = (y+1.5)*self.cell
        if self.moveing:
            self.cv.create_oval(dx-r,dy-r,dx+r,dy+r, fill=color[opponent-1])
            self.cv.create_oval(dx-r2,dy-r2,dx+r2,dy+r2, fill=pt_color[2],
                        outline='', tags='last')
            px = (self.gobang.move_origin[0]+1.5)*self.cell
            py = (self.gobang.move_origin[1]+1.5)*self.cell
            self.cv.create_oval(px-r,py-r,px+r,py+r, fill=color[self.player-1])
            self.cv.create_oval(px-r2,py-r2,px+r2,py+r2, fill=pt_color[1],
                        outline='', tags='last')
            self.moveing = False
        else:
            self.cv.create_oval(dx-r,dy-r,dx+r,dy+r, fill=color[self.player-1])
            self.cv.create_oval(dx-r2,dy-r2,dx+r2,dy+r2, fill=pt_color[1],
                        outline='', tags='last')
        self.player = opponent
        if re == 1 or re == 2:
            self.cv.unbind("<Button-1>")
            player = '黑方' if re == 2 else '白方'
            messagebox.showinfo(title='游戏结束', message = f'{player}获胜！')

if __name__ == '__main__':
    root = tk.Tk()
    gb = OppositeGobangUI(root)
    tk.mainloop()