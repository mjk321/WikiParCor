import MeCab
import os
import re

wakati = MeCab.Tagger("-Owakati")

SRC_LANG = "en"
TGT_LANG = "ja"
LANG_PAIR = SRC_LANG+"-"+TGT_LANG
LANG = TGT_LANG

# https://ja.wikipedia.org/wiki/Category:ウィキペディア英語版から翻訳されたページ
# https://en.wikipedia.org/wiki/Category:Pages_translated_from_Polish_Wikipedia
# https://en.wikipedia.org/wiki/Category:Pages_translated_from_Arabic_Wikipedia
# https://en.wikipedia.org/wiki/Category:Pages_translated_from_Japanese_Wikipedia

CATEGORY = 'Category:ウィキペディア英語版から翻訳されたページ'    #category name. must be a category of translated pages from one language to another
SRC_LANG = "en" # source language language code (e.g. en  ja  ar  etc)
TGT_LANG = "ja" # target language language code (e.g. en  ja  ar  etc)
LANG_PAIR = SRC_LANG+"-"+TGT_LANG # language pair
DES_LANG = "ar" # desired language language code (e.g. en  ja  ar  etc)

# creating the directory where the files are saved
DIR = os.getcwd()
#os.makedirs(DIR)
counter = [0]*114
with open(os.path.join(DIR,'ja.Tanzil simple ar-ja.txt'), "r", encoding = 'utf-8') as f, \
open(os.path.join(DIR,'ja.Tanzil simple ar-ja Mecab.txt'), "w", encoding = 'utf-8') as f1:
    for line in f:
        try:
            line = re.sub(r'[。（）・，「」〔〕()?]', '', line)
            result = re.search(r"\d+", line)
            line1 = re.search(r"\d+\|\d+\|", line)
            line2 = re.sub(r"\d+\|\d+\|","",line)
            line3 = wakati.parse(line2)
            if line1:
                line4 = line1.group(0) + line3
                counter[int(result.group(0))-1] += len(wakati.parse(line2).split())
            else:
                line4 = line3
        except KeyError as e:
            print('KeyError')
        line4 = re.sub(r'\n+','', line4)
        print(line4, file = f1)
with open(os.path.join(DIR, 'ja_counter.txt'), 'w', encoding = 'utf-8') as f:
    print(counter, file = f)
