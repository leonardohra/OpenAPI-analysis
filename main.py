import sys
import os
import yaml
import pickle
from utils import *
from Gensim_Model import *
import time
import io
import csv
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import operator
import pandas as pd
from colaborative_filtering import *
from tkinter import *
from tkinter import scrolledtext
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *

# This is needed to the yaml reader
def meta_constructor(loader, node):
    print(node)

def generate_list(file, dataset_location):
    data_list={}
    loc = os.getcwd() + '/APIs/'
    yaml.add_constructor(u'tag:yaml.org,2002:value', meta_constructor)
    accepted_meth = ['post', 'get', 'put', 'patch', 'delete']
    for base, dirs, files in os.walk(dataset_location):
        for f in files:
            text_document = ''
            if f == "swagger.yaml" or f == "openapi.yaml":
                API = base.replace(loc, '')
                data_list[API] = {}
                data = yaml.load(open(os.path.join(base,f), encoding="utf8"), Loader=yaml.Loader)
                print((API + '/' + f))
                try:
                    text_document = []

                    for api in data['paths'].keys():
                        for methodHTTP in data['paths'][api].keys():
                            if(methodHTTP.lower() in accepted_meth):
                                data_list[API][api + '/' + methodHTTP] = {}

                                if 'description' in list(data['paths'][api][methodHTTP].keys()):
                                    data_list[API][api + '/' + methodHTTP]['description'] = data['paths'][api][methodHTTP]['description']

                                if 'summary' in list(data['paths'][api][methodHTTP].keys()):
                                    data_list[API][api + '/' + methodHTTP]['summary'] = data['paths'][api][methodHTTP]['summary']

                except (OSError, RuntimeError, TypeError, NameError, AttributeError):
                        pass

    save_list(file, data_list)

    return data_list

def save_list(file, itemlist):
    with open(file, 'wb') as fp:
        pickle.dump(itemlist, fp)

def load_list(file):
    itemlist = []

    with open (file, 'rb') as fp:
        itemlist = pickle.load(fp)

    return itemlist

def get_summary_and_description_endpoints(data_list):
    summaries = []
    descriptions = []
    summaries_append_description = []
    for api, endpoints in data_list.items():
        for endpoint, components in endpoints.items():
            if('description' in components.keys() and 'summary'  in components.keys()):
                summaries.append(components['summary'])
                descriptions.append(components['description'])
                summaries_append_description.append(components['summary'] + ' ' + components['description'])

    print("Summary and description endpoints ok")

    return summaries, descriptions, summaries_append_description

def load_data_list(file = './data.txt'):
    list_file = file
    data_list = load_list(list_file)
    print('Data list loaded')
    return data_list

