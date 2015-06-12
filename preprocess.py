import bson.json_util
import glob
import numpy as np
import os
import pprint
import random

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from utils import DATA_DIR


merge_dir = os.path.join(DATA_DIR, 'merge')
merge_glob = glob.glob('{}/*.json'.format(merge_dir))

comments = []
for fn in merge_glob:
    with open(fn) as f:
        comments.append(bson.json_util.loads(f.read()))
comments = [c['body'] for c in comments]

pprint.pprint(random.choice(comments))


'''
vectorizer = TfidfVectorizer(min_df=10, ngram_range=(2, 2), stop_words='english')
vectorized = vectorizer.fit_transform(comments).toarray()

freq = []
for term, index in vectorizer.vocabulary_.items():
    freq.append((term, np.sum(vectorized[:, index])))

pprint.pprint(sorted(freq, key=lambda x: x[1], reverse=True))
'''
