import tkinter as tk

class Calculator:
    """计算器"""
    keys_num = ['1','2','3','4','5','6','7','8','9','0','00']
    keys_op = ['+','-','×','÷']
    colors = {'bg':'#ececf4', 'num':'#fafafa', 'ac':'#ecb036',
                'ops':'#dcdeea', '=':'#596eee', 'moniter':'#ffffff'}

    def __init__(self, parent):
        # 参数
        width = 400; height = 510
        self.formula = '' # 算式

        # 主框架
        self.frame = tk.Frame(parent, width=width, height=height, bg=self.colors['bg'])
        self.frame.pack()

        # 界面
        space = 20 # 边框宽度
        moniter_w = width-space*2; moniter_h = 90
        self.set_moniter((space, space), (moniter_w, moniter_h)) # 显示器区域
        self.set_buttons(space, (space, 2*space+moniter_h), (moniter_w, moniter_w)) # 按键区域

    def set_moniter(self, place, size):
        # 显示器
        moniter = tk.Frame(self.frame, bg=self.colors['moniter'])
        moniter.place(x=place[0], y=place[1], width=size[0], height=size[1])

        self.formula_var = tk.Label(moniter, bg=self.colors['moniter'], text='', anchor='w',
                font=("微软雅黑", 15))
        self.formula_var.place(x=0, y=0, width=size[0], height=size[1]//2)
        self.result_var = tk.Label(moniter, bg=self.colors['moniter'], text='0', anchor='e',
                font=("微软雅黑", 15))
        self.result_var.place(x=0, y=size[1]//2, width=size[0], height=size[1]//2)


    def set_buttons(self, space, place, size):
        # 按键区
        buttons = tk.Frame(self.frame, bg=self.colors['bg'])
        buttons.place(x=place[0], y=place[1], width=size[0], height=size[1])

        but_w = (size[0]+space)//4-space; but_h = (size[1]+space)//5-space
        but_keys = [['7','8','9','4','5','6','1','2','3','0','00','.'],['+','-','×','÷','='],['AC','←']]
        font=("微软雅黑", 20)
        click = lambda s: (lambda: self.cilck(s))

        # 数字区
        for i in range(12):
            but = tk.Button(buttons, text=but_keys[0][i], font=font,
                    command=click(but_keys[0][i]), bg=self.colors['num'])
            but.place(x=(i%3)*(but_w+space), y=(i//3)*(but_h+space), width=but_w, height=but_h)
        # 符号区
        for i in range(5):
            color = '=' if but_keys[1][i] == '=' else 'ops'
            but = tk.Button(buttons, text=but_keys[1][i], font=font,
                    command=click(but_keys[1][i]), bg=self.colors[color])
            but.place(x=3*(but_w+space), y=i*(but_h+space), width=but_w, height=but_h)
        # 特殊按键区
        but0 = tk.Button(buttons, text=but_keys[2][0], font=font,
                    command=click(but_keys[2][0]), bg=self.colors['ac'])
        but0.place(x=0, y=4*(but_h+space), width=but_w*2+space, height=but_h)
        but1 = tk.Button(buttons, text=but_keys[2][1], font=font,
                    command=click(but_keys[2][1]), bg=self.colors['ac'])
        but1.place(x=2*(but_w+space), y=4*(but_h+space), width=but_w, height=but_h)

    def cilck(self, s):
        if(s in self.keys_num):
            # 键入数字
            # 如果键入0
            if(s == '0' or s == '00'):
                if self.formula == '0':
                    # 如果算式只有一个数且为0
                    return
                elif self.formula == '':
                    # 如果算式为空
                    self.formula += '0'
                elif self.formula[-2] in self.keys_op and self.formula[-1]=='0':
                    # 如果位于运算符的0后面
                    return
                elif self.formula[-1] in self.keys_op:
                    # 如果位于运算符后面
                    self.formula += '0'
                else:
                    self.formula += s
            else:
                self.formula += s
        elif(s in self.keys_op):
            # 键入运算符
            if (self.formula[-1] in self.keys_op):
                self.formula = self.formula[:-1]
            self.formula += s
        elif(s == '.'):
            # 键入小数点
            # 反向遍历，查找小数点
            for i in range(len(self.formula)-1, 0, -1):
                if(self.formula[i] in self.keys_op):
                    break
                elif(self.formula[i] == '.'):
                    return
            # 如果未输入数字，补0
            if self.formula == '' or self.formula[-1] in self.keys_op:
                self.formula += '0'
            self.formula += s
        elif(s == 'AC'):
            # 键入AC
            self.formula = ''
            self.result_var['text'] = '0'
        elif(s == '←'):
            # 键入←
            self.formula = self.formula[:-1]
        elif(s == '='):
            # 键入 =
            try:
                if (self.formula[-1] in self.keys_op):
                    self.formula = self.formula[:-1]
                self.result_var['text'] = eval(self.formula.replace('×','*').replace('÷','/'))
            except:
                self.result_var['text'] = '0不能做除数！'

        self.formula_var['text'] = self.formula

if __name__ == '__main__':
    window = tk.Tk()
    window.title('计算器')
    window.resizable(0,0)

    Calculator(window)
    window.mainloop()
