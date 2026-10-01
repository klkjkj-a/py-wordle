from colorama import init
from termcolor import colored
from os import system
import sys
import random

word_length = 6

rule = f'''
用 6 次机会猜测一个字母数为 {word_length} 的英文单词。
输入猜测的单词后回车。输入不区分大小写。
每个字母的颜色代表它的状态。
·{colored('绿色', 'green')}：字母和位置都正确。
·{colored('黄色', 'yellow')}：字母存在但位置不正确。
·白色：字母不在目标单词中。
当玩家输入的单词有多个相同字母时，位置正确的字母（若有）会优先渲染为{colored('绿色', 'green')}。
'''

def initialize():
    while True:
        command = input('输入 n 进入新游戏，输入 q 退出，输入 r 查看规则。\n\n$ ')
        if command == 'n':
            system('cls')
            game()
        elif command == 'q':
            quit()
        elif command == 'r':
            print(rule)
            command = input('$ ')
        elif command == '':
            command = input('$ ')
        else:
            command = input(' 命令无效。\n$ ')

def clear_previous_line(n=1):
    sys.stdout.write(f"\033[{n}A\r\033[2K")
    sys.stdout.flush()

def game():

    global word_length
    
    win = 0
    guessed = []
    count = 0
    
    path = r"words.txt"
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if lines:
        while True:
            word_chosen = random.choice(lines).rstrip('\n')
            word_chosen = word_chosen.lower()
            if len(word_chosen) == word_length:
                break

    # ·· 调 ··· ··· 试 ··· ··· 调 ··· ··· 试 ··· ··· 调 ··· ··· 试 ··· 
    # print(f'调试：[{word_chosen}]')
    # ·· 调 ··· ··· 试 ··· ··· 调 ··· ··· 试 ··· ··· 调 ··· ··· 试 ··· 
    
    print('输入猜测的单词。\n')

    while count <= 5:
        guess = input('> ')
        guess = guess.lower()

        word_temp = list(word_chosen)
        list_guess = list(guess)

        if guess == word_chosen:
            clear_previous_line(n=1)
            print(f"\r{colored(guess, 'green')}", flush=True)
            print(' 猜测正确。\n')
            win = 1
            initialize()
            
        elif guess not in guessed:
            if guess + '\n' in lines and len(guess) == word_length:
                
                    for j in range(0, word_length):
                        if guess[j] == word_chosen[j]:
                            list_guess[j] = colored(list_guess[j], 'green')
                            word_temp[j] = '1'
                    for k in range(0, word_length):
                        for l in range(0, word_length):
                            if list_guess[k] == word_temp[l]:
                                list_guess[k] = colored(list_guess[k], 'yellow')
                                word_temp[l] = '2'
                                
                    guessed.append(guess)
                    list_guess_string = ''.join(list_guess)
                    
                    clear_previous_line(n=1)
                    print(f'\r{list_guess_string}', flush=True)
                    word_temp = list(word_chosen)
                    
                    count += 1

                    if count < 6:
                        print(f' 还有 {6 - count} 次机会。\n')
                    
            elif len(guess) != word_length:
                clear_previous_line(n=1)
                print(f'\r{guess}', flush=True)
                print(' 单词长度不正确，猜测无效。')
                print(f' 还有 {6 - count} 次机会。\n')
                
            else:
                clear_previous_line(n=1)
                print(f'\r{guess}', flush=True)
                print(' 单词不合法，猜测无效。\n')
                print(f' 还有 {6 - count} 次机会。\n')
                
        else:
            clear_previous_line(n=1)
            print(f'\r{guess}', flush=True)
            print(' 重复猜测，猜测无效。')
            print(f' 还有 {6 - count} 次机会。\n')

        if count == 6 and win == 0:
            print(f' 游戏结束，正确答案为 {word_chosen}。\n')
            initialize()


init()

print(f'猜测一个字母数为 {word_length} 的英文单词。')

initialize()
