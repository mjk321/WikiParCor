from mwclient import Site
from pprint import pprint
import re
#https://ja.wikipedia.org/wiki/Category:ウィキペディア英語版から翻訳されたページ
#https://ar.wikipedia.org/wiki/تصنيف:جميع_الصفحات_التي_بحاجة_لاستكمال_الترجمة


#retrieving the talk page pageids of the articles that contains the translation template in the category
site = Site('ja.wikipedia.org')
mw_page = site.pages['Category:ウィキペディア英語版から翻訳されたページ']
results = []
for page in mw_page:
    results.append(str(page.pageid))
with open('data/en-ja_pageid.txt', 'w', encoding = 'utf-8') as f:
    print(results, file=f)

#retrieving the oldids of the source articles (version) and the target articles (insert version) from the talk page pageids
with open('data/en-ja_pageid_version.txt', 'w', encoding = 'utf-8') as f, open('data/en-ja_pageid_insertversion.txt', 'w', encoding = 'utf-8') as g:
        for r in results:
            text = site.pages[int(r)].text()
            m = re.search('version=(\d*)', text)
            n = re.search('insertversion=(\d*)', text)
            if m and n:
                version = m.group(1)
                insertversion = n.group(1)
                print(version, file=f)
                print(insertversion, file=g)


print(len(results))



#https://ja.wikipedia.org/wiki/Category:ウィキペディア英語版から翻訳されたページ
#https://ar.wikipedia.org/wiki/تصنيف:جميع_الصفحات_التي_بحاجة_لاستكمال_الترجمة
#https://ar.wikipedia.org/wiki/تصنيف:مقالات_مترجمة_آليا
