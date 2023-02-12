import tkinter as tk, tkinter.messagebox as tkmsg
import pickle
from PIL import Image, ImageTk

class SignUp(tk.Toplevel):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        self.title('欢迎注册')
        self.geometry('360x200')

        self.windows()

    def windows(self):
        # 用户名框
        self.usrname = tk.StringVar()
        self.usrname.set('abc@xx.com')  # 设置的是默认值
        tk.Label(self, text = '用户名').place(x=10, y=10)
        entry_name = tk.Entry(self, textvariable = self.usrname)
        entry_name.place(x=100, y=10)

        # 用户密码框
        self.usrpwd = tk.StringVar()
        tk.Label(self, text='密  码').place(x=10, y=50)
        entry_pwd = tk.Entry(self, textvariable = self.usrpwd, show='*')
        entry_pwd.place(x=100, y=50)
        # 密码确认框
        self.usrpwd_confirm = tk.StringVar()
        tk.Label(self, text='确认密码').place(x=10, y=90)
        entry_pwd_confirm = tk.Entry(self, textvariable = self.usrpwd_confirm, show='*')
        entry_pwd_confirm.place(x=100, y=90)

        btn_sign_up = tk.Button(self, text=' 注  册', command= self.sign_up)
        btn_sign_up.place(x=120, y=130)

    def sign_up(self):
        pwd = self.usrpwd.get()
        if pwd == '':
            tkmsg.showerror('错误提示', '密码不能为空!')
            self.focus_set()
            return
        complexity = self.pwd_complexity(pwd)
        if complexity == 1:
            tkmsg.showerror('错误提示', '密码长度不能小于6位!')
            self.focus_set()
            return
        elif complexity == 2:
            tkmsg.showerror('错误提示', '密码至少应包含两种类型的字符!')
            self.focus_set()
            return
        if pwd != self.usrpwd_confirm.get():
            tkmsg.showerror('错误提示', '两次输入的密码必须相同')
            self.focus_set()
            return
        name = self.usrname.get()
        if name == '':
            tkmsg.showerror('错误提示', '用户名不能为空!')
            self.focus_set()
            return

        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
            if name in usrs_info:
                tkmsg.showerror('错误提示', '用户名已被注册！')
                self.focus_set()
            else:
                usrs_info[name] = pwd
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(usrs_info, usr_file)
                tkmsg.showinfo('欢迎', '你已经成功注册!')
                self.destroy()

    def pwd_complexity(self, pwd):
        length = 0
        hasNumber = hasUpper = hasLower = hasOther = False
        for s in pwd:
            if s.isdigit():
                hasNumber = True
            elif s.isupper():
                hasUpper = True 
            elif s.islower():
                hasLower = True
            else:
                hasOther = True
            length += 1
        if length < 6:
            return 1
        if hasNumber + hasUpper + hasLower + hasOther < 2:
            return 2
        return 0

        
class Login(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title('欢迎登录')
        self.geometry('450x300')  # 窗口大小为300x200

        self.sign_up = lambda :SignUp(self)
        self.windows()

        self.mainloop()

    def windows(self):
        # 画布
        canvas = tk.Canvas(self, height=300, width=450)
        canvas.pack(side='top')

        tk.Label(self, text='用户名').place(x=100, y=150)
        tk.Label(self, text='密  码').place(x=100, y=190)

        self.usrname = tk.StringVar()  # 将文本框的内容，定义为字符串类型
        self.usrname.set('abc@xx.com')  # 设置默认值
        self.usrpwd = tk.StringVar()

        # 用户名输入框
        tk.Entry(self, textvariable = self.usrname).place(x=160, y=150)
        # 密码输入框
        entry_pwd = tk.Entry(self, textvariable = self.usrpwd, show='*')
        entry_pwd.place(x=160, y=190)

        # 创建注册和登录按钮
        btn_login = tk.Button(self, text=' 登  录', command = self.login)
        btn_login.place(x=150, y=230)
        btn_sign_up = tk.Button(self, text=' 注  册', command = self.sign_up)
        btn_sign_up.place(x=250, y=230)

    def login(self):
        name = self.usrname.get()
        pwd = self.usrpwd.get()
        try:
            with open('usrs_info.pickle', 'rb') as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usrs_info.pickle', 'wb') as usr_file:
                usrs_info = {'admin': 'password'}
                pickle.dump(usrs_info, usr_file)

        if name in usrs_info:
            if pwd == usrs_info[name]:
                tkmsg.showinfo(title='登录成功', message= f'{name}：登录成功！')
            else:
                tkmsg.showinfo(message='错误提示：密码错误，请重试！')

        else:
            is_sign_up = tkmsg.askyesno('提示', '你还没有注册，请先注册！')
            if is_sign_up:
                self.sign_up()


if __name__ == '__main__':
    # SignUp().mainloop()
    Login()

        