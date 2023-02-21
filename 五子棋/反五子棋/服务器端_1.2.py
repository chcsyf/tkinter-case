#coding=UTF-8
import socket, threading, struct, random, json

class OppositeGobang:
    """反五子棋游戏。五子连珠为输"""
    def __init__(self):
        # 棋盘 15x15, 状态：无子、黑子、白子
        self.data = [[0]*15 for i in range(15)]
        self.move_pts = []      # 可移动到的位置
        self.move_origin = None # 移动的原点

    def go(self, player, pt):
        ''' 落子和输赢判断
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

    def moveable_pts(self, pt):
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

    def isLose(self, player, pt):
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

    def __getitem__(self, it):
        return self.data[it[0]][it[1]]

    def __setitem__(self, it, value):
        self.data[it[0]][it[1]] = value

class MyServer:
    def __init__(self):
        # 初始化socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 6688))
        # 设置最大监听数
        self.server.listen(10)
        # 保存每一个客户端的连接和身份信息 {socket:name}
        self.socket_id = {}
        # 保存房间信息 [room]
        self.game_id = []
        # 保存玩家房间信息 {socket:room}
        self.room_id = {}
        # 保存对局数据 {room:[socket,socket,gobang]}
        self.game_data = {}
        self.game_moving = {} # 当前状态 {room:False}
        self.game_player = {} # 当前出棋方 {room:1}

    def run(self):
        while True:
            socket, addr = self.server.accept()
            # 发送信息，提示客户端已成功连接
            self.send_msg(socket, 'success')
            # 记录玩家身份
            self.socket_id[socket] = None
            # 创建线程，负责接收客户端信息
            threading.Thread(target=self.recv_info, args=(socket,), daemon=True).start()

    def send_msg(self, socket, data):
        '''发送消息'''
        data = data.encode("utf-8") # 编码格式转换
        # 确定要发送数据的长度
        send_len = struct.pack('i', len(data)) # 参数'i'表明4个byte
        socket.send(send_len)
        # 发送数据
        socket.send(data)

    def recv_info(self, socket):
        while True:
            buff = socket.recv(4)
            if len(buff) != 4:
                continue
            data_len = struct.unpack('i', buff)[0]
            data = socket.recv(data_len).decode('utf-8')
            print(f'接收{self.socket_id[socket]}:{data}')

            if data == 'goquit':
                self.socket_id.pop(socket)
                r = self.room_id.pop(socket)
                p,q = self.game_data[r][0][0], self.game_data[r][0][1]
                if p == socket and q is not None:
                    self.send_msg(q, 'quit')
                elif q == socket and p is not None:
                    self.send_msg(p, 'quit')
                self.game_id.remove(r)
                self.game_data.pop(r)
                self.game_moving.pop(r)
                self.game_player.pop(r)
                break
            elif data[:5] == 'name_':
                self.socket_id[socket] = data[5:]
            elif data[:5] == 'room_':
                if data == 'room_new1' or data == 'room_new2':
                    # 接收到：新对局，选黑棋、白棋
                    room = random.randint(1000, 99990)
                    while room in self.game_id:
                        room = random.randint(1000, 99990)
                    self.game_id.append(room)
                    self.room_id[socket] = room
                    p = [socket,None] if data == 'room_new1' else [None,socket]
                    self.game_data[room] = [p, OppositeGobang()]
                    self.game_moving[room] = False
                    self.game_player[room] = 1
                    self.send_msg(socket, f'room_{room}')
                    print(self.socket_id[socket],'创建',room)
                elif data[:7] == 'room_in':
                    try:
                        r = int(data[7:])
                        self.room_id[socket] = r
                        if self.game_data[r][0][0] is None:
                            self.send_msg(socket, 'in_1')
                            self.send_msg(socket, f'room_{r}')
                            name = [self.socket_id[socket],
                                self.socket_id[self.game_data[r][0][1]]]
                            name = json.dumps(name, ensure_ascii=False)
                            self.send_msg(socket, f'name_{name}')
                            self.send_msg(self.game_data[r][0][1], f'name_{name}')
                            self.game_data[r][0][0] = socket
                        elif self.game_data[r][0][1] is None:
                            self.send_msg(socket, 'in_2')
                            self.send_msg(socket, f'room_{r}')
                            name = [self.socket_id[self.game_data[r][0][0]],
                                    self.socket_id[socket]]
                            name = json.dumps(name, ensure_ascii=False)
                            self.send_msg(socket, f'name_{name}')
                            self.send_msg(self.game_data[r][0][0], f'name_{name}')
                            self.game_data[r][0][1] = socket
                        else:
                            self.socket_id.pop(socket)
                            self.send_msg(socket, 'out')
                            break
                        print(self.socket_id[socket],'加入',r)
                    except:
                        self.socket_id.pop(socket)
                        self.send_msg(socket, 'out')
                        break
                    self.game_moving[r] = False
                    self.game_player[r] = 1
                continue
            elif data[:4] == 'put_':
                # 放置棋子
                room = self.room_id[socket]
                pl1, pl2 = self.game_data[room][0]
                if pl1 is None or pl2 is None:
                    continue
                if pl1 == socket:
                    ol = 1; op = 2
                else:
                    ol = 2; op = 1
                    pl1, pl2 = pl2, pl1
                if ol != self.game_player[room]:
                    continue
                # 落子情况
                pt = json.loads(data[4:])
                re = self.game_data[room][1].go(ol, tuple(pt))
                if re[0] == 3:
                    self.send_msg(pl1, 'put_3')
                    continue
                elif re[0] == 4:
                    pts = json.dumps(re[1], ensure_ascii=False)
                    self.send_msg(pl1, f'put_4_{pts}')
                    self.game_moving[room] = True
                    continue
                elif re[0] == 0:
                    self.put(room, re[0], pt, ol, op, pl1, pl2)
                    continue
                elif re[0] == 1 or re[0] == 2:
                    self.put(room, re[0], pt, ol, op, pl1, pl2)
                    pts = json.dumps(re, ensure_ascii=False)
                    self.send_msg(pl1, f'win_{pts}')
                    self.send_msg(pl2, f'win_{pts}')
                    break
            elif data[:4] == 'msg_':
                r = self.room_id[socket]
                p,q = self.game_data[r][0][0], self.game_data[r][0][1]
                if p == socket and q is not None:
                    self.send_msg(q, data)
                elif q == socket and p is not None:
                    self.send_msg(p, data)

    def put(self, room, n, pt, ol, op, pl1, pl2):
        # 落子
        if self.game_moving[room]:
            pts = [op, pt, ol, self.game_data[room][1].move_origin]
            pts = json.dumps(pts, ensure_ascii=False)
            self.game_moving[room] = False
        else:
            pts = json.dumps((ol, pt), ensure_ascii=False)
        self.send_msg(pl1, f'put_{n}_{pts}')
        self.send_msg(pl2, f'put_{n}_{pts}')
        self.game_player[room] = op

if __name__ == '__main__':
    my_server = MyServer()
    my_server.run()
