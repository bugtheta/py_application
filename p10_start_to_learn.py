# 第一段python程序
print("好好学习 天天向上")

# 运算
# 可以直接在Python Console输入代码并一句句的执行
# Console会展示出最后一条的结果
1 + 1

1 + 2

1 + 3

# 在编程语言里面 符号大多数有特别的用处
# 常见的的算术运算符号使用如下
print("1 + 4 = ", 1 + 4)  # + 相加
print("1 - 4 = ", 1 - 4)  # + 相减
print("2 * 3 = ", 2 * 3)  # * 相乘
print("2 ** 3 = ", 2 ** 3)  # ** 乘方
print("9 / 3 = ", 9 / 3)  # / 相除
print("10 // 3 = ", 10 // 3)  # // 整除
print("10 % 3 = ", 10 % 3)  # % 求余

# 数据类型
# 不同类型的数据会影响它们之间是否可以进行运算
# 以及是否会被转换
print(99999)  # int 整型
print(1.0333)  # float 浮点型
print("天气真好")  # str 字符串
print(True)  # bool 布尔值
print(9 / 3)  # / 相除的结果会被转换为float

# 变量
a = 1 + 1.0
b = 2 * 3
c = a + b
print("c的值是:", c)

x = "天气真好"
y = " 想出去玩"
z = x + y
print(z)

# 条件语句
dayofweek = 6
if dayofweek < 6:
    print("要早起")
else:
    print("睡到自然醒")

# 条件语句 else if
dayofweek = 7
if dayofweek < 6:
    print("要早起")
elif dayofweek == 6:
    print("睡到自然醒")
elif dayofweek == 7:
    print("起来学英语")

# 循环语句
# for 结构
words = 0  # 一开始掌握的单词数为0
for i in range(7):  # 如果i在[0,7)的范围内
    words += 5  # 每天学习5个单词
    print("现在是第%d天， 我学会了%g个单词" % (i, words))

# while 结构
words = 0
day_counter = 0
while day_counter < 7:
    words += 5
    day_counter += 1
    print("现在是第%d天， 我学会了%g个单词" % (day_counter, words))

# while 死循环
# words = 0
# day_counter = 0
# while True:
#     words += 1
#     day_counter += 1
#     print("现在是第%d天， 我学会了%g个单词" % (day_counter, words))

# 容器
a_list = [4, 3, 5]  # 定义和初始化一个list
print("定义了列表", a_list)
print("第一个元素", a_list[0])  # 选取list内的第一个元素
print("最后一个元素", a_list[-1])  # 选取list内的最后一个元素
a_list.sort()  # 对list内部的元素进行排序
print("排序之后", a_list)
a_list.append(99)  # 加入一个元素到list末尾
print("执行append之后", a_list)
a_list.pop()  # 把list末尾最后一个元素去除
print("执行pop之后", a_list)

# 函数
# y=f(x) 实现对一定规则的运算过程的封装
b_list = [-45, 4.3, 2, 3, 5, 33, 55]
print("b_list", b_list)
print("求和", sum(b_list))
print("求最大值", max(b_list))
print("求最小值", min(b_list))
print("求b_list[0]绝对值", abs(-b_list[0]))
print("将b_list[1]数据类型转为整型", int(b_list[1]))


# 自定义函数
def what_to_go(dow):
    plan = '计划中'  # 定义一个字符串

    # 通过输入的变量dow来进行条件判断
    if dow < 6:
        plan = "今天忙着建设社会主义"
    elif dow == 6:
        plan = "今天想去吃薯条和炸鸡"
    else:
        plan = "有没有人一起出去玩"

    return plan  # 返回plan的值


my_plan_5 = what_to_go(dow=5)
my_plan_6 = what_to_go(dow=6)
my_plan_7 = what_to_go(dow=7)
print("周五的计划是", my_plan_5)
print("周六的计划是", my_plan_6)
print("周日的计划是", my_plan_7)

# 标准库
import math  # 导入math数学库

print("pi的值是", math.pi)
print("求sin90度", math.sin(math.pi / 2))
help(math.sin)  # 查看文档

# 写出数据到文本文件
file = open('./output/mytext.txt', 'w')  # w 声明写出模式
mytext = "今天吃什么"
file.write(mytext)  # 将字符串mytext写出至mytext.txt
file.close()  # 关闭文件

# 从文件读取
file = open('./output/mytext.txt', 'r')  # r 声明读取模式
text_load = file.read()
print(text_load)
