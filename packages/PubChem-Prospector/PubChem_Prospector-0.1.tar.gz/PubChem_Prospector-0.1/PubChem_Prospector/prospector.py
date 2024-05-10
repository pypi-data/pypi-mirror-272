import urllib3
import json
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
#                                                                                                   
#           PubChem Prospector:                                                                     _
#    This pakcage is designed to pull annotations from PubChem via their PUGView API         __  __|_|__ 
#    It iterates through JSON pages and retrieves the annotations. It is designed for      / \   _|+.+|_  
#    Multi-threading and will work best with HPC systems with fast internet connections       \// |WWW|\\
#    Be aware the time required will vary wildly with each annotation type                        // \\

# build_annotation_dict:
# this function creates a dictionary of all possible annotations PubChem Prospector can access
# just run "build_annotation_dict()" and access the dictionary by calling pc_annotations
# it is structured {entry_type:[annotations]}

def build_annotation_dict(): 
    http = urllib3.PoolManager()
    p = http.request("GET",'https://pubchem.ncbi.nlm.nih.gov/rest/pug/annotations/headings/JSON',timeout=10.0)
    p= json.loads(p.data.decode('utf-8'))
    global pc_annotations
    pc_annotations = {}
    for t in set([x['Type'] for x in p['InformationList']['Annotation']]):
        pc_annotations[t] = [x['Heading'] for x in p['InformationList']['Annotation'] if x['Type'] == t]

# annotation_search
# this function is just a quick shortcut for searching annotations in the pc_annotations dictionary
# just give it the entry_type and the string to search by and you can save the result(s) as a variable

def annotation_search(entry_type, string):
    x = [s for s in pc_annotations[entry_type] if string.lower() in s.lower()]
    print(x)
    return x

# get_dict
# this is the main function of PubChem_Prospector. It calls a series of smaller functions to build a 
# dictionary containing all selected annotations for the given entry type. It collects each annotation
# one at a time, so the more you ask for, the longer it will take, but it puts them all together in a 
# nice clean package, accesible by the numeric ids for that entry type in PubChem

def get_anns_wname(ann,name):
    try:
        x,y,z = [ann['LinkedRecords'][list(ann['LinkedRecords'].keys())[0]][0],ann['Name'],[s['String'] for d in ann['Data'] for s in d['Value']['StringWithMarkup']]]
        anns[x]={'Name':y,name:z}
    except:
            try:
                x,y = [ann['LinkedRecords'][list(ann['LinkedRecords'].keys())[0]][0],[d['Value'] for d in ann['Data']]]
                anns[x]={name:y}
            except:
                pass

def get_ann_wname(ann,name):
    try:
        x,y,z = [ann['LinkedRecords'][list(ann['LinkedRecords'].keys())[0]][0],ann['Name'],ann['Data'][0]['Value']['StringWithMarkup'][0]['String']]
        anns[x]={'Name':y,name:z}
    except:
            try:
                x,y = [ann['LinkedRecords'][list(ann['LinkedRecords'].keys())[0]][0],ann['Data'][0]['Value']]
                anns[x]={name:y}
            except:
                pass
            
def get_anns(ann,name):
    try:
        x,y = [ann['LinkedRecords'][list(ann['LinkedRecords'].keys())[0]][0],[s['String'] for d in ann['Data'] for s in d['Value']['StringWithMarkup']]]
        anns[x]={name:y}
    except:
            try:
                x,y = [ann['LinkedRecords'][list(ann['LinkedRecords'].keys())[0]][0],[d['Value'] for d in ann['Data']]]
                anns[x]={name:y}
            except:
                pass

def get_ann(ann,name):
    try:
        x,y = [ann['LinkedRecords'][list(ann['LinkedRecords'].keys())[0]][0],ann['Data'][0]['Value']['StringWithMarkup'][0]['String']]
        anns[x]={name:y}
    except:
            try:
                x,y = [ann['LinkedRecords'][list(ann['LinkedRecords'].keys())[0]][0],ann['Data'][0]['Value']]
                anns[x]={name:y}
            except:
                pass

def get_json_anns(pg, args):
    entry_type, annotation_type, has_name, multi, numpgs = args
    print("\033[F\033[K", end='')
    print(f'page {pg}/{numpgs-1}')
    p = http.request("GET",f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/{annotation_type}/JSON?heading_type={entry_type}&page={pg}',timeout=10.0)
    p= json.loads(p.data.decode('utf-8'))
    tries = 0
    while tries < 60:
        if has_name:
            if multi:
                try:
                    [[get_anns_wname(ann,annotation_type)] for ann in p['Annotations']['Annotation']]
                    break
                except:
                    tries+=1
            else:
                try:
                    [[get_ann_wname(ann,annotation_type)] for ann in p['Annotations']['Annotation']]
                    break
                except: 
                    tries+=1
        else:
            if multi:
                try:
                    [[get_anns(ann,annotation_type)] for ann in p['Annotations']['Annotation']]
                    break
                except: 
                    tries+=1
            else:
                try:
                    [[get_ann(ann,annotation_type)] for ann in p['Annotations']['Annotation']]
                    break
                except: 
                    tries+=1
        time.sleep(1)
        if tries==60:
            print('Error page ',pg)
    
def get_all_anns(entry_type, annotation_type, threads = 32):
    has_name = entry_type in ['Cell','Compound','Substance','Element']
    global http
    http = urllib3.PoolManager()
    annotation_type
    anns = {}
    p=http.request("GET",f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/{annotation_type}/JSON?heading_type={entry_type}&page=0',timeout=10.0)
    p=json.loads(p.data.decode('utf-8'))
    numpgs=p['Annotations']['TotalPages']+1
    [[get_anns(ann, annotation_type)] for ann in p['Annotations']['Annotation']]
    multi = False
    for k in list(anns.keys()):
        if len(anns[k][annotation_type]) > 1:
            multi = True
    print('Multi = ',multi,'\n')
    anns = {}
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_json_anns, range(1, numpgs), repeat([entry_type, annotation_type, has_name, multi, numpgs]))

def add_anns(k,a):
    try:
        pc_p[k][a]=anns[k]
    except:
        pc_p[k]=anns[k]

def get_dict(entry_type, annotation_types, threads = 32):
    global pc_p
    global anns
    pc_p = {}
    if isinstance(annotation_types,list):
        for a in annotation_types:
            print('Getting ',a,' annotations')
            get_all_anns(entry_type,a,threads = threads)
            [add_anns(k,a) for k in anns.keys()]
    else:
        get_all_anns(entry_type,annotation_types,threads = threads)
        pc_p = anns
    return pc_p
    del pc_p, anns