import pyLDAvis
import pyLDAvis.gensim

# Visualize the topics
#pyLDAvis.enable_notebook()
#vis = pyLDAvis.gensim.prepare(model, corpus, id2words)
#vis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def print_words_topic(topic_words):
    num_top_words = len(topic_words)
    fig, ax = plt.subplots(1, 1, figsize=(6, 12))
    plt.ylim(0, num_top_words + 1.0)
    plt.xticks([])
    plt.yticks([])
    plt.title('Topic')
    i = 0
    for (word, share) in topic_words:
        w = word + " (" + str(share) + ")"
        plt.text(0.3, num_top_words - i - 1.0, w)
        plt.tight_layout()
        i += 1
    plt.show()
