import jieba,csv,re,os
from time import perf_counter
from winsound import Beep
from jieba import posseg

def get_files():
    names=[file for file in os.listdir()\
           if file.endswith('.txt') and file != '2.使用说明.txt'\
           if file.replace('.txt','.csv') not in os.listdir('词频')]
    print('需要处理{}个文件'.format(len(names)))
    return names


def words_frequency(name,n=10):
    time=perf_counter()
    with open(name,encoding='utf-8') as F:
        s=F.read()
    s=re.sub(r'[\W]+','',s)
    ls=jieba.lcut(s)
    dic={}
    for w in ls:
        dic[w]=dic.get(w,0)+1
    data=list(dic.items())
    data.sort(key=lambda x:x[1],reverse=True)
    
    for i in range(len(data)):
        if data[i][1]<n:
            data=data[:i-1]
            break
        else:
            result=posseg.cut(data[i][0])
            data[i]=list(data[i])
            for w,s in result:
                data[i].append(s)

    with open(os.path.join('词频',name.replace('.txt','.csv')),'w+',newline='') as F:
        wt=csv.writer(F)
        wt.writerow(('词语','词频','词性'))
        wt.writerows(data)
        print('已生成文件:{},耗时{:.2f}秒'.format(name.replace('txt','csv'),perf_counter()-time))




names=get_files()
T=perf_counter()
if names!=[]:
    for name in names:        
        words_frequency(name,5)
    if len(names)>1:
        print('所有文件已处理,耗时{:.2f}'.format(perf_counter()-T))
else:
    print('没有需要处理的文件')
for i in range(5):            
    Beep(800,500)

