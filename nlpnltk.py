import os
import re
import nltk
import xlsxwriter

def lexical_diversity(text):
    return len(set(text))/len(text)


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

with open(os.path.join(DIR,LANG_PAIR+'_2'+DES_LANG+'langArticlesWikitext_cleaned.txt'), "r", encoding = 'utf-8') as f, \
open(os.path.join(DIR,LANG_PAIR+'_2'+DES_LANG+'langArticlesWikitext_tokens.txt'), "w", encoding = 'utf-8') as f1, \
xlsxwriter.Workbook(os.path.join(DIR,LANG_PAIR+'_2'+DES_LANG+'langArticlesWikitext_freqdist.xlsx')) as workbook:
    worksheet1 = workbook.add_worksheet()
    worksheet2 = workbook.add_worksheet()
    data = f.read()
    words = data.split()
    long_words = [w for w in set(words) if len(w) > 3]

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
