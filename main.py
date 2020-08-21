import sys
import os
import yaml
import pickle
from Gensim_Model import *
import time
import io
import csv
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

def meta_constructor(loader, node):
    print(node)

def generate_list(file, dataset_location):
    data_list={}
    yaml.add_constructor(u'tag:yaml.org,2002:value', meta_constructor)
    accepted_meth = ['post', 'get', 'put', 'patch', 'delete']
    for base, dirs, files in os.walk(dataset_location):
        for f in files:
            text_document = ''
            if f == "swagger.yaml" or f == "openapi.yaml":
                API = base.split('\\')[-2]
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

    return summaries, descriptions, summaries_append_description

def main():
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
    output_folder = './results/'
    outfile = 'run'
    data_list_sum = sum
    data_list_des = des
    data_list_spd = s_p_d

    gen_mod_sum = Gensim_Model(data_list_spd)
    gen_mod_sum.pre_processing()
    gen_mod_sum.model_construction_evaluation_topn(output_folder, outfile + '_spd', qtt_topics=range(2, 11), coherence_types = [ CoherenceType.C_V ])

    gen_mod_sum = Gensim_Model(data_list_sum)
    gen_mod_sum.pre_processing()
    gen_mod_sum.model_construction_evaluation_topn(output_folder, outfile + '_sum', qtt_topics=range(2, 11), coherence_types = [ CoherenceType.C_V ])

    gen_mod_des = Gensim_Model(data_list_des)
    gen_mod_des.pre_processing()
    gen_mod_des.model_construction_evaluation_topn(output_folder, outfile + '_des', qtt_topics=range(2, 11), coherence_types = [ CoherenceType.C_V ])

if __name__ == "__main__":
    main()
