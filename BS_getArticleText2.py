from bs4 import BeautifulSoup
import urllib
import requests
import MeCab
import re
import os

def cleanupText(txt, lang):
    wakati = MeCab.Tagger("-Owakati")
    txt = re.sub(r'\[\d+\]','', txt)
    txt = re.sub(r'[^\w\s]','', txt)

    if lang == "ja":
        txt = wakati.parse(txt)

    txt = re.sub(r'\n+','', txt)
    return txt

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
goodDIR = os.path.join(os.getcwd(), LANG_PAIR+"\\data\\goodArticles\\")
badDIR = os.path.join(os.getcwd(), LANG_PAIR+"\\data\\badArticles\\")
if not os.path.exists(DIR):
    print(DIR + " does not exist!")
    os.makedirs(DIR)
if not os.path.exists(goodDIR):
    print(goodDIR + " does not exist!")
    os.makedirs(goodDIR)
if not os.path.exists(badDIR):
    print(badDIR + " does not exist!")
    os.makedirs(badDIR)


with open(os.path.join(DIR,LANG_PAIR+'_'+TGT_LANG+'ArticlesWith_'+DES_LANG+'Lang.txt'), "r", encoding = 'utf-8') as f, \
open(os.path.join(DIR,'log.txt'), "w", encoding = 'utf-8') as t3:
    for _ in range(1):
        next(f)
    goodCount = 0
    badCount = 0
    for line in f:
        tgt_wordNum = 0
        des_wordNum = 0
        with open(os.path.join(DIR,'temp1.txt'), "w", encoding = 'utf-8') as t1, \
        open(os.path.join(DIR,'temp2.txt'), "w", encoding = 'utf-8') as t2 :
            res1 = requests.get("https://"+TGT_LANG+".wikipedia.org/wiki/"+urllib.parse.unquote(line.split('\t')[0].strip('\n')))
            res2 = requests.get("https://"+DES_LANG+".wikipedia.org/wiki/"+urllib.parse.unquote(line.split('\t')[1].strip('\n')))
            soup1 = BeautifulSoup(res1.text, 'html.parser')
            soup2 = BeautifulSoup(res2.text, 'html.parser')

            for (item1, item2) in zip(soup1.find_all("p"), soup2.find_all("p")):
                try:
                    text = cleanupText(item1.text, TGT_LANG)
                    print(text, file = t1)
                    tgt_wordNum += len(text.split())

                    text = cleanupText(item2.text, DES_LANG)
                    print(text, file = t2)
                    des_wordNum += len(text.split())
                except KeyError:
                    print("KeyError")

        with open(os.path.join(DIR,'temp1.txt'), "r", encoding = 'utf-8') as t1, \
        open(os.path.join(DIR,'temp2.txt'), "r", encoding = 'utf-8') as t2:
            try:
                ratio = tgt_wordNum/des_wordNum

                if 2.515213223 < ratio < 3.157300957:
                    goodCount += 1
                    with open(os.path.join(goodDIR,str(goodCount)+") "+LANG_PAIR+'_2'+TGT_LANG+'langArticlesWikitext.txt'), "w", encoding = 'utf-8') as f1, \
                    open(os.path.join(goodDIR,str(goodCount)+") "+LANG_PAIR+'_2'+DES_LANG+'langArticlesWikitext.txt'), "w", encoding = 'utf-8') as f2 :
                        for (line1, line2) in zip(t1, t2):
                            print(line1, file = f1)
                            print(line2, file = f2)

                else:
                    badCount += 1
                    with open(os.path.join(badDIR,str(badCount)+") "+LANG_PAIR+'_2'+TGT_LANG+'langArticlesWikitext.txt'), "w", encoding = 'utf-8') as f1, \
                    open(os.path.join(badDIR,str(badCount)+") "+LANG_PAIR+'_2'+DES_LANG+'langArticlesWikitext.txt'), "w", encoding = 'utf-8') as f2 :
                        for (line1, line2) in zip(t1, t2):
                            print(line1, file = f1)
                            print(line2, file = f2)

                t3.write("article "+str(goodCount+badCount)+": tgt word count: " +str(tgt_wordNum)+ "; des word count: " +str(des_wordNum)+ "\nratio: "+ str(ratio) +"\n")
            except ZeroDivisionError:
                print("dividing by zero!")


with open(os.path.join(DIR,'articleCount.txt'), "w", encoding = 'utf-8') as c:
    c.write("good articles: "+str(goodCount)+"\t bad articles: "+str(badCount))
