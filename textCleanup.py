import re
SRC_LANG = "en"
TGT_LANG = "ja"
LANG_PAIR = SRC_LANG+"-"+TGT_LANG
c = '\[(\d*)\]'

with open('data/'+LANG_PAIR+'_'+SRC_LANG+'cleantext.txt', 'w', encoding = 'utf-8') as f, open('data/'+LANG_PAIR+'_'+SRC_LANG+'ArticlesWikitext.txt', 'r', encoding = 'utf-8') as f1:
    for line in f1:
        a = line.startswith("This is an old revision")
        b = line.endswith("from the current revision.")
        if a and b:
            continue
        elif re.search(c, line):
            line.replace(c,'')
        print(line, file = f)
