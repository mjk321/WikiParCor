import re
import MeCab5
import os

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
DIR = os.path.join(os.getcwd(), LANG_PAIR+"\\data\\")
#os.makedirs(DIR)

with open(os.path.join(DIR,LANG_PAIR+'_2'+DES_LANG+'langArticlesWikitext.txt'), "r", encoding = 'utf-8') as f, \
open(os.path.join(DIR,LANG_PAIR+'_2'+DES_LANG+'langArticlesWikitext_cleaned.txt'), "w", encoding = 'utf-8') as f1:
    wakati = MeCab.Tagger("-Owakati")
    for line in f:
        line = re.sub(r'\[\d+\]','', line)
        line = re.sub(r'[^\w\s]','', line)
        if DES_LANG == "ja":
            line = wakati.parse(line)
        line = re.sub(r'\n+','', line)
        print(line, file = f1)
