# py-wordle
Wordle 小游戏的 Python 实现。使用 Python 3.12.2.
## pyWordle.py
以命令行界面呈现。需要和 words.txt 在同一目录下才能运行。
## pyWordle_tk.py
调用 tkinter 库，以图形界面呈现，可以选择单词长度。需要和 words.txt、logo.ico 在同一目录下才能运行。
## words.txt
词库。Python 从这个文件抽取单词。

词库来自 [https://github.com/dwyl/english-words] 仓库。

保留词库原有 Unlicense 许可证。根据许可证规定，词库实际已进入公共领域（public domain）。

**代码仍然以原 GPL 许可证开源。**

## 致谢
pyWordle_tk.py的代码大部分由 DeepSeek 生成。

词库来自公开语料数据，很多词的变化形式由腾讯元宝补充。
## Release
Release 中是最终的发行版安装包。建议在 64 位 Windows 系统安装。

在发行版中，words.txt 和 .exe 格式的主程序在同一个文件夹内。

对软件的一切修改都必须符合 GPL 许可证的规定。

有时 releases 中的文件不会随仓库中词库的更新而更新。

## 关于图标
图标用画世界 Pro 绘制，用 Windows 自带的“画图”修改尺寸，用格式工厂转换格式为 .ico。图标是一个意大利体的字母 W，代表Wordle。
