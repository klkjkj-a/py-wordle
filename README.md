# py-wordle
Wordle 小游戏的 Python 实现。使用 Python 3.12.2.
## pyWordle.py
以命令行界面呈现。需要和 words.txt 在同一目录下才能运行。
## pyWordle_tk.py
调用 tkinter 库，以图形界面呈现，可以选择单词长度。需要和 words.txt 在同一目录下才能运行。
## words.txt
词库。Python 从这个文件抽取单词。

词库单词不齐全，一些形容词和副词缺少比较级和最高级。

## 致谢
pyWordle_tk.py的代码大部分由 DeepSeek 生成。

词库来自公开语料数据，很多词的变化形式由腾讯元宝补充。
## Release
Release 中是最终的发行版安装包。建议在 64 位 Windows 系统安装。
在发行版中，word.txt 和 .exe 格式的主程序在同一个文件夹内。
发现词库缺词，可以直接修改词库。最好要以 issue 的形式上报。
