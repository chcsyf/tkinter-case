import random

class Connect:
    '''
    连连看游戏逻辑
    连接方式：直线连通(相邻、相望)、一折连通、两折连通
    直线连通：二者相邻或之间没有其他元素，必然位于同一水平或同一垂直方向。
    一折连通：相当于位于一个矩形对角顶点，若矩形另外两个顶点可以同时和这两点直连，那就说明可以"一折连通"。
    两折连通：可以转化为判断能否找到一个点C，这个C点与A可以直线连通，且C与B可以通过有一个转角的路径连通。
              可以扫描A同一水平和同一垂直方向的所有点C，判断C能否与B点经过1个转角连通。
    '''
    def __init__(self, height = 10, width = 10, animals_num = 10):
        self.h = height
        self.w = width
        if self.h%2 and self.w%2:
            self.w += 1 # 避免奇数
        self.num = animals_num
        self.surplus = self.w*self.h
        while self.num*2 > self.surplus:
            self.num //= 2 # 避免元素过多
        self.map = [[0]*(self.h+2) for i in range(self.w+2)] # 向四周扩2格
        self.create_map()

    def create_map(self):
        # 生成随机地图
        n = self.w*self.h // self.num # 每个动物数量
        if n%2: n -= 1  # 避免奇数
        tmpMap = []
        for i in range(1, self.num+1):
            tmpMap += [i]*n
        tmpMap += [1]*(self.w*self.h - self.num*n)
        random.shuffle(tmpMap)
        for x in range(0, self.w):
            for y in range(0, self.h):
                self.map[x+1][y+1] = tmpMap[x*self.h + y]
    
    def links(self, x1, y1, x2, y2):
        # 连接性
        # 判断是否直连
        if x1 == x2:
            if self.row_pass(x1, y1, y2):
                return 2, (x1, y1, x2, y2)
        if y1 == y2:
            if self.col_pass(y1, x1, x2):
                return 2, (x1, y1, x2, y2)
        # 判断是否一折连通
        if x1 != x2 and y1 != y2:
            pts = self.one_corner_link(x1, y1, x2, y2)
            if pts:
                return 3, (x1, y1, *pts, x2, y2)
        # 判断是否二折连通
        pts = self.two_corner_link(x1, y1, x2, y2)
        if pts:
            return 4, (x1, y1, *pts, x2, y2)
        return False

    def removed(self, x1, y1, x2, y2):
        # 判断是否可以消除
        if self.map[x1][y1] != self.map[x2][y2] or (not self.map[x1][y1]) \
                            or (not self.map[x2][y2]):
            return False
        pts = self.links(x1, y1, x2, y2)
        if pts:
            self.map[x1][y1] = 0 
            self.map[x2][y2] = 0
            self.surplus -= 2
            # print(pts)
            return pts
        return False

    def is_win(self):
        return not self.surplus

    def row_pass(self, x0, y1, y2):
        # 行连接性
        y1,y2 = (y1,y2) if y1<y2 else (y2,y1)
        row = any(self.map[x0][y1+1:y2])
        return not row

    def col_pass(self, y0, x1, x2):
        # 列连接性
        x1,x2 = (x1,x2) if x1<x2 else (x2,x1)
        col = False if x1+1==x2 else any([x[y0] for x in self.map[x1+1:x2]])
        return not col

    def one_corner_link(self, x1, y1, x2, y2):
        # 判断是否一折连通
        # p3 = (x1, y2); p4 = (x2, y1)
        if (not self.map[x1][y2]) and self.row_pass(x1, y1, y2) \
                        and self.col_pass(y2, x1, x2):
            return x1, y2
        if (not self.map[x2][y1]) and self.row_pass(x2, y1, y2) \
                        and self.col_pass(y1, x1, x2):
            return x2, y1
        return False

    def two_corner_link(self, x1, y1, x2, y2):
        '''判断是否二折连通'''
        # 查找x方向
        y = y1-1
        while 0 <= y and not self.map[x1][y]:
            p4 = self.one_corner_link(x1, y, x2, y2)
            if p4: return x1, y, *p4
            y -= 1
        y = y1+1
        while y < self.h+2 and not self.map[x1][y]:
            p4 = self.one_corner_link(x1, y, x2, y2)
            if p4: return x1, y, *p4
            y += 1 
        # 查找y方向
        x = x1-1
        while 0 <= x and not self.map[x][y1]:
            p4 = self.one_corner_link(x, y1, x2, y2)
            if p4: return x, y1, *p4
            x -= 1
        x = x1+1
        while x < self.w+2 and not self.map[x][y1]:
            p4 = self.one_corner_link(x, y1, x2, y2)
            if p4: return x, y1, *p4
            x += 1
        return False


if __name__ == '__main__':
    connection = Connect(5,5,4)
    connection.map=[[0, 0, 0, 0, 0, 0, 0],
                    [0, 4, 1, 2, 4, 3, 0],
                    [0, 2, 4, 2, 2, 2, 0],
                    [0, 1, 4, 3, 3, 4, 0],
                    [0, 4, 1, 4, 1, 1, 0],
                    [0, 1, 3, 1, 2, 1, 0],
                    [0, 3, 3, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0]]
    link1 = connection.removed(1, 1, 1, 4)
    link2 = connection.removed(3, 1, 5, 1)
    link3 = connection.removed(4, 5, 5, 5)
    link4 = connection.removed(4, 4, 6, 5)
    link5 = connection.removed(2, 5, 5, 4)
    link6 = connection.removed(2, 3, 2, 4)
    link7 = connection.removed(0, 0, 1, 2)
    link8 = connection.removed(1, 2, 4, 2)


    connection.map=[[0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 2, 0, 3, 0],
                    [0, 2, 4, 2, 2, 2, 0],
                    [0, 0, 4, 3, 3, 4, 0],
                    [0, 4, 1, 4, 1, 0, 0],
                    [0, 0, 3, 1, 2, 2, 0],
                    [0, 3, 3, 1, 3, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0]]
    link8 = connection.removed(6, 2, 6, 4)
    print(connection.map)


