from bs4 import BeautifulSoup
import requests

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

with open(os.path.join(dir,pair+"_"+lang+"ArticlesId.txt"), "r") as f, \
open(os.path.join(dir,pair+"_"+lang+"ArticlesWikitext.txt"), "w", encoding = 'utf-8') as f1, \
open(os.path.join(dir,pair+"_"+lang+"ArticlesKeyErrorIds.txt"), "w", encoding = 'utf-8') as e:
    for line in f:
        oldId = line.strip()
        res = requests.get("https://"+LANG+".wikipedia.org/w/?oldid="+oldId)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.find_all("p"):
            try:
                print(item.text, file = f1)
            except KeyError:
                    print("KeyError\t"+oldId, file = e)
