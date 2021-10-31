SRC_LANG = "en"
TGT_LANG = "ja"
LANG_PAIR = SRC_LANG+"-"+TGT_LANG

# removing the pairs with a versionid, a insertversion id or both missing
with open('data/'+LANG_PAIR+'_pageid_'+LANG_PAIR+'ids.txt', 'w', encoding = 'utf-8') as f:
    print("English Articles ids"+"\t"+"Japanese Articles ids", file =f)
    with open('data/'+LANG_PAIR+'_pageid_version.txt', 'r') as f1, open('data/'+LANG_PAIR+'_pageid_insertversion.txt', 'r') as f2:
            for line in f1:
                line1 = line.strip()
                line2 = f2.readline().strip()
                if line1 and line2:
                    print(line1+'\t'+line2, file = f)

with open('data/'+LANG_PAIR+'_pageid_'+LANG_PAIR+'ids.txt', 'r') as f:
    for _ in range(1):
        next(f)
    with open('data/'+LANG_PAIR+'_'+SRC_LANG+'ArticlesID.txt', 'w', encoding = 'utf-8') as f1, open('data/'+LANG_PAIR+'_'+TGT_LANG+'ArticlesID.txt', 'w', encoding = 'utf-8') as f2:
        for line in f:
            print(line.split('\t')[0], file = f1)
            print(line.split('\t')[1].strip('\n'), file = f2)
