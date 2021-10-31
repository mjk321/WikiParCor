import requests
import os
import re

S = requests.Session()

# https://ja.wikipedia.org/wiki/Category:ウィキペディア英語版から翻訳されたページ
# https://en.wikipedia.org/wiki/Category:Pages_translated_from_Polish_Wikipedia
# https://en.wikipedia.org/wiki/Category:Pages_translated_from_Arabic_Wikipedia
# https://en.wikipedia.org/wiki/Category:Pages_translated_from_Japanese_Wikipedia

CATEGORY = 'Category:ウィキペディア英語版から翻訳されたページ'    #category name. must be a category of translated pages from one language to another
SRC_LANG = "en" # source language language code (e.g. en  ja  ar  etc)
TGT_LANG = "ja" # target language language code (e.g. en  ja  ar  etc)
LANG_PAIR = SRC_LANG+"-"+TGT_LANG # language pair
DES_LANG = "ar"

# creating the directory where the files are saved
DIR = os.path.join(os.getcwd(), LANG_PAIR+"\\data\\")
#os.makedirs(DIR)

URL = "https://"+TGT_LANG+".wikipedia.org/w/api.php"
with open(os.path.join(DIR,LANG_PAIR+'_'+TGT_LANG+'ArticlesID.txt'), "r") as f, \
open(os.path.join(DIR,LANG_PAIR+'_'+TGT_LANG+'ArticlesWith_'+DES_LANG+'Lang.txt'), "w", encoding = 'utf-8') as f1:
    print(TGT_LANG+"_wiki_url_titles:\t"+DES_LANG+"_wiki_url_titles:", file = f1)
    for line in f:
        oldId = line.strip()
        PARAMS = {
        "action": "parse",
        "oldid": oldId,
        "prop": "langlinks|displaytitle",
        "format": "json"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        LN = []
        try:
            for x in DATA["parse"]["langlinks"]:
                LN.append(x)
            for y in LN:
                if DES_LANG == y["lang"]:
                    print(DATA["parse"]["displaytitle"]+"\t"+re.search('https://'+DES_LANG+'.wikipedia.org/wiki/(.*)', y["url"]).group(1), file = f1)
        except KeyError:
            print("KeyError")
