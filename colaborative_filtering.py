#data_lemmatized: a list of lists, every list is a set of words with the endpoints' description
#corpus the set of words translated to numbers and frequency
# [id2w.doc2bow(elem) for elem in b] , b = [['test', 'of', 'something']], transforming the set of words into their respective numbers
import pandas as pd
import math
from scipy import spatial
from preprocess import execute_preprocessing

'''
other_texts = [
    ['computer', 'time', 'graph']
]

id2w = gen_mod_des._Gensim_Model__id2_words
corp = gen_mod_des._Gensim_Model__corpus
ot_id2w = id2w.doc2bow(other_texts)
mod = gen_mod_des.get_default_model()
ot_in_tpcs = mod[ot_id2w[0]]
qtt = 9
id_to_tpc = []

for j in range(qtt):
    found = False
    for elem in ot_in_tpcs:
        if(elem[0] == j):
            id_to_tpc.append([123456789, j, elem[1]])
            found = True
    if(not found):
        id_to_tpc.append([123456789, j, 0])

df2 = pd.DataFrame(id_to_tpc, columns=['id_sentence', 'topic_num', 'score'])
'''
'''
other_texts = [
    ['computer', 'time', 'graph'],
    ['survey', 'response', 'eps'],
    ['human', 'system', 'computer']
]
'''


'''def create_table_ids_topics(gen_mod):
    rec = gen_mod.endpoint_in_topics_dataset()
    df = pd.DataFrame(rec, columns=['id_sentence', 'topic_num', 'score'])
    sentSubsetGroup = df.groupby(['id_sentence'])
    sentSubsetGroup = sorted(sentSubsetGroup, key=lambda x: len(x[1]), reverse=True)
    print('Topics for each endpoints modeled in a table')

    return sentSubsetGroup
'''

def new_text_to_topics(mod, text):
    print(text)
    new_tpcs = mod.new_text_to_topics(text)
    return new_tpcs

def calc_euclidean_distance(a, b):
    return spatial.distance.euclidean(a, b)

def calc_cosine_distance(a, b):
    return spatial.distance.cosine(a, b)

def calc_pearson_correlation(a, b):
    nScores = len(b)
    Sxx = sum([i**2 for i in a]) - pow(sum(a),2)/float(nScores)
    Syy = sum([i**2 for i in b]) - pow(sum(b),2)/float(nScores)
    Sxy = sum( i*j for i, j in zip(a, b)) - sum(a)*sum(b)/float(nScores)
    #If the denominator is different than zero, then divide, else, 0 correlation.
    if Sxx != 0 and Syy != 0:
        return Sxy/math.sqrt(Sxx*Syy)
    else:
        return 0

def calculate_similarity(new_text_tpcs, dataset, type):
    sim_scores = {}
    i = 0
    lim = len(dataset)
    progress = False

    for name, group in dataset:
        group = group.sort_values(by='topic_num')
        nScores = len(group)
        temp_df = new_text_tpcs[new_text_tpcs['topic_num'].isin(group['topic_num'].tolist())]
        tempScoreList = temp_df['score'].tolist()
        tempGroupList = group['score'].tolist()
        sim_score = 0

        if(type == 'Cosine Distance'):
            sim_score = calc_cosine_distance(tempScoreList, tempGroupList)
        elif(type == 'Euclidean Distance'):
            sim_score = calc_euclidean_distance(tempScoreList, tempGroupList)
        elif(type == 'Pearson Correlation'):
            sim_score = calc_pearson_correlation(tempScoreList, tempGroupList)

        sim_scores[name] = sim_score
        i += 1

        if(i%1000 == 0):
            print('{}/{}'.format(i, lim))

    return sim_scores

def topic_dist_for_new_text(text):
    txt_pp = execute_preprocessing(text)
    new_tpcs = mod.new_text_to_topics(txt_pp[0])
    return new_tpcs

def create_table_ids_topics(gen_mod):
    rec = gen_mod.endpoint_in_topics_dataset()
    df = pd.DataFrame(rec, columns=['id_sentence', 'topic_num', 'score'])
    sentSubsetGroup = df.groupby(['id_sentence'])
    sentSubsetGroup = sorted(sentSubsetGroup, key=lambda x: len(x[1]), reverse=True)
    print('Topics for each endpoints modeled in a table')

    return sentSubsetGroup

'''
def calculate_spatial_distance(new_text_tpcs, dataset):
    spatial_distance = {}
    #For every user group in our subset
    for name, group in dataset:
        group = group.sort_values(by='topic_num')
        nScores = len(group)
        temp_df = new_text_tpcs[new_text_tpcs['topic_num'].isin(group['topic_num'].tolist())]
        tempScoreList = temp_df['score'].tolist()
        tempGroupList = group['score'].tolist()
        dist = spatial.distance.euclidean(tempScoreList, tempGroupList)
        spatial_distance[name] = dist

    return spatial_distance

def calculate_cosine_distance(new_text_tpcs, dataset):
    cosine_distance = {}
    #For every user group in our subset
    for name, group in dataset:
        group = group.sort_values(by='topic_num')
        nScores = len(group)
        temp_df = new_text_tpcs[new_text_tpcs['topic_num'].isin(group['topic_num'].tolist())]
        tempScoreList = temp_df['score'].tolist()
        tempGroupList = group['score'].tolist()
        dist = spatial.distance.cosine(tempScoreList, tempGroupList)
        cosine_distance[name] = dist

    return cosine_distance

def calculate_pearson_correlation(new_text_tpcs, dataset):
    #Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
    pearsonCorrelationDict = {}
    #For every user group in our subset
    for name, group in dataset:
        group = group.sort_values(by='topic_num')
        nScores = len(group)
        temp_df = new_text_tpcs[new_text_tpcs['topic_num'].isin(group['topic_num'].tolist())]
        tempScoreList = temp_df['score'].tolist()
        tempGroupList = group['score'].tolist()
        Sxx = sum([i**2 for i in tempScoreList]) - pow(sum(tempScoreList),2)/float(nScores)
        Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(nScores)
        Sxy = sum( i*j for i, j in zip(tempScoreList, tempGroupList)) - sum(tempScoreList)*sum(tempGroupList)/float(nScores)
        #If the denominator is different than zero, then divide, else, 0 correlation.
        if Sxx != 0 and Syy != 0:
            pearsonCorrelationDict[name] = Sxy/math.sqrt(Sxx*Syy)
        else:
            pearsonCorrelationDict[name] = 0

    return pearsonCorrelationDict
'''
