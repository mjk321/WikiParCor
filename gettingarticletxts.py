import requests
import re
import os
import urllib
import wikipedia

S = requests.Session()

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

URL = "https://"+TGT_LANG+".wikipedia.org/w/api.php"

with open(os.path.join(DIR,LANG_PAIR+'_'+TGT_LANG+'ArticlesWith_arLang.txt'), "r", encoding = 'utf-8') as f, \
open(os.path.join(DIR,LANG_PAIR+'_2'+TGT_LANG+'langArticlesWikitext.txt'), "w", encoding = 'utf-8') as f1:
    for _ in range(1):
        next(f)
    for line in f:
        title = line.split('\t')[0].strip('\n')
        PARAMS = {
        "action": "parse",
        "page": urllib.parse.unquote(title),
        "prop": "wikitext",
        "format": "json"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        try:
            print(DATA["parse"]["wikitext"]["*"], file = f1)
        except KeyError:
                print("KeyError")
