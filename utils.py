import os
import yaml
import pickle

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

def get_component_if_both_and_info(data, comp):
    result = []
    info = {}
    id = 0
    for api, paths in data.items():
            for path, components in paths.items():
                if('description' in components.keys() and 'summary' in components.keys()):
                    for component, value in components.items():
                        if(component == comp):
                            info[id] = [api, path, component, value]
                            id += 1
                            result.append(value)
                            break

    return result, info

def generate_id_to_info_dictionary(data_list):
    cur_id = 0
    id_to_info_dict = {}
    for api, endpoints in data_list.items():
        for endpoint, components in endpoints.items():
            if('description' in components and 'summary' in components):
                for component, value in components.items():
                    if(component == 'description' and value != ''):
                        id_to_info_dict[cur_id] = [api, endpoint, component, value]
                        cur_id += 1

    print("Dictionary of endpoints' information generated")
    return id_to_info_dict

def dataset_topics_over_zero(dataset_subset_group):
    d = {}

    for data in dataset_subset_group:
        d[data[0]] = []
        for i in range(data[1].shape[0]):
            if(data[1]['score'].to_list()[i] > 0):
                d[data[0]].append([data[1]['topic_num'].to_list()[i], data[1]['score'].to_list()[i]])

    return d

def dataset_topics_best_topic(dataset_subset_group):
    d = {}

    for data in dataset_subset_group:
        d[data[0]] = []
        high_score = -1
        high_score_i = -1
        for i in range(data[1].shape[0]):
            if(data[1]['score'].to_list()[i] > high_score):
                high_score = data[1]['score'].to_list()[i]
                high_score_i = i
        d[data[0]].append([data[1]['topic_num'].to_list()[high_score_i], data[1]['score'].to_list()[high_score_i]])

    return d

def filter_endpoints_by_topic(d, topic):
    ids_in_topic = []

    for key, values in d.items():
        for value in values:
            if(value[0] == topic):
                ids_in_topic.append(key)
                break

    return ids_in_topic

def new_dataset_filtered_endpoint(dataset, endp_list):
    return [dataset[i] for i in endp_list]
