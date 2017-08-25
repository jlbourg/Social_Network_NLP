from sklearn.manifold import TSNE
from collections      import Counter
from matplotlib       import pylab

import plotly.plotly as py
import tensorflow    as tf
import pandas as pd
import numpy  as np

import os
import re
import time
import random
import logging

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/alpha_shape.csv')
df.head()

scatter = dict(
    mode = "markers",
    name = "y",
    type = "scatter3d",    
    x = df['x'], y = df['y'], z = df['z'],
    marker = dict( size=3, color="rgb(23, 190, 207)" )
)
clusters = dict(
    alphahull = 7,
    name = "y",
    opacity = 0.1,
    type = "mesh3d",    
    x = df['x'], y = df['y'], z = df['z']
)
layout = dict(
    title = '3d point clustering',
    scene = dict(
        xaxis = dict( zeroline=False ),
        yaxis = dict( zeroline=False ),
        zaxis = dict( zeroline=False ),
    )
)
#fig = dict( data=[scatter, clusters], layout=layout )
#py.plot(fig, filename='3d point clustering')

#----------------------------------------------------
VOCAB_SIZE    = 5000
TXT_FILE_NAME = '../word_embeddings/data.txt'
with open(TXT_FILE_NAME) as txt_file:
    words = tf.compat.as_str(txt_file.read()).split()


pre_vocab = [['NULL', -1]] + Counter(words).most_common(VOCAB_SIZE - 1)

# Debug
#print(pre_vocab[:20])

# Because hash is faster when searching word's index
hash_map = dict()
for idx, (a_word, occurrence) in enumerate(pre_vocab):
    hash_map[a_word] = idx

data = []
nulls = 0

# Words with occurence rank higher than VOCAB_SIZE (rare words) will be replaces with Null
for a_word in words:
    if a_word in hash_map:
        a_word_idx = hash_map[a_word]
    else:
        a_word_idx = 0
        nulls += 1
    data.append(a_word_idx)

pre_vocab[0][1] = nulls

# Turn values into keys, and keys into values
key_reverse_hash_map = dict(zip(hash_map.values(), hash_map.keys()))
print(type(key_reverse_hash_map))
print(len(key_reverse_hash_map))
print('---------------------------------------------')
with open('key_reverse_hash_map','wb') as numpyFile:
    np.save(numpyFile, key_reverse_hash_map)
#----------------------------------------------------

# Add ops to save and restore all the variables.
num_points = 400
VOCAB_SIZE = 5000
embedding_size = 128 

#with open('../word_embeddings/key_reverse_hash_map','rb') as numpyFile:
#    key_reverse_hash_map = np.load(numpyFile)
#print(type(key_reverse_hash_map))
#print(len(key_reverse_hash_map))


tf.reset_default_graph()

embeddings = tf.get_variable("embeddings",[VOCAB_SIZE, embedding_size])
norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
normalized_embeddings = embeddings / norm

saver = tf.train.Saver()

# Use the saver object normally after that.
with tf.Session() as sess:
    embeddings.initializer.run()
    saver.restore(sess, "../word_embeddings/model_nazi2/saved_session.model-90000") 
    final_embeddings = normalized_embeddings.eval()

tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
two_d_embeddings = tsne.fit_transform(final_embeddings[1:num_points+1, :])


def plot(embeddings, labels):
    assert embeddings.shape[0] >= len(labels), 'More labels than embeddings'
    pylab.figure(figsize=(15,15))  # in inches
    for i, label in enumerate(labels):
        x, y = embeddings[i,:]
        pylab.scatter(x, y)
        pylab.annotate(label, xy=(x, y), xytext=(5, 2), textcoords='offset points',
                     ha='right', va='bottom')
    pylab.show()

words = [key_reverse_hash_map[i] for i in range(1, num_points+1)]
plot(two_d_embeddings, words) 
