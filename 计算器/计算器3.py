import tkinter as tk
# 画布部分
from matplotlib import mathtext         # 创建LaTex样式图像
import matplotlib.font_manager as mfm   # 字体
from io import BytesIO                  # 二进制的类文件对象
import numpy as np                      # 数据处理
from PIL import ImageTk,Image           # 图像对象
# 图像绘制
def images(frame, text='123', pt=(0,0), size=20):
    # 设置字体样式，创建图像
    text = r'$'+text+r'$'
    bfo = BytesIO() # 创建二进制的类文件对象
    prop = mfm.FontProperties(family='sans serif', size=size, weight='normal') #size（字号）
    mathtext.math_to_image(text, bfo, prop=prop, dpi=72) # 创建LaTex样式图像到bfo
    # 转换图像背景为透明
    img = Image.open(bfo) # 打开二进制的类文件对象，返回一个PIL图像对象
    pt = pt[0]+img.size[0]//2+2,pt[1]+2
    r= img.split()[0] # 分离出RGBA四个通道
    img = np.dstack((r,r,r,255-np.array(r))).astype(np.uint8) # RGBA四个通道合并为三维的numpy数组
    img = Image.fromarray(img) # numpy数组转PIL图像对象
    # 在画布创建图像
    img = ImageTk.PhotoImage(img)
    image = frame.create_image(*pt, anchor='n', image=img)


# 主窗口
window = tk.Tk()
window.title('计算器')
width = 400; height=530
window.geometry(f'{width}x{height}')
window.resizable(0,0)

# 框架
frame1 = tk.Canvas(window, bg='white')
frame2 = tk.Frame(window, bg='green')
# img = images(frame1, r'\frac{1}{\frac{1}{\frac{1}{\frac{1}{\frac{1}{x+1}+1}+1}+1}+1}', (0,0), 40)
frame1.place(x=20, y=20, width=width-40, height=height-width-20)
frame2.place(x=20, y=height-width+20, width=width-40, height=width-40)

# 按钮函数 #return function
keys_num = ['7','8','9','4','5','6','1','2','3','0']
keys_op = ['+','-','×','/']
keys_0 = True
str1 = '' # 算式
str2 = '0' # 答案
img1 = images(frame1, r'f(x)=\frac{1}{4+x^{2}}÷89.4', (5,5), 20)
img2 = images(frame1, r'0', (300,70), 20)
def click(s): 
    def _cilck():
        global str1
        global str2
        global keys_0
        global img1
        global img2
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
            try: str2 = str(eval(str1.replace('×','*')))
            except: str2 = '0 error！'
        str01 = str1 if len(str1)>0 else '|'
        str02 = str2 if len(str2)>0 else '0'
        frame1.delete("all")
        img1 = images(frame1, str01, (5,5), 20)
        img2 = images(frame1, str02, (200,70), 20)
    return _cilck


# 按钮
frame_w0 = width-40
but_w = frame_w0//4; but_h = frame_w0//5
but_keys = ['7','8','9','+','4','5','6','-','1','2','3','×','0','.','=','/','←','AC']
for i in range(18):
    but = tk.Button(frame2, text=but_keys[i], font=("微软雅黑", 25), command = click(but_keys[i]))
    if i< 16:
        but.place(x=(i%4)*but_w, y=(i//4)*but_h, width=but_w, height=but_h)
    else:
        but.place(x=(i%4)*but_w*2, y=(i//4)*but_h, width=but_w*2, height=but_h)

window.mainloop()

