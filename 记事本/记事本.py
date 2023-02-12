import tkinter as tk, tkinter.filedialog as tk_file
import os

class NotePad:
    def __init__(self, win, filename = '未命名文件.txt'):
        self.win = win
        self.win.title('记事本-'+filename)
        self.win.geometry("600x400+200+100")
        self.filename = filename

        # 文字窗口
        self.notePad = tk.Text(win, undo=True)
        self.notePad.pack(expand='yes', fill='both')
        scroll = tk.Scrollbar(self.notePad) # 滚动条
        self.notePad.config(yscrollcommand=scroll.set)
        scroll.config(command=self.notePad.yview)
        scroll.pack(side='right', fill='y')

        # 主菜单
        self.menubar = tk.Menu(self.win)
        # 子菜单
        self.file_menu()
        self.edit_menu()
        # 将主菜单设置在窗口上
        self.win['menu'] = self.menubar
        #或 self.win.config(menu=self.menubar)

    def file_menu(self):
        '''文件功能'''
        menus = [None]*4
        menus[0] = lambda *e: self.file_new()
        menus[1] = lambda *e: self.file_open()
        menus[2] = lambda *e: self.file_save()
        menus[3] = lambda *e: self.file_saveas()
        keys = ['N','O','S','Shift+S']
        keysl = ('n','o','s','Shift-s')
        menusl = ("新建","打开","保存","另存为")
        # 菜单
        filemenu = tk.Menu(self.menubar, tearoff=False)
        for i in range(len(menus)):
            filemenu.add_command(label=menusl[i], accelerator=f"Ctrl+{keys[i]}", command=menus[i])
        # 绑定filemenu
        self.menubar.add_cascade(label="文件", menu=filemenu)
        # 绑定快捷键
        keys[3] = 'Shift-S'
        for i in range(len(menus)):
            self.win.bind(f"<Control-{keys[i]}>", menus[i])
            self.win.bind(f"<Control-{keysl[i]}>", menus[i])

    def edit_menu(self):
        # 编辑功能
        menus = [None]*7
        menus[0] = lambda *e: self.notePad.event_generate("<<Undo>>")
        menus[1] = lambda *e: self.notePad.event_generate("<<Redo>>")
        menus[2] = lambda *e: self.notePad.event_generate("<<Cut>>")
        menus[3] = lambda *e: self.notePad.event_generate("<<Copy>>")
        menus[4] = lambda *e: self.notePad.event_generate("<<Paste>>")
        menus[5] = lambda *e: self.edit_find()
        menus[6] = lambda *e: self.notePad.tag_add("sel", "1.0", "end")
        keys = ('Z','Y','X','C','V','F','A')
        keysl = ('z','y','x','c','v','f','a')
        menusl = ("撤销","重做","剪切","复制","粘贴","查找","全选")
        # 菜单
        editmenu = tk.Menu(self.menubar, tearoff=False)
        for i in range(len(menus)):
            editmenu.add_command(label=menusl[i], accelerator=f"Ctrl+{keys[i]}", command=menus[i])
            if i in (1,4):
                editmenu.add_separator()
        # 绑定filemenu
        self.menubar.add_cascade(label="编辑", menu=editmenu)
        # 绑定快捷键
        for i in range(len(menus)):
            self.win.bind(f"<Control-{keys[i]}>", menus[i])
            self.win.bind(f"<Control-{keysl[i]}>", menus[i])
        # 绑定鼠标右键
        self.win.bind("<Button-3>", lambda e: editmenu.tk_popup(e.x_root, e.y_root))

    def file_new(self):
        self.win.title("记事本-未命名文件.txt")
        self.filename = None
        self.notePad.delete(1.0, 'end')

    def file_open(self):
        self.filename = tk_file.askopenfilename(filetypes=[("文本文件",".txt")]) # 不能选择编码方式
        if self.filename == "":
            self.filename = None
        else:
            self.win.title("记事本-" + os.path.basename(self.filename))
            with open(self.filename, mode='r', encoding='utf-8') as f:
                self.notePad.delete(1.0, 'end')
                self.notePad.insert(1.0, f.read())

    def file_save(self):
        try:
            with open(self.filename, mode='w', encoding='utf-8') as f:
                f.write(self.notePad.get(1.0, 'end'))
        except:
            self.file_saveas()

    def file_saveas(self):
        if not self.filename:
            self.filename = '未命名文件.txt'
        filename = tk_file.asksaveasfilename(initialfile=self.filename, filetypes=[("文本文件",".txt")])
        if filename:
            self.filename = filename
        with open(self.filename, mode='w', encoding='utf-8') as f:
            f.write(self.notePad.get(1.0, 'end'))
        self.win.title("记事本 " + os.path.basename(self.filename))

    def edit_find(self):
        # 查找
        find = tk.Toplevel(self.win)
        find.title("查找")
        find.geometry("260x60+400+250")
        find.transient(self.notePad) # 指定为self.notePad的临时窗口

        tk.Label(find, text="查找：").grid(row=0, column=0, sticky="e")

        string = tk.StringVar()
        et = tk.Entry(find, width=20, textvariable=string)
        et.grid(row=0, column=1, padx=2, pady=2, sticky="we")
        et.focus_set()

        num = tk.IntVar()
        tk.Checkbutton(find, text="不区分大小写", variable=num).grid(row=1, column=1, sticky='e')

        def search():
            self.notePad.tag_remove("match", "1.0", 'end')
            count = 0; pos = "1.0"
            needle = string.get()
            if needle:
                while True:
                    pos = self.notePad.search(needle, pos, nocase=num.get(), stopindex='end')
                    if not pos:
                        break
                    lastpos = f'{pos}+{len(needle)}c'
                    self.notePad.tag_add("match", pos, lastpos)
                    count += 1; pos = lastpos
                self.notePad.tag_configure('match', background = 'yellow')
                et.focus_set()
                find.title(f"{count}个被匹配")

        def close_search():
            self.notePad.tag_remove("match", "1.0", 'end')
            find.destroy()

        bt = tk.Button(find, text="查找所有", command = search)
        bt.grid(row=0, column=2, sticky="e" + "w", padx=2, pady=2)

        find.protocol("WM_DELETE_WINDOW", close_search)

if __name__ == '__main__':
    win = tk.Tk()
    NotePad(win)
    tk.mainloop()