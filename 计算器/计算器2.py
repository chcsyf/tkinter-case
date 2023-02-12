from numbers import Number

# 完成('+','-','*','/','//','%', '(', ')', '.') 和负数
# 完成 尾部追加

# 数字类
class No(Number):
    def __init__(self, value=0):
        self.f = False # 小数
        if isinstance(value, No):
            self.val = value.val    # 数值
            self.str = value.str    # 字符串
        elif isinstance(value, Number):
            self.val = value        # 数值
            self.str = str(value)   # 字符串
        elif value == '.':
            self.val = 0            # 数值
            self.str = str('0.')    # 字符串
            self.f = True
        else: 
            assert eval(value), '无效No类型！'
            self.val = eval(value)      # 数值
            self.str = str(eval(value)) # 字符串
        if(self.val<0 and self.str[0] != '('):
            self.str='('+self.str+')'
        self.l = len(self.str)
    def __str__(self):
        return self.str

    # 字符拼接
    def __lshift__(self, s):
        if s.isdigit():
            if(self.val<0): self.str= self.str[:-1]+s+')'
            else: self.str = (self.str+s) if(self.str!='0') else s
            self.val = eval(self.str)
        elif(s=='.' and not self.f):
            if(self.val<0): self.str= self.str[:-1]+'.)'
            else: self.str += '.'
            self.f = True
        self.l = len(self.str)
        return self
    # 负数字符串
    def __neg__(self):
        self.val = -self.val
        if(self.str[1] == '-'):
            self.str = self.str[2:-1]
        else:
            self.str = '(-'+self.str+')'
        self.l = len(self.str)
        return self

# 算式类
class Op():
    def __init__(self, op1=No(0), o= None, op2=No(0)):
        self.b = 0 # 左括号个数
        self.end_num = False # 默认结尾不是数字
        if(o in ('+','-','*','/','//','%')):
            self.str = op1.str+o+op2.str    # 字符串
            self.val = eval(self.str)       # 数值
            self.end_No = op2 if isinstance(op2, No) else op2.end_No
        else: 
            self.val = op1.val      # 数值
            self.str = op1.str      # 字符串
            self.end_No = op1 if isinstance(op1, No) else op1.end_No 
        self.l = len(self.str)
    def __str__(self):
        return self.str+'='

    # 字符拼接
    def __lshift__(self, s):
        if (self.end_num and (s.isdigit() or s=='.')): # 拼给数字
            end_len = self.end_No.l
            self.end_No<<s
            self.str = self.str[:-end_len]+self.end_No.str
            # 判断括号
            strs = self.str
            for i in range(self.b):
                strs += ')'
            self.val = eval(strs)
        elif(not self.end_num and (isinstance(s, No) or s=='.' or
                (isinstance(s, str) and s.isdigit()))): # 拼给非数字
            self.end_No = No(s)
            self.str += self.end_No.str
            # 判断括号
            strs = self.str
            for i in range(self.b):
                strs += ')'
            self.val = eval(strs)
            self.end_num = True
        elif(self.str[-1] !='(' and self.end_num and
                s in ('+','-','*','/','//','%')): # 拼运算符
            self.end_num = False
            self.str += s
        elif(s=='('): # 拼接左括号
            if(self.str == '0'): # 零开头
                self.str = s 
                self.val = 0 
                self.b = 1
            elif(not self.end_num):
                self.str += s
                self.b += 1
        elif(s==')'): # 拼接右括号
            if(self.end_num):
                if(self.b>0):
                    self.str += s
                    self.b -= 1
                else:
                    self.str = '('+self.str+s
                    self.b = 0
            # 判断括号
            strs = self.str
            for i in range(self.b):
                strs += ')'
            self.val = eval(strs)
        self.l = len(self.str)
        return self

if __name__ == '__main__':
    a = Op()
    a<<'('<<'('<<'('<<'('<<'('
    a<<No(-8)<<"+"<<No(3)
    a<<')'<<'/'<<'5'<<')'<<'/'<<'5656'<<')'<<'/'<<'435'
    a<<'5'<<'-'<<'5'<<'('<<'/'<<'5'<<')'<<'/'<<'5'<<')'

    print(a, a.val, a.l)
