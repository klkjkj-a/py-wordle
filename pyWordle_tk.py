import tkinter as tk
from tkinter import font
from tkinter.ttk import Combobox
import random

root = tk.Tk()
root.title('pyWordle')
root.geometry('600x800')
root.resizable(False, False)

NUM_ROWS = 6
LENGTH = 5

word_chosen = ''
lines = []
guessed = []# 猜测列表
window_rule = None
window_options = None
window_about = None

###
def rule():
    global window_rule

    if window_rule is not None and window_rule.winfo_exists():
        window_rule.lift()
        return

    window_rule = tk.Toplevel(root)
    window_rule.title("规则")
    window_rule.geometry("470x190")
    window_rule.resizable(False, False)

    window_rule.focus_set()
    
    def close_window_rule():
        window_rule.destroy()

    tk.Label(window_rule, text=f'''用 6 次机会猜测一个字母数为 {LENGTH} 的英文单词。
输入猜测的单词后按下确定按钮。输入不区分大小写。
每个字母的颜色代表它的状态。
 · 绿色：字母和位置都正确。
 · 黄色：字母存在但位置不正确。
 · 白色：字母不在目标单词中。''', font=('微软雅黑', 11), anchor='w', justify='left').pack(anchor='w', fill='x', padx=10, pady=10)

    tk.Button(window_rule, text='确定', command=close_window_rule).pack(pady=1)

