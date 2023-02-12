import tkinter as tk, tkinter.messagebox as messagebox

class Gobang:
    """五子棋游戏"""
    def __init__(self):
        # 棋盘 15x15, 状态：无子、黑子、白子
        self.data = [[0]*15 for i in range(15)]

    def go(self, player:1|2, pt:tuple[int]) -> 0|1|2:
        ''' 落子和输赢判断
            五子棋是逐步落子，故只需判断最新落子是否连成五子。
            输入：player：黑(1)、白(2)
                  pt：落子位置(0-15, 0-15)
            返回：0：落子失败，1：落子成功但未五子连珠，2：落子成功并五子连珠
        '''
        if self[pt] != 0:
            return 0
        self[pt] = player

        # 输赢判断
        r = pt[0]; c = pt[1]
        # 行
        num = 0; r1 = r; r2 = r+1
        while r1 >= 0 and self[r1,c] == player:
            num += 1; r1 -= 1
        while r2 < 15 and self[r2,c] == player:
            num += 1; r2 += 1
        if num >= 5: return 2
        # 列
        num = 0; c1 = c; c2 = c+1
        while c1 >= 0 and self[r,c1] == player:
            num += 1; c1 -= 1
        while c2 < 15 and self[r,c2] == player:
            num += 1; c2 += 1
        if num >= 5: return 2
        # 斜1
        num = 0; r1 = r; r2 = r+1; c1 = c; c2 = c+1
        while r1 >= 0 and c1 >= 0 and self[r1,c1] == player:
            num += 1; r1 -= 1; c1 -= 1
        while r2 < 15 and c2 < 15 and self[r2,c2] == player:
            num += 1; r2 += 1; c2 += 1
        if num >= 5: return 2
        # 斜2
        num = 0; r1 = r; r2 = r+1; c1 = c; c2 = c-1 # 注意c2
        while r1 >= 0 and c1 < 15 and self[r1,c1] == player:
            num += 1; r1 -= 1; c1 += 1
        while r2 < 15 and c2 >= 0 and self[r2,c2] == player:
            num += 1; r2 += 1; c2 -= 1
        if num >= 5: return 2
        return 1

    def __getitem__(self, it:tuple[int]):
        return self.data[it[0]][it[1]]

    def __setitem__(self, it:tuple[int], value:int):
        self.data[it[0]][it[1]] = value

class GobangUI:
    """五子棋游戏UI"""
    def __init__(self, parent):
        self.cell = 30          # 每个方块大小
        # 游戏数据
        self.gobang = Gobang()  # 棋盘数据
        self.player = False     # 初始棋手为黑棋
        self.num = 0            # 手数
        # 主窗口
        length = (14+1.5+1.5)*self.cell
        self.cv = tk.Canvas(parent, width=length, height=length)
        self.cv.pack()
        # 绘制棋盘
        self.board(length)
        self.cv.bind("<Button-1>", self.call_left)

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
        '''鼠标左键事件'''
        x = event.x//self.cell-1  # 换算棋盘坐标
        y = event.y//self.cell-1

        # 落子
        color = ('black', 'white'); r = 12; r2 = 6
        if x<0 or x>14 or y<0 or y>14:
            return
        re = self.gobang.go(self.player+1, (x,y))
        if re == 0:
            return
        else:
            # 绘制棋子
            self.cv.delete('last')
            self.num += 1
            dx = (x+1.5)*self.cell; dy = (y+1.5)*self.cell
            self.cv.create_oval(dx-r,dy-r,dx+r,dy+r, fill=color[self.player])
            self.player = not self.player
            self.cv.create_text(dx, dy, text=f'{self.num}', fill=color[self.player])
            self.cv.create_oval(dx-r2,dy-r2,dx+r2,dy+r2, fill='red', outline='', tags='last')
            if re == 2:
                self.cv.unbind("<Button-1>")
                player = '黑方' if self.player else '白方'
                messagebox.showinfo(title='游戏结束', message = f'{player}获胜！')


if __name__ == '__main__':
    root = tk.Tk()
    gb = GobangUI(root)
    tk.mainloop()