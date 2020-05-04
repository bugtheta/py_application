import os
import glob
import pandas as pd
from docx import Document
import re
import thulac
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


# 函数
def draw_words_to_art(text_dict: dict, bg_pic='py_logo', seed=42):
    '''
    :param text_dict: {term:frequency}
    :param bg_pic: name of your png
    :param seed: random seed
    :return: None
    '''
    path_img = "./materials/" + bg_pic + ".png"

    background_image = np.array(Image.open(path_img))

    wc = WordCloud(
        font_path="./materials/simhei.ttf",  # 设置中文字体
        # repeat=True,  # 允许文字重复
        repeat=False,  # 允许文字重复
        random_state=seed,  # 随机种子
        mask=background_image,  # 文字位置蒙版
        background_color='white',  # 背景颜色
        max_words=500,
    ).generate_from_frequencies(text_dict)

    image_colors = ImageColorGenerator(background_image)
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.show()


# ----- step1 将表格全部移动在一起 -----
# https://docs.python.org/zh-cn/3.7/library/glob.html
xlsx_list = glob.glob('./materials/编程语言报名表/**/*.xlsx', recursive=True)
docx_list = glob.glob('./materials/编程语言报名表/**/*.docx', recursive=True)

for xlsx in xlsx_list:
    # 替换处理掉一下shell下需要转义的字符
    xlsx = xlsx.replace(' ', '\ ')
    xlsx = xlsx.replace('(', '\(')
    xlsx = xlsx.replace(')', '\)')
    xlsx = xlsx.replace('&', '\&')
    xlsx_name = xlsx.split('/')[-1]

    # 生产复制名利的字符串
    cmd = 'cp ' + xlsx + ' ./materials/xlsx/'

    # 给重复命名的文件重命名 不然会覆盖丢失文件
    if os.path.exists(xlsx):
        cmd += xlsx_name.strip('.xlsx') + '_copy.xlsx'

    # 利用os输出shell命令
    os.system(cmd)
    # cp /old_path/xxxx.xlsx /new_path/

    # 利用shutil模块也可以进行复制
    # https://docs.python.org/3.7/library/shutil.html

for docx in docx_list:
    docx = docx.replace(' ', '\ ')
    docx = docx.replace('(', '\(')
    docx = docx.replace(')', '\)')
    docx = docx.replace('&', '\&')

    docx_name = docx.split('/')[-1]

    cmd = 'cp ' + docx + ' ./materials/docx/'

    # 给重复命名的文件重命名 不然会覆盖丢失文件
    if os.path.exists(docx):
        cmd += docx_name.strip('.docx') + '_copy.docx'
    os.system(cmd)

# ----- step2 数据汇总和处理 -----

xlsx_list = glob.glob('./materials/xlsx/*.xlsx')
docx_list = glob.glob('./materials/docx/*.docx')

# 合并excel的数据
df_list = []

for xlsx in xlsx_list:
    try:
        df = pd.read_excel(xlsx, sheet_name=0, skiprows=1)
        df_list.append(df)
    except:
        print('!!!!Somethings wrong with ', xlsx)

df_all = pd.concat(df_list, axis=0)

# 简单的统计数据
print("总共有报名表 {}".format(len(df_all)))
print("报名人数top10的单位:")
df_gp = df_all.groupby('单位')['单位'].count().sort_values(ascending=False)
print(df_gp.head(10))

# ----- step3 文本读取和分析 -----

# 合并words的数据
doc_text_list = []
all_text = ''

for docx in docx_list:
    # docx = docx_list[0]
    document = Document(docx)

    this_text = ''

    for para in document.paragraphs:
        this_text += para.text + '\n'

    doc_text_list.append(this_text)
    all_text += this_text

# 文本清理 去掉题目
# 将题目string用q1和q2表示
q1 = ''
q2 = ''

all_text = all_text.replace(q1, ' ')
all_text = all_text.replace(q2, ' ')

# 去除标点和换行
all_text = all_text.replace('。', ' ')
all_text = all_text.replace('\n', ' ')
all_text = all_text.replace('、', ' ')
all_text = all_text.replace('）', ' ')
all_text = all_text.replace('（', ' ')
all_text = all_text.replace('-', ' ')
all_text = all_text.replace('一', ' ')
all_text = all_text.replace('；', ' ')
all_text = all_text.replace('。', ' ')

# 分词
# i am eating things. 4 words
# 我 正在 吃东西.  6 characters to 3 words
# http://thulac.thunlp.org/
thu1 = thulac.thulac(seg_only=True, filt=True)
cut_text = thu1.cut(all_text, text=True)
cut_text_list = cut_text.split(" ")

# 统计词频
words_counter = {}
for word in cut_text_list:
    if len(word) <= 1:
        continue  # 排除单字和标点

    if word not in words_counter:
        words_counter[word] = 1
    else:
        words_counter[word] += 1

words_counter_list = list(zip(words_counter.keys(), words_counter.values()))
words_counter_list.sort(key=lambda x: x[1], reverse=True)
print(words_counter_list[:20])  # 打印刷选出的top20词频的词汇

# 绘制词云
# draw_words_to_art(words_counter, 'Squirtle')

# --------------
# 找到一些重要的词汇
# 计算TF-IDF
# tf
tf_dict = {}
total_words = len(cut_text_list)
for key, value in words_counter.items():
    tf_dict[key] = value * 1.0 / total_words

# idf
all_text_2 = '_^^_'.join(doc_text_list)
all_text_2 = all_text_2.replace(q1, ' ')
all_text_2 = all_text_2.replace(q2, ' ')
doc_text_list_2 = all_text_2.split('_^^_')

idf_dict = {}
for j, word in enumerate(tf_dict.keys()):

    if j % 200 == 0:
        print('{}/{}'.format(j, len(tf_dict)))

    idf_counter = 0
    for doc_txt in doc_text_list_2:
        if re.search(re.escape(word), doc_txt):
            idf_counter += 1
    idf_dict[word] = np.log(len(doc_text_list_2) * 1.0 / (idf_counter + 1))

# tf_idf
tf_idf_dict = {}

for word in tf_dict.keys():
    tf_idf = tf_dict[word] * idf_dict[word]
    tf_idf_dict[word] = tf_idf

tf_idf_list = list(zip(tf_idf_dict.keys(), tf_idf_dict.values()))
tf_idf_list.sort(key=lambda x: x[1], reverse=True)
print(tf_idf_list[:20])

# draw_words_to_art(tf_idf_dict, 'Bulbasaur', seed=0)
