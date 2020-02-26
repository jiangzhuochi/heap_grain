from random import randint
from textwrap import dedent

def b(ten):
    """将十进制整数转成二进制字符串，去掉开头的0b"""
    return bin(ten)[2:]

def d(two):
    """将二进制字符串转成十进制整数"""
    return int(two, 2)

def mod2_add_rule(num1, num2):
    """模2加法法则"""
    if (int(num1) + int(num2) == 0) or (int(num1) + int(num2) == 2):
        return '0'
    else:
        return '1'

def mod2_operate(str1, str2, rule):
    """
    两个二进制字符串的模2运算，会自动将位数少的前面补0
    返回二进制字符串，减法是 str1 - str2
    """
    if len(str1) >= len(str2):
        str2 = '0' * (len(str1)-len(str2)) + str2
    else:
        str1 = '0' * (len(str2)-len(str1)) + str1     
    return ''.join(list(map(rule, str1, str2)))

def element_add(lst):
    """
    将每个谷堆的谷粒二进制字符串模2相加，返回二进制字符串
    
    这里采用了递归的写法
    """
    n = len(lst)
    if n == 1:
        # 终止条件，当列表中只有一个数时，将其转成二进制与0相加（相当于直接输出）
        return mod2_operate(b(lst[0]), '0', mod2_add_rule)
    else:
        # 递归操作，将倒数一二位数转成二进制，模2相加
        # 再转成十进制数字，替换掉倒数第二位，并去掉最后一位，缩短列表
        lst[n-2] = d(mod2_operate(b(lst[n-1]), b(lst[n-2]), mod2_add_rule))
        lst.pop()
        return element_add(lst)


def zzz(vector):
    """判断谷堆是否已空"""
    if vector.count(0) == 3:
        return True
    else:
        return False

def convert_int(num):
    """
    用来判断输入的是否是整数.

    int(3.2)结果为 3
    int('3')结果为 3
    int()微妙之处在于，int('3.2')会报错
    """
    try:
        return int(num) - 1
    except ValueError:
        return None

def judge_heap_num(vector, num):
    """
    判断所选谷堆的谷粒数量是否为0，是返回True
    """
    if vector[num] == 0:
        return True
    else:
        return False

# 用函数先判断输入是否合法
# 避免while循环条件很长
def judge_heap_input(entry, vector):
    """
    依次检查输入，输入不合法返回False，后面被while调用
    """
    if convert_int(entry) is None:
        print('输入内容非整数！请重新输入.')
        return False
    elif int(entry) not in [1, 2, 3]:
        print('找不到谷堆！请重新输入.')
        return False
    elif judge_heap_num(vector, convert_int(entry)):
        print('谷堆已空！请重新输入.')
        return False
    else:
        return True
        
def judge_grain_input(entry, vector, heap_num):
    if convert_int(entry) is None:
        print('输入内容非整数！请重新输入.')
        return False
    elif int(entry) not in [i+1 for i in range(vector[heap_num])]:
        print('抓取的数量有误！请重新输入.')
        return False
    else:
        return True

def select_difficulty():
    print(dedent("""
    请选择难度，输入
    easy or e ，下同
    normal  n 
    hard    h 
    lunatic l 
    """))
    in_hard = input('> ')
    if in_hard == 'easy' or in_hard == 'e':
        return 6, True
    elif in_hard == 'normal' or in_hard == 'n':
        return 10, True
    elif in_hard == 'hard' or in_hard == 'h':
        return 15, True
    elif in_hard == 'lunatic' or in_hard == 'l':
        return 25, True
    else:
        print("输入错误！")
        return -1, False


def main():

    print(dedent("""
    可爱的早苗邀请您一起玩游戏.
    这里有三个谷堆，每个谷堆都有一些数量的谷粒.
    两人轮流抓，一次只能抓一堆，最少抓一粒，可以全抓.
    您可以选择先抓与后抓.
    谁抓到最后一把谁赢."""))
    game = 0
    win = 0
    lost = 0
    max_grain, boolean = select_difficulty()
    while not boolean:
        max_grain, boolean = select_difficulty()

    while True:

        heap_grain = [7, 12, 11] # 测试用
        heap_grain = [randint(1, max_grain), randint(1, max_grain), randint(1, max_grain)]
        game += 1
        print(f'这是您的第 {game} 次游戏')
        print('游戏开始，现在 1-3 号谷堆的谷粒数量分别是', heap_grain)
        print('请选择先抓还是后抓，先抓输入1，后抓输入2')
        order = input('> ')
        while order != '1' and order != '2':
            print('请选择先抓还是后抓，先抓输入1，后抓输入2')
            order = input('> ')
        count = int(order) - 1 # 偶数玩家先抓

        while not zzz(heap_grain):
            if count % 2 == 0:
                print('----------------------------------------')
                print('到您抓了！')
                print('现在 1-3 号谷堆的谷粒数量分别是', heap_grain)
                print('要抓哪一堆谷物？输入1, 2 或 3, 输入down认输')
                
                heap = input('> ')
                while (heap != 'down') and (not judge_heap_input(heap, heap_grain)):
                    heap = input('> ')
                if heap == 'down':
                    break 

                heap = convert_int(heap)

                print(f'将在 {heap + 1} 号谷堆抓取，要抓多少谷粒？')
                grain = input('> ')
                while not judge_grain_input(grain, heap_grain, heap):
                    grain = input('> ')
                grain = int(grain)

                heap_grain[heap] -= grain # 更新谷堆数量
                print('现在 1-3 号谷堆的谷粒数量分别是', heap_grain)
                print('----------------------------------------')

                count += 1


            else:
                heap_grain_copy = heap_grain.copy()
                # 复制一份该列表，因为列表是可变对象，在函数里的列表就是全局的
                # 下面的函数会改变列表
                sum_grain = element_add(heap_grain_copy)
                if int(sum_grain) == 0:
                    # 这是必输情况
                    print('您一眼看穿此局，早苗认输了！')
                    break
                else:
                    # 这是必赢情况
                    # 列表的操作要小心，复制一份操作
                    print('早苗已经赢了，不信的话请继续玩下去.')
                    s = sorted(heap_grain)
                    flag = 0    # 遍历每个谷堆，找 模2和 全为0的情况，
                                # 找到了就用flag标记，防止在多个谷堆抓的情况
                    for i in range(len(heap_grain)):
                        index = heap_grain.index(s[i])
                        for j in range(1, s[i] + 1):
                            heap_grain_copy2 = heap_grain.copy()
                            heap_grain_copy2[index] -= j
                            if int(element_add(heap_grain_copy2)) == 0:
                                heap_grain[index] -= j
                                print(f'早苗在 {index + 1} 号谷堆抓取了 {j} 粒')
                                flag = 1
                                break
                        if flag == 1:
                            break

                count += 1

        if count % 2 == 0:
            print('----------------------------------------')
            print('早苗赢了！')
            lost += 1
        else:
            print('----------------------------------------')
            print('恭喜！您赢了！')
            win += 1

        print(f'您共进行了 {game} 次游戏，赢了 {win} 次 输了 {lost} 次')
        print('按 Ctrl+C 退出游戏.')
        print('----------------------------------------')
        print('****************************************')


if __name__ == '__main__':
    main()

# 原理：谷粒模2和全是0的一方先抓必输，因为抓完和必不全为0
# 对手只需再次抓到0，如此往复，必然对手抓到最后一把
