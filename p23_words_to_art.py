from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np

# 读取背景图片
path_img = "./materials/py_logo.png"
background_image = np.array(Image.open(path_img))

# 读取并用空格切分文本
words_txt = open('./materials/words.txt', 'r', encoding='UTF-8').read()
words_list = words_txt.split('\n')
cut_text = " ".join(words_list)

# 配置参数和初始WordCloud对象
wc = WordCloud(
    font_path="./materials/simhei.ttf",    # 设置中文字体
    repeat=True,                           # 允许文字重复
    random_state=42,                       # 随机种子
    mask=background_image,                 # 文字位置蒙版
    background_color='white',              # 背景颜色

).generate(cut_text)

# 生成颜色
image_colors = ImageColorGenerator(background_image)

# 绘图
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")  # 不显示x轴y轴刻度
plt.show()  # 显示图片
