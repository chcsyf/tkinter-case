import random
import numpy as np

class Union_Set:
    '''并查集实现。使用时，先初始化，再合并。'''
    def __init__(self, arr:set[int]):
        '''初始化: 数组(无重复)转化为简单字典，
            每个节点(键)的父节点(值)为其自身。
        例：{1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}'''
        self.parent = {pos: pos for pos in arr}
        self.count = len(arr)

    def union(self, node1, node2):
        '''合并: 节点1的父节点修改为节点2。
        例：由 [[1, 2], [1, 5], [3, 4], [5, 2], [1, 3]]
            得 {1: 1, 2: 1, 3: 1, 4: 3, 5: 1, 6: 6}'''
        self.parent[self.find(node1)] = self.find(node2)

    def find(self, node):
        '''查找: 查找节点元素的根节点。
        例：由 {1: 1, 2: 1, 3: 1, 4: 3, 5: 1, 6: 6}
            得 5 -> 3 -> 1'''
        if node == self.parent[node]:
            return node
        return self.find(self.parent[node])


class Maze(object):
    '''迷宫游戏地图数据生成'''
    def __init__(self, width=11, height=11):
        assert width >= 5 and height >= 5, "长宽应不小于5"
        width = int(width); height = int(height)        # 整数
        self.width = width if width%2 else width+1      # 奇数
        self.height = height if height%2 else height+1  # 奇数

        self.matrix = np.ones((self.height, self.width)) # 初始化地图
        # {0:路, 1:墙}
        self.start = (1, 0) # 入口
        self.end = (self.height-2, self.width-1) # 出口

    def resize_matrix(self, width, height, mode = 0):
        '''重置矩阵'''
        self.__init__(width, height)
        self.generate_matrix(mode)

    def from_matrix(self, new_matrix = None):
        '''从矩阵数据生成地图'''
        self.__init__(len(new_matrix[0]), len(new_matrix))
        self.matrix = new_matrix

    def generate_matrix(self, mode = 0):
        '''根据生成模式生成矩阵。'''
        assert mode in (0, 1, 2), f"模式{mode}不存在"
        # 不同的地图生成算法模式。
        if mode == 0:
            self.generate_matrix_kruskal()
        elif mode == 1:
            self.generate_matrix_dfs()
        elif mode == 2:
            self.generate_matrix_prim()

    def generate_matrix_kruskal(self):
        '''最小生成树算法-kruskal(选边法)生成矩阵'''

        # 检查
        def check(rows, cols):
            ans, counter = [], 0
            for p in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                r, c = rows + p[0], cols + p[1]
                if 0 < r < self.height-1 and 0 < c < self.width-1 \
                        and self.matrix[r, c] == 1:
                    ans.append([p[0]*2, p[1]*2])
                    counter += 1
            if counter <= 1:
                return []
            return ans

        nodes = set()
        row = 1
        while row < self.height:
            col = 1
            while col < self.width:
                self.matrix[row, col] = 0
                nodes.add((row, col))
                col += 2
            row += 2

        union_set = Union_Set(nodes)
        while union_set.count > 1:
            row, col = nodes.pop()
            directions = check(row, col)
            if len(directions):
                random.shuffle(directions)
                for lt in directions:
                    r, c = row + lt[0], col + lt[1]
                    if union_set.find((row, col)) == union_set.find((r, c)):
                        continue
                    nodes.add((row, col))
                    union_set.count -= 1
                    union_set.union((row, col), (r, c))

                    if row == r:
                        self.matrix[row, min(col, c)+1] = 0
                    else:
                        self.matrix[min(row, r)+1, col] = 0
                    break
        # 将出口和入口处的值设置为0
        self.matrix[self.start] = 0
        self.matrix[self.end] = 0

    def generate_matrix_dfs(self):
        '''dfs算法生成矩阵'''

        # 将出口和入口处的值设置为0
        self.matrix[self.start] = 0
        self.matrix[self.end] = 0

        # 检查
        def check(r, c):
            temp_sum = 0
            for p in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                temp_sum += self.matrix[r+p[0], c+p[1]]
            return temp_sum >= 3

        visit_flag = np.zeros((self.height, self.width))
        # dfs算法
        def dfs(row, col):
            visit_flag[row, col] = 1
            self.matrix[row, col] = 0
            if row == self.start[0] and col == self.start[1] + 1:
                return

            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)
            for lt in directions:
                r, c = row+lt[0], col+lt[1]
                if 0 < r < self.height-1 and 0 < c < self.width-1 \
                        and visit_flag[r, c] == 0 and check(r, c):
                    if row == r:
                        visit_flag[row, min(col, c)+1] = 1
                        self.matrix[row, min(col, c)+1] = 0
                    else:
                        visit_flag[min(row, r)+1, col] = 1
                        self.matrix[min(row, r)+1, col] = 0
                    dfs(r, c)

        dfs(self.end[0], self.end[1]-1)
        self.matrix[self.start[0], self.start[1]+1] = 0

    def generate_matrix_prim(self):
        '''primer算法生成矩阵'''

        # 检查
        def check(r, c):
            temp_sum = 0
            for p in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                temp_sum += self.matrix[r+p[0], c+p[1]]
            return temp_sum > 3

        queue = []  # queue:队列
        row = (np.random.randint(1, self.height-1) //2) *2+1
        col = (np.random.randint(1, self.width-1) //2) *2+1
        queue.append((row, col, -1, -1))
        while len(queue) != 0:
            row, col, p, q = queue.pop(np.random.randint(0, len(queue)))
            if check(row, col):
                self.matrix[row, col] = 0
                if p != -1 and row == p:
                    self.matrix[row, min(col, q) + 1] = 0
                elif p != -1 and col == q:
                    self.matrix[min(row, p)+1, col] = 0
                for lt in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                    r, c = row+lt[0], col+lt[1]
                    if 0 < r < self.height-1 and 0 < c < self.width-1 \
                            and self.matrix[r, c] == 1:
                        queue.append((r, c, row, col))

        # 将出口和入口处的值设置为0
        self.matrix[self.start] = 0
        self.matrix[self.end] = 0

    def find_path_dfs(self, end):
        '''解迷宫：dfs算法'''
        visited = np.zeros((self.height, self.width))
        # {0:未经过的位置, 1:已经过的位置}; path: 栈
        _path = []
        def dfs(path):
            nonlocal _path
            pt = path[-1] # 从最后一点开始查找
            # 判断到达出口。由于是深度优先，所以到达出口的path是直接路径。
            if pt == end:
                _path = path[:]
                return 
            # 未到达出口，四向dfs探索
            for p in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                r, c = pt[0]+p[0], pt[1]+p[1] # 四向遍历
                if 0 < r < self.height-1 and 0 < c < self.width \
                        and visited[r, c] == 0 and self.matrix[r, c] == 0:
                    visited[r,c] = 1 # 标记为已探索
                    dfs(path+[(r, c)]) # path+[(r, c)] 而不是 path+=[(r, c)]
        # 从入口开始查找
        dfs([self.start])
        return _path


    # 打印矩阵
    def print_matrix(self, find = False):
        matrix = self.matrix.copy()
        if find:
            for p in self.find_path_dfs(self.end):
                matrix[p] = -1
        for i in range(self.height):
            for j in range(self.width):
                if matrix[i,j] == 1:
                    print('□', end='')
                elif matrix[i,j] == 0:
                    print(' ', end='')
                elif matrix[i,j] == -1:
                    print('■', end='')
            print('')


# 迷宫生成部分主函数
if __name__ == '__main__':
    for i in range(3):
        maze = Maze(15, 13)
        maze.generate_matrix(i)
        maze.print_matrix()
        print('-'*20)
        maze.find_path_dfs(maze.end)
        maze.print_matrix(True)
        print('-'*20)
