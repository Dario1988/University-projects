
# Part 1.1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ground_truth=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_1_1/part_1_1__Ground_Truth.tsv',delimiter='\t')
se1=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_1_1/part_1_1__Results_SE_1.tsv',delimiter='\t')
se2=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_1_1/part_1_1__Results_SE_2.tsv',delimiter='\t')
se3=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_1_1/part_1_1__Results_SE_3.tsv',delimiter='\t')

# a bit of descriptive statistics on the search engine
se1.describe()
se2.describe()
se3.describe()

# Function to convert in dict
def dicti(file):
    se1_dicti={}
    for i in range(0,len(file)):
        c=file[i][1]
        key=file[i][0]
        se1_dicti[key]=[j for j in c]
    return se1_dicti

# Change structure do data
# trasfrom ground truth in a dictionary structure:
# {query_1:[doc_id],...,query_n:[doc_id]}
lista=list(ground_truth.groupby('Query_id')['Relevant_Doc_id'])
query=[]
for i in ground_truth['Query_id']:
    query.append(i)
sort_query=sorted(set(query))

#ground truth in dictionary
ground_truth_dict={}
for i in range(0,len(sort_query)):
    c=lista[i][1]
    key=lista[i][0]
    ground_truth_dict[key]=[j for j in c]
    
# ### we do the same for the search engines
# **dictionary for search engine 1,2 and 3**
se1=list(se1.groupby('Query_ID')['Doc_ID'])
se2=list(se2.groupby('Query_ID')['Doc_ID'])
se3=list(se3.groupby('Query_ID')['Doc_ID'])
se1_dict=dicti(se1)
se2_dict=dicti(se2)
se3_dict=dicti(se3)

# So now we can compute a bit of statistics on the data
import matplotlib.pyplot as plt


# N° of docs in each query 
ground_len={}
for i,j in ground_truth_dict.items():
    ground_len[i]=len(j)

x=list(ground_truth_dict.keys())
y=ground_len.values()
plt.bar(x, y)
plt.xlabel('Query id')
plt.ylabel('n° docs')
plt.title('docs for each query in the Gt')
plt.savefig('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_1_1/output_data/barplot_gt.png')
plt.show()

# Function that create dataframe for p@k
def dataframe(ground_truth_dict,a): 
    pat=[]
    for i in range(1,4):
        c=pat_key(globals()['se%s_dict' % i],ground_truth_dict,a)
        pat.append(c)
    return pat


# Precision P@k
def pat_key(search_engine,gr,v):
    pat=[]
    count=0
    for k in search_engine.keys():
        if k in gr.keys():
            for value in range(0,v):
                if search_engine[k][value] in gr[k]:
                    count+=1
            pat.append(count/min(v,len(gr[k])))
        count=0
    return np.mean(pat)
pa1_se_result=dataframe(ground_truth_dict,1)
pa3_se_result=dataframe(ground_truth_dict,3)
pa5_se_result=dataframe(ground_truth_dict,5)
pa10_se_result=dataframe(ground_truth_dict,10)

from pandas import DataFrame
Pat = DataFrame({'Search engine': ['SE_1','SE_2','SE_3']})
Pat['mean(P@1)']=pa1_se_result
Pat['mean(P@3)']=pa3_se_result
Pat['mean(P@5)']=pa5_se_result
Pat['mean(P@10)']=pa10_se_result
Pat.set_index(['Search engine'])

Pat.to_csv('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_1_1/output_data/p@k.csv',index=False)


#Recall
def rec(search_engine,gr):
    pat=[]
    count=0
    for k in search_engine.keys():
        if k in gr.keys():
            for value in range(0,len(gr[k])):
                if search_engine[k][value] in gr[k]:
                    count+=1
            pat.append(count/len(gr[k]))
        count=0
    return np.mean(pat),min(pat),np.percentile(pat,25),np.median(pat),np.percentile(pat,75),max(pat)
R1=['SE_1']
for i in rec(se1_dict,ground_truth_dict):
    R1.append(i)
R2=['SE_2']
for i in rec(se2_dict,ground_truth_dict):
    R2.append(i)
R3=['SE_3']
for i in rec(se3_dict,ground_truth_dict):
    R3.append(i)
Recall=pd.DataFrame(data=[R1,R2,R3],columns=['Search engine','Mean(R-Precision_Distrbution)','min(R-Precision_Distrbution)','1°_quartile (R-Precision_Distrbution)','MEDIAN(R-Precision_Distrbution)','3°_quartile (R-Precision_Distrbution)','MAX(R-Precision_Distrbution)'])
Recall.set_index(['Search engine'])
Recall.to_csv('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_1_1/output_data/r_precision.csv',index=False)


# MRR
def mrr(search_engine,gr):
    count=0
    pat=[]
    for k in search_engine.keys():
        if k in gr.keys():
            for value in range(0,len(search_engine[k])):
                if search_engine[k][value] in gr[k]:
                    index=search_engine[k].index(search_engine[k][value])+1
                    pat.append(1/index)
                    break
    return( (1/len(search_engine))*(sum(pat)))
Mrr=[]
for i in range(1,4):
    c=mrr(globals()['se%s_dict' % i],ground_truth_dict)
    Mrr.append(c)
from pandas import DataFrame
MRR = pd.DataFrame({'Search engine':['SE_1','SE_2','SE_2']})
MRR['MRR']=Mrr
MRR.set_index(['Search engine'])
MRR.to_csv('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_1_1/output_data/mrr.csv',index=False)


# Function that create dataframe for ndcg
def dataframe_ndcg(ground_truth_dict,a): 
    ndcg_result=[]
    for i in range(1,4):
        c=ndcg(globals()['se%s_dict' % i],ground_truth_dict,a)
        ndcg_result.append(c)
    return ndcg_result

# nDCG
def dcg(search_engine,gr,v):
    pat=[]
    t=[]
    a = 0
    for k in search_engine.keys():
        if k in gr.keys():
            for value in range(0,v):
                if search_engine[k][value] in gr[k]:
                    pat.append(1)
                else:
                    pat.append(0)
            for i in range(1,len(pat)):
                a += (pat[i]/np.log2(i+1))
            t.append(pat[0] + a)
            pat=[]
            a = 0
    return t
def idcg(search_engine,gr,v):
    pat=[]
    t=[]
    a = 0
    for k in search_engine.keys():
        if k in gr.keys():
            for value in range(0,v):
                pat.append(1)
            for i in range(1,len(pat)):
                a += (pat[i]/np.log2(i+1))
            t.append(pat[0] + a)
            pat=[]
            a = 0
    return t

def ndcg(search_engine,gr,v):
    result = []
    for i in range(0,len(search_engine)):
        c = dcg(search_engine,gr,v)[i]/idcg(search_engine,gr,v)[i]
        result.append(c)
    return np.mean(result)
nDCG1=dataframe_ndcg(ground_truth_dict,1)
nDCG3=dataframe_ndcg(ground_truth_dict,3)
nDCG5=dataframe_ndcg(ground_truth_dict,5)
nDCG10=dataframe_ndcg(ground_truth_dict,10)
from pandas import DataFrame
NDCG = DataFrame({'Search engine': ['SE_1','SE_2','SE_3']})
NDCG['mean(nDCG@1)']=nDCG1
NDCG['mean(nDCG@3)']=nDCG3
NDCG['mean(nDCG@5)']=nDCG5
NDCG['mean(nDCG@10)']=nDCG10
NDCG.set_index(['Search engine'])
NDCG.to_csv('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_1_1/output_data/ndcg.csv',index=False)

