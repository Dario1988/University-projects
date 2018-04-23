# Part 1.2
import pandas as pd
import numpy as np
ground_truth_2=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_1_2/part_1_2__Ground_Truth.tsv',delimiter='\t')
se1_2=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_1_2/part_1_2__Results_SE_1.tsv',delimiter='\t')
se2_2=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_1_2/part_1_2__Results_SE_2.tsv',delimiter='\t')
se3_2=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_1_2/part_1_2__Results_SE_3.tsv',delimiter='\t')

lista2=list(ground_truth_2.groupby('Query_id')['Relevant_Doc_id'])
query2=[]
for i in ground_truth_2['Query_id']:
    query2.append(i)
sort_query=sorted(set(query2))

#ground truth in dictionary
ground_truth_dict_2={}
for i in range(0,len(sort_query)):
    c=lista2[i][1]
    key=lista2[i][0]
    ground_truth_dict_2[key]=[j for j in c]

# Function to convert in dict
def dicti(file):
    se1_dicti={}
    for i in range(0,len(file)):
        c=file[i][1]
        key=file[i][0]
        se1_dicti[key]=[j for j in c]
    return se1_dicti

se1_2=list(se1_2.groupby('Query_ID')['Doc_ID'])
se2_2=list(se2_2.groupby('Query_ID')['Doc_ID'])
se3_2=list(se3_2.groupby('Query_ID')['Doc_ID'])
se1_2_dict=dicti(se1_2)
se2_2_dict=dicti(se2_2)
se3_2_dict=dicti(se3_2)
#p@k function for the app
def pat_key_app(search_engine,gr,v):
    pat=[]
    count=0
    for k in search_engine.keys():
        if k in gr.keys():
            try:
                for value in range(0,v):
                    if search_engine[k][value] in gr[k]:
                        count+=1
                pat.append(count/min(v,len(gr[k])))
            except:
                pass
        count=0
    return np.mean(pat)
#apply p@k function on our search engine and find the best result
a=pat_key_app(se1_2_dict,ground_truth_dict_2,4)
b=pat_key_app(se2_2_dict,ground_truth_dict_2,4)
c=pat_key_app(se3_2_dict,ground_truth_dict_2,4)

from pandas import DataFrame
Pat = DataFrame({'result': ['mean(P@4)']})
Pat['SE_1']=a
Pat['SE_2']=b
Pat['SE_3']=c
Pat.set_index(['result'])
Pat.to_csv('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_1_2/output_data/p@4.csv',index=False)

