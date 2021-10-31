from mwclient import Site
from pprint import pprint
import re
from bs4 import BeautifulSoup
import requests
import urllib
import MeCab
import nltk
import xlsxwriter
import os


def lexical_diversity(text):
    return len(set(text))/len(text) # calculates the lexical diversity of the text

def getArticleIds(lang, pair, category, dir):
    #retrieving the talk page pageids of the articles that contains the translation template in the category
    site = Site(lang+'.wikipedia.org')
    mw_page = site.pages[category]
    results = []
    for page in mw_page:
        results.append(str(page.pageid))    # retrieving the pageids in a list
    with open(os.path.join(dir,pair+'_pageid.txt'), 'w', encoding = 'utf-8') as f:
        print(results, file=f)

    #retrieving the oldids of the source articles (version) and the target articles (insert version) from the talk page pageids
    with open(os.path.join(dir,pair+'_pageid_version.txt'), 'w', encoding = 'utf-8') as f, \
    open(os.path.join(dir,pair+'_pageid_insertversion.txt'), 'w', encoding = 'utf-8') as g:
            for r in results:
                text = site.pages[int(r)].text()
                m = re.search('version=(\d*)', text)
                n = re.search('insertversion=(\d*)', text)
                if m and n:
                    version = m.group(1)
                    insertversion = n.group(1)
                    print(version, file=f)
                    print(insertversion, file=g)


    print("Number of Articles: "+str(len(results))) 

def cleanupIds(src, tgt, pair, dir):
    # removing the pairs with a versionid, a insertversion id or both missing
    with open(os.path.join(dir,pair+'_pageid_'+pair+'ids.txt'), 'w', encoding = 'utf-8') as f:
        print(src+" Articles ids"+"\t"+tgt+" Articles ids", file =f)
        with open(os.path.join(dir,pair+'_pageid_version.txt'), 'r') as f1, \
        open(os.path.join(dir,pair+'_pageid_insertversion.txt'), 'r') as f2:
                for line in f1:
                    line1 = line.strip()
                    line2 = f2.readline().strip()
                    if line1 and line2:
                        print(line1+'\t'+line2, file = f)
    #separating the oldids to individual files
    with open(os.path.join(dir,pair+'_pageid_'+pair+'ids.txt'), 'r') as f:
        for _ in range(1):
            next(f)
        with open(os.path.join(dir,pair+'_'+src+'ArticlesID.txt'), 'w', encoding = 'utf-8') as f1, \
        open(os.path.join(dir,pair+'_'+tgt+'ArticlesID.txt'), 'w', encoding = 'utf-8') as f2:
            for line in f:
                print(line.split('\t')[0], file = f1)
                print(line.split('\t')[1].strip('\n'), file = f2)

def getArticleTextsBS(src, tgt, pair, dir):
    getArticleTextBS(src, pair, dir)
    getArticleTextBS(tgt, pair, dir)

def getArticleTextBS(lang, pair, dir):
    #extracting the texts from the articles
    with open(os.path.join(dir,pair+"_"+lang+"ArticlesId.txt"), "r") as f, \
    open(os.path.join(dir,pair+"_"+lang+"ArticlesWikitext.txt"), "w", encoding = 'utf-8') as f1, \
    open(os.path.join(dir,pair+"_"+lang+"ArticlesKeyErrorIds.txt"), "w", encoding = 'utf-8') as e:
        for line in f:
            oldId = line.strip()
            res = requests.get("https://"+lang+".wikipedia.org/w/?oldid="+oldId)
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.find_all("p"):
                try:
                    text = cleanupText(item.text, lang)
                    print(text, file = f1)
                except KeyError:
                        print("KeyError\t"+oldId, file = e)

def getLangLinks(tgt, des, pair, dir):
    #extracting the titles of available articles of a desired language within the articles of the target language articles
    URL = "https://"+tgt+".wikipedia.org/w/api.php"
    S = requests.Session()
    with open(os.path.join(dir,pair+'_'+tgt+'ArticlesID.txt'), "r") as f, \
    open(os.path.join(dir,pair+'_'+tgt+'ArticlesWith_'+des+'Lang.txt'), "w", encoding = 'utf-8') as f1:
        print(tgt+"_wiki_url_titles:\t"+des+"_wiki_url_titles:", file = f1)
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
                    if des == y["lang"]:
                        print(DATA["parse"]["displaytitle"]+"\t"+re.search('https://'+des+'.wikipedia.org/wiki/(.*)', y["url"]).group(1), file = f1)
            except KeyError:
                print("KeyError")

