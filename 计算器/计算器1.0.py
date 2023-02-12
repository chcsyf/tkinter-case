import tkinter as tk

# 主窗口
window = tk.Tk()
window.title('计算器')
width = 400; height=530
window.geometry(f'{width}x{height}')
window.resizable(0,0)

# 生成动态字符串
text1 = tk.StringVar()
text2 = tk.StringVar()
text2.set("0")

# 按钮函数 #return function
keys_num = ['7','8','9','4','5','6','1','2','3','0']
keys_op = ['+','-','×','/']
keys_0 = True
str1 = '' # 算式
str2 = '0' # 答案

def click(s): 
    def _cilck():
        global str1
        global str2
        global keys_0
        if(s in keys_num):
            #0开头问题
            if(s != '0'): keys_0 = False
            if((len(str1)>0 and str1[-1] not in keys_num and str1[-1] != '.') or len(str1)==0):
                keys_0 = True
            if(keys_0 and len(str1)>0 and str1[-1] == '0'):
                str1 = str1[:-1]
            str1+=s
        elif(s in keys_op):
            if(str1[-1] in keys_op): return
            else: str1+=s
        elif(s == '.'): # 判断小数点
            l = len(str1)
            for i in range(l):
                if(str1[l-1-i] in keys_op): break
                elif(str1[l-1-i] == '.'): return
            if((len(str1)>0 and str1[-1] not in keys_num) or len(str1)==0):
                str1+='0'
            str1+=s
        elif(s == 'AC'):
            str1 = ''; str2 = '0'
        elif(s == '←'):
            str1 = str1[:-1]
        elif(s == '='):
            try: str2 = eval(str1.replace('×','*'))
            except: str2 = '0不能做除数！'
        text1.set(str1)
        text2.set(str2)
    return _cilck

# 框架
frame_w = 20; frame_w0 = width-frame_w*2
frame_h = [frame_w, 55, 55, 20]
frame1 = tk.Entry(window, bd=0, textvariable=text1, font=("微软雅黑", 20))
frame2 = tk.Entry(window, bd=0, textvariable=text2, font=("微软雅黑", 20), justify='right')
frame3 = tk.Frame(window, bg='#5C4CEE')
frame1.place(x=frame_w, y=frame_w, width=frame_w0, height=frame_h[1])
frame2.place(x=frame_w, y=sum(frame_h[0:2]), width=frame_w0, height=frame_h[2])
frame3.place(x=frame_w, y=sum(frame_h), width=frame_w0, height=frame_w0)

# 按钮
but_w = frame_w0//4; but_h = frame_w0//5
but_keys = ['7','8','9','+','4','5','6','-','1','2','3','×','0','.','=','/','←','AC']
for i in range(16):
    but = tk.Button(frame3, text=but_keys[i], font=("微软雅黑", 25), command = click(but_keys[i]))
    but.place(x=(i%4)*but_w, y=(i//4)*but_h, width=but_w, height=but_h)
for i in range(2):
    but = tk.Button(frame3, text=but_keys[16+i], font=("微软雅黑", 25), command = click(but_keys[16+i]))
    but.place(x=(i%2)*but_w*2, y=4*but_h, width=but_w*2, height=but_h)


window.mainloop()