def main():
    qtt_tpcs = [5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
    source = './APIs/'
    list_file = './data.txt'
    file_exists = os.path.isfile(list_file)
    data_list = []

    if(file_exists):
        data_list = load_list(list_file)
    else:
        data_list = generate_list(list_file, source)

    print ('Number of APIs: ' + str(len(data_list)))

    sum, des, s_p_d = get_summary_and_description_endpoints(data_list)
    output_folder = './results/new_results/'
    outfile = 'run'
    data_list_sum = sum
    data_list_des = des
    data_list_spd = s_p_d


    gen_mod_des = Gensim_Model(data_list_des)
    gen_mod_des.model_construction_evaluation_topn(output_folder, outfile + '_des', qtt_topics=qtt_tpcs, coherence_types = [ CoherenceType.C_V ], topns = [5, 10])

    gen_mod_sum = Gensim_Model(data_list_sum)
    gen_mod_sum.model_construction_evaluation_topn(output_folder, outfile + '_sum', qtt_topics=qtt_tpcs, coherence_types = [ CoherenceType.C_V ], topns = [5, 10])

    gen_mod_sum = Gensim_Model(data_list_spd)
    gen_mod_sum.model_construction_evaluation_topn(output_folder, outfile + '_spd', qtt_topics=qtt_tpcs, coherence_types = [ CoherenceType.C_V ], topns = [5, 10])

def main2():
    source = './APIs/'
    list_file = './data.txt'
    file_exists = os.path.isfile(list_file)
    data_list = []

    if(file_exists):
        data_list = load_list(list_file)

    print ('Number of APIs: ' + str(len(data_list)))

    sum, des, s_p_d = get_summary_and_description_endpoints(data_list)
    output_folder = './results/'
    outfile = 'run'
    data_list_des = des

    gen_mod_des = Gensim_Model(data_list_des)
    gen_mod_des.pre_processing()
    gen_mod_des.set_default_model(algo = TopicModelingAlgorithm.NMF, topic_qtt=9)

def main3():
    list_file = './data.txt'
    data_list = load_list(list_file)
    summ, des, s_p_d = get_summary_and_description_endpoints(data_list)
    data_list_des = des
    gen_mod_des = Gensim_Model(data_list_des)
    gen_mod_des.pre_processing()
    gen_mod_des.set_default_model(algo = TopicModelingAlgorithm.NMF, topic_qtt=9)

    text = ['computer', 'time', 'graph']

    dataset = create_table_ids_topics(gen_mod_des)
    nt_to_topics = new_text_to_topics(gen_mod_des, text)
    pearsonCorrelationDict = calculate_pearson_correlation(nt_to_topics, dataset)
    sorted_pearson = sorted(pearsonCorrelationDict.items(), key=lambda x:x[1], reverse=True)
    for i in range(10):
        print(gen_mod_des.id_to_endpoint(sorted_pearson[i][0]))

def main4():
    list_file = './data.txt'
    data_list = load_list(list_file)
    id_info = generate_id_to_info_dictionary(data_list)

    #prep_text = load_list('prep_text.txt')
    gen_mod_des = create_model(data_list, prep_text=None, base = 'description', tpc_qtt=100, alg = TopicModelingAlgorithm.NMF)
    dataset = create_table_ids_topics(gen_mod_des)
    window = cfg_window(gen_mod_des, dataset, id_info)
    window.mainloop()

#def API_topic_comparison(data_list, mod):
#    end_tpcs =
#    for API, endpoints in data_list.items():
#        for endpoint, component in endpoints.items():


def main_eval():
    list_file = './data.txt'
    data_list = load_list(list_file)
    id_info = generate_id_to_info_dictionary(data_list)

    #prep_text = load_list('prep_text.txt')
    gen_mod_des = create_model(data_list, None, 55)
    dataset = create_table_ids_topics(gen_mod_des)

    # 'Cosine Distance' 'Euclidean Distance' 'Pearson Correlation'

    sim_type ='Euclidean Distance'
    txt = ''
    txt = gen_mod_des.pre_process_external(txt)
    nt_to_topics = new_text_to_topics(gen_mod_des, txt)
    simDict = calculate_similarity(nt_to_topics, dataset, type=sim_type)
    rev = False if sim_type == 'Euclidean Distance' else True
    sorted_sim = sorted(simDict.items(), key=lambda x:x[1], reverse=rev)


def create_model(data_list, prep_text=None, base = 'description', tpc_qtt=9, alg = TopicModelingAlgorithm.NMF):
    summ, des, s_p_d = get_summary_and_description_endpoints(data_list)
    data_list = des if base == 'description' else summ if base == 'summary' else s_p_d

    #gen_mod = Gensim_Model(data_list, prep_text)
    gen_mod = Gensim_Model(data_list, prep_text)
    gen_mod.set_default_model(algo = alg, topic_qtt=tpc_qtt)
    print("model created: {} {} topics".format(alg.simple_name(), tpc_qtt))
    return gen_mod

def generate_id_to_info_dictionary(data_list):
    cur_id = 0
    id_to_info_dict = {}
    for api, endpoints in data_list.items():
        for endpoint, components in endpoints.items():
            if('description' in components and 'summary' in components):
                for component, value in components.items():
                    if(component == 'description'):
                        id_to_info_dict[cur_id] = [api, endpoint, component, value]
                        cur_id += 1

    print("Dictionary of endpoints' information generated")
    return id_to_info_dict


def change_scrolled_text(sc_text, text):
    sc_text.config(state=tk.NORMAL)
    sc_text.delete(1.0, END)
    sc_text.insert(INSERT, text)
    sc_text.config(state=tk.DISABLED)

def search_btn_clicked(model, dataset, txt, sim_type, scr_txt, id_info):
    #'computer time graph'
    txt = model.pre_process_external(txt)
    nt_to_topics = new_text_to_topics(model, txt)
    simDict = calculate_similarity(nt_to_topics, dataset, type=sim_type)
    rev = False if sim_type == 'Euclidean Distance' else True
    sorted_sim = sorted(simDict.items(), key=lambda x:x[1], reverse=rev)

    result = []
    for i in range(10):
        info = id_info[sorted_sim[i][0]]
        result.append("In the API {}, the endpoint {} has the following description: {}. \nSimilarity type: {} \nvalue: {} \n\n".format(info[0], info[1], info[3], sim_type, sorted_sim[i][1]))

    txt_res = "\n".join(result)
    change_scrolled_text(scr_txt, txt_res)

def cfg_window(model, dataset, id_info):
    window = Tk()
    window.title("Services recommendation tool")
    window.geometry('1200x800')

    lbl_search = Label(window, text="Please insert your search request")
    lbl_search.grid(column=0, row=0)

    txt_search = Entry(window)
    txt_search.grid(column=0, row=1)

    cb_search = Combobox(window)
    cb_search.grid(column=1, row=1)
    cb_search['values']= ('Euclidean Distance', 'Cosine Distance', 'Pearson Correlation')
    cb_search.current(1)

    txt_result = scrolledtext.ScrolledText(window, state=tk.DISABLED)
    txt_result.grid(column=0, row=2)

    btn_search = Button(window, text="Search", command=lambda: search_btn_clicked(model, dataset, txt_search.get(), cb_search.get(), txt_result, id_info))
    btn_search.grid(column=2, row=1)

    #window.mainloop()
    return window

def loading_window():
    pass

if __name__ == "__main__":
    #main3()
    main4()


'''
import operator
from main import *
import pandas as pd
list_file = './data.txt'
data_list = load_list(list_file)
summ, des, s_p_d = get_summary_and_description_endpoints(data_list)
data_list_des = des
gen_mod_des = Gensim_Model(data_list_des)
gen_mod_des.pre_processing()
gen_mod_des.set_default_model(algo = TopicModelingAlgorithm.NMF, topic_qtt=9)


rec = gen_mod_des.endpoint_in_topics_dataset()
df = pd.DataFrame(rec, columns=['id_sentence', 'topic_num', 'score'])
sentSubsetGroup = df.groupby(['id_sentence'])
sentSubsetGroup = sorted(sentSubsetGroup, key=lambda x: len(x[1]), reverse=True)

[0.9, ]

#Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
pearsonCorrelationDict = {}
#For every user group in our subset
for name, group in sentSubsetGroup:
    #Let’s start by sorting the input and current user group so the values aren’t mixed up later on
    group = group.sort_values(by='topic_num')
    #Get the N for the formula
    nRatings = len(group)
    #Get the review scores for the movies that they both have in common
    temp_df = df2[df2['topic_num'].isin(group['topic_num'].tolist())]
    #And then store them in a temporary buffer variable in a list format to facilitate future calculations
    tempRatingList = temp_df['score'].tolist()
    #Let’s also put the current user group reviews in a list format
    tempGroupList = group['score'].tolist()
    #Now let’s calculate the pearson correlation between two users, so called, x and y
    Sxx = sum([i**2 for i in tempRatingList]) — pow(sum(tempRatingList),2)/float(nRatings)
    Syy = sum([i**2 for i in tempGroupList]) — pow(sum(tempGroupList),2)/float(nRatings)
    Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) — sum(tempRatingList)*sum(tempGroupList)/float(nRatings)
    #If the denominator is different than zero, then divide, else, 0 correlation.
    if Sxx != 0 and Syy != 0:
        pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
    else:
        pearsonCorrelationDict[name] = 0


max(pearsonCorrelationDict.iteritems(), key=operator.itemgetter(1))[0]


from main import *
list_file = './data.txt'
data_list = load_list(list_file)
summ, des, s_p_d = get_summary_and_description_endpoints(data_list)
data_list_des = des
gen_mod_des = Gensim_Model(data_list_des)
gen_mod_des.pre_processing()
gen_mod_des.set_default_model(algo = TopicModelingAlgorithm.NMF, topic_qtt=9)

text = ['computer', 'time', 'graph']

dataset = create_table_ids_topics(gen_mod_des)
nt_to_topics = new_text_to_topics(gen_mod_des, text)
pearsonCorrelationDict = calculate_pearson_correlation(nt_to_topics, dataset)
sorted_pearson = sorted(pearsonCorrelationDict.items(), key=lambda x:x[1], reverse=True)


corp = gen_mod_des._Gensim_Model__corpus
id2w = gen_mod_des._Gensim_Model__id2_words
dt_l = gen_mod_des._Gensim_Model__data_list
tk = gen_mod_des._Gensim_Model__data_tkzed
stp = gen_mod_des._Gensim_Model__data_stp
lem = gen_mod_des._Gensim_Model__data_lemmatized
a = 200
print('{}\n\n{}\n\n{}'.format(dt_l[a], tk[a], lem[a]))


'''


'''
This query returns system application information if the application ID provided is for system application. Results encompass deployed applications in active, activating, and downloading states. This query requires that the node name corresponds to a node on the cluster. The query fails if the provided node name does not point to any active Service Fabric nodes on the cluster
'''
