
# coding: utf-8

#%% PART A
import ast
import pandas as pd
min_hash=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_2_2/HW_1_part_2_2_dataset__min_hash_sketches.tsv',delimiter='\t')
sets_id=pd.read_csv('/Users/alfonsodamelio/Desktop/DATA SCIENCE/2°SEMESTRE/DMT(Leonardi)/dataset/part_2_2/HW_1_part_2_2_dataset__SETS_IDS_for_UNION.tsv',delimiter='\t')
#length universe set
universe=1123581321
#calculate jaccard how defined in the report
def jaccard(sketch):
    count=0
    for i in sketch:
        if i == 0:
            count+=1
    return (count/len(sketch)) 
def estimated_original_set_size(sketch):
    #convert in a list Min_Hash_Sketch column
    sketch=list(min_hash.Min_Hash_Sketch)
    #removing string before list
    x=[]
    for i in sketch:
        x.append(ast.literal_eval(i))
    #we append in a list all the estimated originale set size
    estimated_set=[]
    for i in x:
        estimated_set.append(round(jaccard(i)*universe))
    return estimated_set

original_set_size=estimated_original_set_size(min_hash)
#save in a csv file as claimed
with open('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_2_2/output_data/OUTPUT_HW_1_part_2_2_a.csv',"w") as f:
    f.write("Min_Hash_Sketch_INTEGER_Id"+ "," +  "ESTIMATED_ORIGINAL_SET_SIZE" +"\n")
    for sketch in range(0,50):
            f.write(str(sketch) + "," + str(original_set_size[sketch]) +"\n")

#%% PART B
def create_structure(sets_id):
    union_id=list(sets_id.Union_Set_id)
    union_of_sets=list(sets_id.set_of_sets_ids)
    w=[]
    for i in union_of_sets:
        w.append(ast.literal_eval(i))
    #prepare structure of the dataset__SETS_IDS_for_UNION
    nested=[]
    lista=[]
    for i in range(0,10):
        for j in w[i]:
            lista.append(j)
        nested.append(lista)
        lista=[]
    dictionary=dict(zip(union_id,nested))
    return dictionary

dictionary=create_structure(sets_id)

# at this point we compute the Union-Size-Estimation
def union_set(sketch,dictionary):
    #convert in a list Min_Hash_Sketch column
    sketch=list(min_hash.Min_Hash_Sketch)
    #removing string before list
    x=[]
    for i in sketch:
        x.append(ast.literal_eval(i))

    if len(dictionary)==2:
        z=[k for k in dictionary]
        pmin=list(map(lambda pair: min(pair), zip(x[z[0]],x[z[1]])))
        #print('union between sketch id: '+str(z[0])+'-'+str(z[1])+' is:')
        return round(jaccard(pmin)*universe)
    elif len(dictionary)==3:
        z=[k for k in dictionary]
        #print('union between sketch id: '+str(z[0])+'-'+str(z[1])+'-'+str(z[2])+' is:')
        pmin=list(map(lambda pair: min(pair), zip(x[z[0]],x[z[1]],x[z[2]])))
        return round(jaccard(pmin)*universe)
    elif len(dictionary)==4:
        z=[k for k in dictionary]
        #print('union between sketch id: '+str(z[0])+'-'+str(z[1])+'-'+str(z[2])+'-'+str(z[3])+' is:')
        pmin=list(map(lambda pair: min(pair), zip(x[z[0]],x[z[1]],x[z[2]],x[z[3]])))
        return round(jaccard(pmin)*universe)
    elif len(dictionary)==5:
        z=[k for k in dictionary]
        #print('union between sketch id: '+str(z[0])+'-'+str(z[1])+'-'+str(z[2])+'-'+str(z[3])+'-'+str(z[4])+' is:')
        pmin=list(map(lambda pair: min(pair), zip(x[z[0]],x[z[1]],x[z[2]],x[z[3]],x[z[4]])))
        return round(jaccard(pmin)*universe)
    else:
        pass

    
ESTIMATED_UNION_SIZE=[]
for i in range(0,10):
    ESTIMATED_UNION_SIZE.append(union_set(min_hash,dictionary[i]))

#save in a csv file as claimed
with open('/Users/alfonsodamelio/Desktop/DMT4BaS_2018/HW_1/part_2_2/output_data/OUTPUT_HW_1_part_2_2_b.csv',"w") as f:
    f.write("Union_Set_id"+ ";" + "set_of_sets_ids"+ ";" +"ESTIMATED_UNION_SIZE" +"\n")
    for sketch in range(0,10):
            f.write(str(sketch)+ ";" +str(sets_id.set_of_sets_ids[sketch])+ ";" +str(ESTIMATED_UNION_SIZE[sketch]) +"\n")