def getDesArticleText(r, tgt, des, pair, dir):
    with open(os.path.join(dir,pair+'_'+tgt+'ArticlesWith_'+des+'Lang.txt'), "r", encoding = 'utf-8') as f, \
    open(os.path.join(dir,pair+'_2'+tgt+'langArticlesWikitext.txt'), "w", encoding = 'utf-8') as f1, \
    open(os.path.join(dir,pair+'_2'+des+'langArticlesWikitext.txt'), "w", encoding = 'utf-8') as f2 :
        for _ in range(1):
            next(f)
        count = 0
        for line in f:
            tgt_wordNum = 0
            des_wordNum = 0
            with open(os.path.join(dir,'temp1.txt'), "w", encoding = 'utf-8') as t1, \
            open(os.path.join(dir,'temp2.txt'), "w", encoding = 'utf-8') as t2 :
                res1 = requests.get("https://"+tgt+".wikipedia.org/wiki/"+urllib.parse.unquote(line.split('\t')[0].strip('\n')))
                res2 = requests.get("https://"+des+".wikipedia.org/wiki/"+urllib.parse.unquote(line.split('\t')[1].strip('\n')))
                soup1 = BeautifulSoup(res1.text, 'html.parser')
                soup2 = BeautifulSoup(res2.text, 'html.parser')

                for (item1, item2) in zip(soup1.find_all("p"), soup2.find_all("p")):
                    try:
                        text = cleanupText(item1.text, tgt)
                        print(text, file = t1)
                        tgt_wordNum += len(text.split())

                        text = cleanupText(item2.text, des)
                        print(text, file = t2)
                        des_wordNum += len(text.split())
                    except KeyError:
                        print("KeyError")

            with open(os.path.join(dir,'temp1.txt'), "r", encoding = 'utf-8') as t1, \
            open(os.path.join(dir,'temp2.txt'), "r", encoding = 'utf-8') as t2 :
                try:
                    print("tgt word count: " +str(tgt_wordNum)+ "; des word count: " +str(des_wordNum))
                    ratio = tgt_wordNum/des_wordNum
                    print("ratio: "+ str(ratio))

                    if (r-0.5) < ratio < (r+0.5):
                        count += 1
                        for (line1, line2) in zip(t1, t2):
                            print(line1, file = f1)
                            print(line2, file = f2)

                except ZeroDivisionError:
                    print("dividing by zero!")

    with open(os.path.join(dir,'articleCount.txt'), "w", encoding = 'utf-8') as c:
        c.write(str(count))

def cleanupText(txt, lang):
    wakati = MeCab.Tagger("-Owakati")
    txt = re.sub(r'\[\d+\]','', txt)
    txt = re.sub(r'[^\w\s]','', txt)

    if lang == "ja":
        txt = wakati.parse(txt)

    txt = re.sub(r'\n+','', txt)
    return txt

def someStats(src, tgt, pair, dir):
    someStatistics(src, pair, dir)
    someStatistics(tgt, pair, dir)

def someStatistics(lang, pair, dir):
    with open(os.path.join(dir,pair+"_"+lang+"ArticlesWikitext.txt"), "r", encoding = 'utf-8') as f, \
    open(os.path.join(dir,pair+"_"+lang+"ArticlesWikitext_tokens.txt"), "w", encoding = 'utf-8') as f1, \
    xlsxwriter.Workbook(os.path.join(dir,pair+'_'+lang+'ArticlesWikitext_freqdist.xlsx')) as workbook:
        worksheet1 = workbook.add_worksheet()
        worksheet2 = workbook.add_worksheet()
        data = f.read()
        words = data.split()
        long_words = [w for w in set(words) if len(w) > 3]

        print("----"+pair+" pair, "+lang+" articles----")
        print("number of words: "+str(len(words)))
        print("number of distinct/unique words: "+str(len(set(words))))
        print("lexical diversity: "+ str(lexical_diversity(words)))
        fdist1 = nltk.FreqDist(words)
        lwords = []
        for v in long_words:
            lwords.append([v, fdist1[v]])
        print(fdist1)
        for row_num, data in enumerate(sorted(lwords, key = lambda x:x[1], reverse = True)):
            worksheet1.write_row(row_num, 0, data)
        for row_num, data in enumerate(sorted(fdist1.most_common(), key = lambda x:x[1], reverse = True)):
            worksheet2.write_row(row_num, 0, data)
        print(set(words), file = f1)
        print("___________________________________________________________________")

##############################################################################################
# https://ja.wikipedia.org/wiki/Category:ウィキペディア英語版から翻訳されたページ
# https://en.wikipedia.org/wiki/Category:Pages_translated_from_Polish_Wikipedia
# https://en.wikipedia.org/wiki/Category:Pages_translated_from_Arabic_Wikipedia
# https://en.wikipedia.org/wiki/Category:Pages_translated_from_Japanese_Wikipedia


CATEGORY = 'Category:ウィキペディア英語版から翻訳されたページ'    #category name. must be a category of translated pages from one language to another
SRC_LANG = "en" # source language language code (e.g. en  ja  ar  etc)
TGT_LANG = "ja" # target language language code (e.g. en  ja  ar  etc)
LANG_PAIR = SRC_LANG+"-"+TGT_LANG # language pair
DES_LANG = "ar" # desired Language Language code (language code for a desired language version of extracted articles)
WRD_RATIO = 1.543156 # word number ratio (Tanzil ar-ja's Japanese word number-to-Arabic word number's ratio in this case)
# creating the directory where the files are saved
DIR = os.path.join(os.getcwd(), LANG_PAIR+"\\data\\")
try:
    os.makedirs(DIR)
except FileExistsError:
    print(DIR+" already exists")

#getArticleIds(TGT_LANG, LANG_PAIR, CATEGORY, DIR)
#cleanupIds(SRC_LANG, TGT_LANG, LANG_PAIR, DIR)
#getArticleTextsBS(SRC_LANG, TGT_LANG, LANG_PAIR, DIR)
#someStats(SRC_LANG, TGT_LANG, LANG_PAIR, DIR)


#optional
#getLangLinks(TGT_LANG, DES_LANG, LANG_PAIR, DIR)
getDesArticleText(WRD_RATIO, TGT_LANG, DES_LANG, LANG_PAIR, DIR)
