import untils.generate_fake_data as gen

# 产生csv数据
# gen.one_fake()
# gen.many_fake(nums=20)


# 1 利用open的方式读取csv数据
file = open('./fake_data/fake_data.csv')
my_csv = file.read()  # 直接读取所有文本

# 用换行切分文本
my_csv_lines = my_csv.split('\n')
# 用逗号再次切分文本
my_csv_2d = []  # 二维列表存储数据
for i in range(len(my_csv_lines)):
    one_line_list = my_csv_lines[i].split(',')
    my_csv_2d.append(one_line_list)

print(my_csv_2d[0][0])  # 第一行第一列, city字段
print(my_csv_2d[1][0])  # 第二行第一列
my_csv  # 文本中的\n表示换行

# 2 利用pandas内置方法直接读取csv
import pandas as pd

my_csv_df = pd.read_csv('./fake_data/fake_data.csv')
print(my_csv_df['city'][0])  # 直接读取city字段的第一个数据
print(my_csv_df.head(10))  # 打印前10行的数据

# 3 合并多个csv
import glob

# 用glob和通配符*获得文件夹下所有csv的路径
all_test_paths = glob.glob('./fake_data/fake_data_*.csv')
csv_list = []  # 定义list来存放多个csv

for path in all_test_paths:
    tmp_df = pd.read_csv(path)
    csv_list.append(tmp_df)
    print(path.split('/')[-1], 'has %d lines' % len(tmp_df))

# 将所有list内的csv连接成一整个csv
# axis=0表示行的方向进行连接 类似SQL里的union all
all_in_one_df = pd.concat(csv_list, axis=0)
print('all in one has %d lines' % len(all_in_one_df))
all_in_one_df.to_csv('./output/fake_data_one.csv')

# 4 绘制数据图
import matplotlib.pyplot as plt

# 对数据进行聚合，得到每天的price的最小值
min_group = all_in_one_df.groupby('date')['price'].min()
# 绘制散点图 详细参数配置建议参考文档
plt.plot(min_group.index, min_group.values, 'x-')
# x轴标签旋转
plt.xticks(rotation=90)
# 绘制图像
plt.show()
