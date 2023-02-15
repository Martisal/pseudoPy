import json

with open('/home/saletta/datasets/code-to-text/python/train.jsonl', 'r') as jf:
    jsl = jf.readlines()
    #jobj = jf.read()
    

jstr = '[\n'

for i in range(len(jsl)-1):
    jstr += jsl[i][:-1] + ',\n'

jstr += jsl[len(jsl)-1][:-1] + '\n]'
js = json.loads(jstr)

py = open('train_py_fun', 'w')
en = open('train_py_en', 'w')

for j in js:
    docstring = ''
    for i in range(len(j['docstring_tokens'])):
        docstring += j['docstring_tokens'][i] + ' '

    code = j['code'].replace('\n', '\\n')    
        
    py.write(code + '\n')
    en.write(docstring[:-1] + '\n')

py.close()
en.close()
