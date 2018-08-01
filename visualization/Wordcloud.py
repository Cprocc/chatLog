# -*- coding=utf-8 -*-
import sys

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pymongo import MongoClient
from wordcloud import WordCloud, ImageColorGenerator


class wordcloud():
    def __init__(self):
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.word

    def close(self):
        self.client.close()

    def draw_wordcloud(self, word_dict, name):
        cat_mask = np.array(Image.open('../visualization/cat.png'))
        wc = WordCloud(font_path='../visualization/msyh.ttc',
                       width=800, height=400,
                       background_color="white",  # 背景颜色
                       mask=cat_mask,  # 设置背景图片
                       min_font_size=6
                       )
        wc.fit_words(word_dict)

        image_colors = ImageColorGenerator(cat_mask)
        # recolor wordcloud and show
        # we could also give color_func=image_colors directly in the constructor
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        plt.savefig('../photos/' + name + '.png', dpi=800)
        plt.close()

    def PL_wordcloud(self):
        word_dict = {'吴培森': ['阿毛','吴培森','老五'], '赵新诚': ['老赵','赵新诚','老六'], '李侨': ['李侨','儿子','老大'],
                     '李茂': ['茂哥','李茂','老二'], '柯泽冉': ['小三', '三儿','柯泽冉'], '祝博': ['老四','祝博']}
        self.draw_wordcloud(self.word_fre(word_dict), sys._getframe().f_code.co_name)

    def all_wordcloud(self, word_len=3):
        word_dict = {}
        stop_word = ['图片', '表情', '说','的','了','O']
        for doc in self.post.find({}):
            if len(doc['word']) > word_len and doc['word'] not in stop_word:
                word_dict[doc['word']] = doc['item']
        self.draw_wordcloud(word_dict, sys._getframe().f_code.co_name + str(word_len))

    def company_wordcloud(self):
        word_dict = {'华中科技大学': ['华科','华工'], '华中农业大学': ['华农','我农','皇家种地高中'], '大连理工大学': ['大连理工','大工'],
                      '武汉大学': ['武汉大学', '武大'],
                     '华中师范大学':['华中师范大学','华师'],'中南财经政法大学':['财大','中南财大','中南财经政法大学']}

        self.draw_wordcloud(self.word_fre(word_dict), sys._getframe().f_code.co_name)

    def word_fre(self, word_dict):
        word_fre = {}
        for key in word_dict.keys():
            word_fre[key] = 0

        res_dict = {}
        for doc in self.post.find({}):
            res_dict[doc['word']] = doc['item']

        for res_key in res_dict.keys():
            for word_key in word_dict.keys():
                if str(res_key).lower() in word_dict[word_key]:
                    word_fre[word_key] = word_fre[word_key] + res_dict[res_key]

        return word_fre

    def work(self):
        self.PL_wordcloud()
        self.company_wordcloud()
        self.all_wordcloud()


if __name__ == '__main__':
    word = wordcloud()
    word.all_wordcloud()