###
def options():
    global window_options

    if window_options is not None and window_options.winfo_exists():
        window_options.lift()
        return

    window_options = tk.Toplevel(root)
    window_options.title("设置")
    window_options.geometry("470x170")
    window_options.resizable(False, False)

    window_options.focus_set()

    def close_window_options():
        window_options.destroy()

    tk.Label(window_options, text='字母数设置', font=('微软雅黑', 11)).place(x=20, y=10)
    tk.Label(window_options, text='当设置的字母数与当前不同时，会重启游戏。', font=('微软雅黑', 11)).place(x=20, y=40)

    tk.Label(window_options, text='设置字母数为', font=('微软雅黑', 11), anchor='w', justify='left').place(x=20, y=70)

    lettersnum_string = tk.StringVar()
    combo = Combobox(
        window_options,
        state='readonly',
        width=5,
        textvariable=lettersnum_string,
        values=['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
        font=('Segoe UI', 11)
    )
    combo.current(1)
    combo.place(x=120, y=70)
    
    def c():
        global LENGTH
        if int(lettersnum_string.get()) != LENGTH:
            window_options.destroy()
            LENGTH = int(lettersnum_string.get())
            start()
        else:
            window_options.destroy()
        
    tk.Button(window_options, text='确定', font=('微软雅黑', 11), command=c).place(x=190, y=65)


###
def about_game():
    global window_about

    if window_about is not None and window_about.winfo_exists():
        window_about.lift()
        return

    window_about = tk.Toplevel(root)
    window_about.title("关于游戏")
    window_about.geometry("470x170")
    window_about.resizable(False, False)

    window_about.focus_set()

    def close_window_about():
        window_about.destroy()

    tk.Label(window_about, text='''本游戏是经典小游戏Wordle的Python实现。
作者：klkjkj-a (GitHub)''', font=('微软雅黑', 11), anchor='w', justify='left').pack(anchor='w', fill='x', padx=10, pady=10)
    
    strike_font = font.Font(family='微软雅黑', size=11, overstrike=True)
    tk.Label(window_about, text='大部分代码由 DeepSeek 生成。', font=strike_font, anchor='w', justify='left').pack(anchor='w', fill='x', padx=10, pady=5)

    tk.Button(window_about, text='确定', command=close_window_about).pack()

###
CHAR_RANGES = [(0x41, 0x5A), (0x61, 0x7A)]

def make_validator(parent, length=1, ranges=None):
    def validate(P):
        if len(P) > length:
            return False
        if ranges:
            for ch in P:
                if not any(lo <= ord(ch) <= hi for lo, hi in ranges):
                    return False
        return True
    return (parent.register(validate), '%P')


class CodeRow:
    def __init__(self, parent, length=5, char_ranges=None):
        self.length = length
        self.entries = []
        self.frame = tk.Frame(parent)

        vcmd = make_validator(self.frame, length=1, ranges=char_ranges)

        for i in range(length):
            e = tk.Entry(self.frame, width=2, justify='center', font=('Arial', 16))
            e.pack(side='left', padx=2)
            e.config(validate='key', validatecommand=vcmd)
            self.entries.append(e)

        for i, e in enumerate(self.entries):
            e.bind('<KeyRelease>', lambda ev, idx=i: self._on_key(ev, idx))

        self.on_change = None
        self.entries[0].focus_set()

    def _on_key(self, event, idx):
        if event.keysym == 'BackSpace':
            if idx > 0 and not self.entries[idx].get():
                self.entries[idx - 1].focus_set()
        elif len(self.entries[idx].get()) == 1 and idx < self.length - 1:
            self.entries[idx + 1].focus_set()

        if self.on_change:
            self.on_change()

    def get_code(self):
        return ''.join(e.get() for e in self.entries)

    def is_complete(self):
        return len(self.get_code()) == self.length

    def disable(self):
        for e in self.entries:
            e.config(state='disabled')


container = tk.Frame(root)
container.pack(pady=20)

rows = []
buttons = []

def initialize():
    global rows, buttons, guessed
    rows = []
    buttons = []
    guessed = []

    # 关键：销毁 container 里的所有旧控件
    for widget in container.winfo_children():
        widget.destroy()

    rows = []
    buttons = []

    for i in range(NUM_ROWS):
        row = CodeRow(container, LENGTH, CHAR_RANGES)
        row.frame.grid(row=i * 2, column=0, sticky='w', pady=(0, 4))
        rows.append(row)

        btn = tk.Button(container, text='确定')
        btn.grid(row=i * 2 + 1, column=0, pady=(0, 20))
        btn.grid_remove()
        buttons.append(btn)

def select_word():
    global word_chosen, lines
    path = r'words.txt'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if lines:
        while True:
            word_chosen = random.choice(lines).rstrip('\n')
            if len(word_chosen) == LENGTH:
                break

def make_check(i):
    def check():
        if rows[i].is_complete():
            buttons[i].grid()
        else:
            buttons[i].grid_remove()
    return check


def make_click(i):
    def click():
        global guessed
        
        win = False
        word_temp = list(word_chosen)
        word_guessed = []# 当前所猜的词
        word_string = (rows[i].get_code()).lower()
        label_text = ''

        # print(word_chosen)
        
        if i < NUM_ROWS and word_string + '\n' in lines and word_string != word_chosen and word_string not in guessed:

            buttons[i].grid_remove()
            rows[i].on_change = None
            rows[i].disable()
            guessed.append(word_string)
        
            word_guessed = list(word_string)

            for j in range(0, LENGTH):
                if word_guessed[j] == word_chosen[j]:
                    word_guessed[j] = '0'
                    word_temp[j] = '1'
            
            for k in range(0, LENGTH):
                for l in range(0, LENGTH):
                    if word_guessed[k] == word_temp[l]:
                        word_guessed[k] = '2'
                        word_temp[l] = '3'
            
            word_temp = list(word_chosen)
            
            for l in range(0, LENGTH):
                if word_guessed[l] == '0':
                    rows[i].entries[l].config(
                        disabledforeground='white',
                        disabledbackground='#6BAA64',
                    )
                elif word_guessed[l] == '2':
                    rows[i].entries[l].config(
                        disabledforeground='white',
                        disabledbackground='#C9B457',
                    )
                else:
                    rows[i].entries[l].config(
                        disabledforeground='white',
                        disabledbackground='#787C7F',
                    )

            if i < NUM_ROWS - 1:
                rows[i + 1].frame.grid()
                rows[i + 1].entries[0].focus_set()
        
        elif word_string in guessed:
            pass
            #label_text = ''
            #label = tk.Label(root, text=label_text, font=('Noto Sans SC', 14)).pack()
        elif word_string == word_chosen:
            for m in range(0, LENGTH):
                rows[i].entries[m].config(
                    disabledforeground='white',
                    disabledbackground='#6BAA64',
                )
            buttons[i].grid_remove()
            rows[i].on_change = None
            rows[i].disable()
            tk.Label(root, text='猜测正确。', font=('微软雅黑', 12)).pack()
            win = True

        if i == 5 and win == False:
            tk.Label(root, text=f'游戏结束，正确答案为 {word_chosen}。', font=('微软雅黑', 12)).pack()
            
    return click

def clear_all():
    for widget in list(root.winfo_children()):
        widget.destroy()

def hide_all():
    for row in rows:
        for e in row.entries:
            e.grid_remove()
    for btn in buttons:
        btn.grid_remove()

def hide_all_labels(widget=None):
    if widget is None:
        widget = root
    for child in widget.winfo_children():
        if isinstance(child, tk.Label):
            manager = child.winfo_manager()
            if manager == 'grid':
                child.grid_remove()
            elif manager == 'pack':
                child.pack_forget()
            elif manager == 'place':
                child.place_forget()
        hide_all_labels(child)

def close_all_toplevels():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()

def start():
    global label_text
    label_text = ''
    select_word()
    guessed.clear()     # 清空历史内容
    initialize()        # 内部已销毁旧控件并重建
    close_all_toplevels()
    hide_all_labels()

    for i in range(NUM_ROWS):
        rows[i].on_change = make_check(i)
        buttons[i].config(command=make_click(i))

    # 初始只显示第一行
    for i in range(1, NUM_ROWS):
        rows[i].frame.grid_remove()

menubar = tk.Menu(root)

sub_menu_game = tk.Menu(menubar, tearoff=0)
sub_menu_game.add_command(label='新游戏', command=start)
sub_menu_game.add_command(label='规则', command=rule)

menubar.add_cascade(label='游戏', menu=sub_menu_game)

sub_menu_options = tk.Menu(menubar, tearoff=0)
sub_menu_options.add_command(label='设置', command=options)

menubar.add_cascade(label='设置', menu=sub_menu_options)

sub_menu_about = tk.Menu(menubar, tearoff=0)
sub_menu_about.add_command(label='关于游戏', command=about_game)

menubar.add_cascade(label='关于', menu=sub_menu_about)

root.config(menu=menubar)

start()

root.mainloop()
