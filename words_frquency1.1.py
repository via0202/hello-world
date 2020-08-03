import jieba,csv,re,os
from time import perf_counter
from jieba import posseg

def get_files():  # 获取所有文件名称
    names=[file for file in os.listdir()\
           if file.endswith('.txt') ]
    print('需要处理{}个文件'.format(len(names)))
    return names

def words_frequency(name,n=10): # 统计词频
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
        if data[i][1]<n:  # 删除词频小于n的词语
            data=data[:i-1]
            break
        else:
            result=posseg.cut(data[i][0])  # 分析词性
            data[i]=list(data[i])
            for w,s in result:
                data[i].append(s)
    try:
        os.mkdir(os.path.join(os.path.dirname(name),'词频'))
    except:
        pass
    with open(os.path.join('词频',name.replace('.txt','.csv')),'w+',newline='') as F:  # 生成csv文件
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


