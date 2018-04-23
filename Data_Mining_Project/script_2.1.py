#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 11:30:06 2018

@author: alfonsodamelio
"""

#read data e append in a list called song
songs = []
import os
for subdir, dirs, files in os.walk('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_2_1/lyrics_collection__CONVERTED'): 
    #with os.walk we found the dir, subdir and files contained in this directory
    for file in files: #at this point we work on the files contained in the directory (name of songs)
        if(file.endswith(".html")): #keep the name of songs inside the file that finish with .html
            filepath = os.sep+file #at this point create the file path ( /name of song.html) and append it in song list
            songs.append(filepath)


#%%create shingles function
def shingles(file):
    b=[]
    shingleLength = 3
    for j in range(len(file) - shingleLength + 1):
        a = tuple(file[j:j+shingleLength])
        b.append(a) 
    return b

#%%scraping and cretion of dictionary structure with name of files as keys and list of shingles as values
import time
import codecs, json, requests
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup #we import Beutiful Soup to scrape inside 'html' file
from nltk.corpus import stopwords
start_time = time.time()
stat={}
result = {}
headers = {'content-type':'application/json'}
all_shingles=[]
for song in songs:

    f = codecs.open('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_2_1/lyrics_collection__CONVERTED'+ song , 'r', 'utf-8')
    soup = BeautifulSoup(f.read(), "lxml")
    #get lyrics
    for link in soup.find_all('body'):
        try:
            
            tokenizer = RegexpTokenizer(r'\w+') #do the tokenization and remove punctuation
            t = tokenizer.tokenize(link.get_text(separator = ' ')) #separate the word like this --> helloLove
            x = ''
            for element in t:
                x = x+' '+element.lower() #case folding (Normalization)--> all word in the lyrics lower
            stat[song]=x.split()
            result[song]= shingles(x.split()) #shingles k=3
            
            
        except:
            pass
    try:
        for j in result[song]:
            all_shingles.append(j) #put all shingles in a list
    except:
        pass
    
    if len(result)%1000==0:
        print(len(result))
     #append dictionary in a list
    if len(result)==87042: #append in a list 87042 thousand songs 
        break
print("--- %s seconds ---" % (time.time() - start_time))
#%% statistics part
# n° of songs for each docs
count=[]
for key in stat.keys():
        count.append(len(stat[key]))

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
plt.title('Histogram of songs length',fontsize=17)
plt.hist(count,color='green',ec='black')
plt.xlabel('Length',fontsize=13)
plt.ylabel('n° of songs',fontsize=13)
plt.xlim(0,2000)
plt.savefig('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_2_1/output_data/song_length.png')
plt.show()

#%% most common words
from collections import Counter
from nltk.corpus import stopwords
eng=stopwords.words('english')
mostwords = {}
for key in stat.keys():
    for word in stat[key]:
        if(word.lower() not in eng) :
            if(word.lower() in mostwords):
                mostwords[word.lower()]+=1
            else:
                mostwords[word.lower()]=1
c2 = Counter(mostwords)
best=c2.most_common(10)
nomi=[]
length=[]
for key,value in best:
    nomi.append(key)
    length.append(value)
plt.bar(range(len(nomi)),length,align='center',color='red')
plt.xticks(range(len(nomi)), nomi,fontsize=15, rotation=70)
plt.title('10 most common words histogram' )
plt.ylabel('frequency')
plt.xlabel('words')
plt.savefig('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_2_1/output_data/most_common_words.png')
plt.show()

#%%
Set=set(all_shingles) #set of shingles
set_shingles=[shingle for shingle in Set]

#%%for each shingle in the set we assign an integer from 0 to length of the set
inv={}
idx=0
for shingle in set_shingles:
    inv[shingle]=idx
    idx+=1
    
#%% for each shingles check its value in the inverse dictionary before created
for song in result.keys():
    try:
        for i in range(0,len(result[song])):
            result[song][i]=inv[result[song][i]]
    except:
        pass
#%%remove empty set 
element_erase=[]
for key,value in result.items():
    if (len(value)==0):
        element_erase.append(key)
def entries_to_remove(entries, the_dict):
    for key in entries:
        if key in the_dict:
            del the_dict[key]
entries_to_remove(element_erase,result)

#%% Create file tsv structure
import numpy as np
fieldnames = [["set_id","set_as_list_of_elements_id"]]
for shingle in result:
    fieldnames.append([shingle,str(result[shingle])])
fieldnames=np.asarray(fieldnames)
np.savetxt('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_2_1/output_data/shingles.tsv',fieldnames,delimiter="\t",fmt="%s")
#%% save result in local
import json 
file= open('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/song.json',"w")
json.dump(result,file)
file.close()

#%% create hashing function
import random
import math

################################################
num_hash_functions = 300
upper_bound_on_number_of_distinct_terms  = 10000000
#upper_bound_on_number_of_distinct_terms =   138492
#upper_bound_on_number_of_distinct_terms =  3746518

################################################


### primality checker
def is_prime(number):
	for j in range(2, int(math.sqrt(number)+1)):
		if (number % j) == 0: 
			return False
	return True
with open('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_2_1/output_data/hash_300.tsv',"w") as f:
    f.write("a	b	p	n"+"\n")
    for hash_function_id in range(num_hash_functions):
        	a = random.randint(1, upper_bound_on_number_of_distinct_terms-1)
        	b = random.randint(0, upper_bound_on_number_of_distinct_terms-1)
        	p = random.randint(upper_bound_on_number_of_distinct_terms, 10*upper_bound_on_number_of_distinct_terms)
        	while is_prime(p) == False:
        		p = random.randint(upper_bound_on_number_of_distinct_terms, 10*upper_bound_on_number_of_distinct_terms)
        	f.write(str(a) + "\t" + str(b) + "\t" + str(p) + "\t" + str(upper_bound_on_number_of_distinct_terms)+"\n")

#%%find best r and b, with all possibile combination saved in file---> combinazioni_300.csv
import pandas as pd
import numpy as np
comb=pd.read_csv('/Users/alfonsodamelio/Desktop/combinazioni_300.csv',header=-1,delimiter=';') #all possible combinations of r and b
def scurve(r,b):
    p=1-(1-(0.85)**r)**b
    return p
lista=[]
r_b=[]
for i in range(0,18):
    r_b.append((comb[0][i],comb[1][i]))
    lista.append(scurve(comb[0][i],comb[1][i]))
dictio=dict(zip(r_b,lista))
#at this point we find the combination of r and b that is closer to our constraint, so jaccard=0.85 and p=0.97
value = 0.97
A = [i for i in dictio.values()]
A=np.array(A)
idx = (np.abs(A-value)).argmin()
keys=[key for key in dictio.keys()]
print('These are the best r and b choosen: '+str(keys[idx]))

#%% in this part we compute the number of False positive
import pandas as pd
candidates=pd.read_csv('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_2_1/output_data/ALL_NEAR_DUPLICATE_CANDIDATES_with_LSH__12_25_300__hw1.tsv',delimiter='\t')
near_duplicate=pd.read_csv('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_2_1/output_data/APPROXIMATED_NEAR_DUPLICATES_DETECTION__lsh_plus_min_hashing__12_25_300__hw1.tsv',delimiter='\t')
candidates['new_col'] = list(zip(candidates.name_set_1, candidates.name_set_2))
near_duplicate['new_col'] = list(zip(near_duplicate.name_set_1, near_duplicate.name_set_2))
set_candidates=set(candidates.new_col)
set_near=set(near_duplicate.new_col)
count=0
for i in set_candidates:
    if i not in set_near:
        count+=1
    else:
        pass
print('number of false positive is: '+str(count))
     




