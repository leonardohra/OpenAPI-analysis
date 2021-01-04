import os
import yaml
import pickle

# This is needed to the yaml reader
def meta_constructor(loader, node):
    print(node)

def generate_list(file, dataset_location):
    data_list={}
    loc = os.getcwd() + '\\APIs\\'
    yaml.add_constructor(u'tag:yaml.org,2002:value', meta_constructor)
    accepted_meth = ['post', 'get', 'put', 'patch', 'delete']
    for base, dirs, files in os.walk(dataset_location):
        for f in files:
            text_document = ''
            if f == "swagger.yaml" or f == "openapi.yaml":
                API = base.replace(loc, '')
                data_list[API] = {}
                data = yaml.load(open(os.path.join(base,f), encoding="utf8"), Loader=yaml.Loader)
                print((API + '\\' + f))
                try:
                    text_document = []

                    for pat in data['paths'].keys():
                        for methodHTTP in data['paths'][pat].keys():
                            if(methodHTTP.lower() in accepted_meth):
                                data_list[API][pat + '/' + methodHTTP] = {}

                                if 'description' in list(data['paths'][pat][methodHTTP].keys()):
                                    data_list[API][pat + '/' + methodHTTP]['description'] = data['paths'][pat][methodHTTP]['description']

                                if 'summary' in list(data['paths'][pat][methodHTTP].keys()):
                                    data_list[API][pat + '/' + methodHTTP]['summary'] = data['paths'][pat][methodHTTP]['summary']

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
