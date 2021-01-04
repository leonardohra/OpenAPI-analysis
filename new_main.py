from preprocess import *
from colaborative_filtering import *
from utils import *
from tkinter import *
from tkinter import scrolledtext
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *
from New_Gensim_Model import Gensim_Model
from CustomEnumerators import TopicModelingAlgorithm, CoherenceType

def prepare_dataset():
    data_file = 'data.txt'
    component = 'description'

    data = load_list(data_file)
    data_list, id_info = get_component_if_both_and_info(data, component)
    data_lemmatized, id_info = execute_preprocessing_and_update_info(data_list, id_info, None)

    return data_lemmatized, id_info

def main():
    algo = TopicModelingAlgorithm.NMF
    topic_qtt = 9

    data_lemmatized, id_info = prepare_dataset()

    mod = Gensim_Model(data_lemmatized)
    mod.set_model(algo, topic_qtt)

    dataset = create_table_ids_topics(mod)

    window = cfg_window(mod, dataset, id_info)
    window.mainloop()

def evaluate_and_set_best_model(data_lemmatized):
    mod = Gensim_Model(data_lemmatized)
    mod.evaluate_several_models(algorithms = [TopicModelingAlgorithm.LDA, TopicModelingAlgorithm.NMF])
    mod.set_best_model()
    return mod

def filter_sub_topics_over_0(mod, qtt_tpcs, data_lemmatized):
    dataset = create_table_ids_topics(mod)
    d_0 = dataset_topics_over_zero(dataset)
    endps = [filter_endpoints_by_topic(d_0, i) for i in qtt_tpcs]
    new_datasets = [new_dataset_filtered_endpoint(data_lemmatized, endp) for endp in endps]
    return endps, new_datasets

def filter_sub_topics_best_topic(mod, data_lemmatized, qtt_tpcs):
    dataset = create_table_ids_topics(mod)
    d_most = dataset_topics_best_topic(dataset)
    endps = [filter_endpoints_by_topic(d_most, i) for i in qtt_tpcs]
    new_datasets = [new_dataset_filtered_endpoint(data_lemmatized, endp) for endp in endps]
    return endps, new_datasets

def main_evaluate_subs(topic_qtt, algo, sub_qtt_tpcs, output_folder, outfile):
    data_lemmatized, id_info = prepare_dataset()

    mod = Gensim_Model(data_lemmatized)
    mod.set_model(algo, topic_qtt)

    sub_topic_eval(mod, data_lemmatized, sub_qtt_tpcs, output_folder, outfile)

def sub_topic_eval(mod, data_lemmatized, qtt_tpcs, output_folder, outfile):
    dataset = create_table_ids_topics(mod)
    d_0 = dataset_topics_over_zero(dataset)
    #d_most = dataset_topics_best_topic(dataset)
    endps = [filter_endpoints_by_topic(d_0, i) for i in qtt_tpcs]
    new_datasets = [new_dataset_filtered_endpoint(data_lemmatized, endp) for endp in endps]

    mod_subs = [Gensim_Model(new_dataset) for new_dataset in new_datasets]

    for i in range(len(mod_subs)):
        print(len(endps[i]))
        if(len(endps[i]) > 0):
            mod_subs[i].evaluate_several_models(output_folder, outfile + '_' + str(i), algorithms = [TopicModelingAlgorithm.LDA, TopicModelingAlgorithm.LSA, TopicModelingAlgorithm.NMF], qtt_topics=qtt_tpcs, topns=[5])


def change_scrolled_text(sc_text, text):
    sc_text.config(state=tk.NORMAL)
    sc_text.delete(1.0, END)
    sc_text.insert(INSERT, text)
    sc_text.config(state=tk.DISABLED)

def search_btn_clicked(model, dataset, txt, sim_type, scr_txt, id_info):
    #'computer time graph'
    txt = execute_preprocessing([txt], None)[0]
    nt_to_topics = new_text_to_topics(model, txt)
    print(nt_to_topics)
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
    main()


'''
#Evaluate topics
from new_main import *
qtt_tpcs = [5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
output_folder = './results/new_results/'
outfile = 'run'
data_file = 'data.txt'
component = 'description'
algo = TopicModelingAlgorithm.NMF

data = load_list(data_file)
data_list, id_info = get_component_if_both_and_info(data, component)
data_lemmatized, id_info = execute_preprocessing_and_update_info(data_list, id_info)

mod = Gensim_Model(data_lemmatized)
#mod.evaluate_several_models(output_folder, outfile, algorithms = [TopicModelingAlgorithm.LDA, TopicModelingAlgorithm.LSA, TopicModelingAlgorithm.NMF], qtt_topics=qtt_tpcs, topns=[5])
mod.set_model(algo, 20)

qtt_tpcs = range(2, 20)
dataset = create_table_ids_topics(mod)
#d_0 = dataset_topics_over_zero(dataset)
d_most = dataset_topics_most_topics(dataset)
endps = [filter_endpoints_by_topic(d_most, i) for i in range(qtt_tpcs)]
new_datasets = [new_dataset_filtered_endpoint(data_lemmatized, endp) for endp in endps]

mod_subs = [Gensim_Model(new_dataset) for new_dataset in new_datasets]

for i in range(len(mod_subs)):
    mod_subs[i].evaluate_several_models(output_folder, outfile + 'sub_' + str(i + 2), algorithms = [TopicModelingAlgorithm.LDA, TopicModelingAlgorithm.LSA, TopicModelingAlgorithm.NMF], qtt_topics=qtt_tpcs, topns=[5])
'''
