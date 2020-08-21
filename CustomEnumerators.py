from enum import Enum

class TopicModelingAlgorithm(Enum):
    LDA = 1
    LSA = 2
    NMF = 3
    
    def simple_name(self):
        names = {
            1: 'LDA',
            2: 'LSA',
            3: 'NMF'
        }
        return '{0}'.format(names[self.value])
    
    def __str__(self):
        names = {
            1: 'Latent Dirichlet Allocation (LDA)',
            2: 'Latent Semantic Analysis (LSA), aka Latent Semantic Index (LSI)',
            3: 'Non Negative Matrix Factorization (NMF)'
        }
        
        return '{0}'.format(names[self.value])
    
class CoherenceType(Enum):
    U_MASS = 1
    C_V = 2
    C_UCI = 3
    C_NPMI = 4
    
    def __str__(self):
        dict_param_gensim = {
            1: 'u_mass',
            2: 'c_v',
            3: 'c_uci',
            4: 'c_npmi'
        }

        return '{0}'.format(dict_param_gensim[self.value])
        
        
class EntityAlgorithm(Enum):
    NLTK = 1
    SPACY = 2
    NONE = 3