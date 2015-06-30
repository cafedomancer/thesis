import numpy as np
import os
import pymongo
import sys

from collections import defaultdict
from gensim import corpora, models, similarities
from itertools import repeat
from operator import itemgetter
from pprint import pprint
from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from features import clean_body
from utils import find_pull_requests


# prepare database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.msr14

# split full name into owner and repo
full_name = 'rails/rails'
owner, repo = full_name.split('/')

# extract pull request bodies
pullreqs = find_pull_requests(db, owner, repo, is_merged=True)
m_bodies = [p['body'] for p in pullreqs]

pullreqs = find_pull_requests(db, owner, repo, is_merged=False)
u_bodies = [p['body'] for p in pullreqs]

# remove none and empty
m_bodies = list(filter(bool, m_bodies))
u_bodies = list(filter(bool, u_bodies))

# clean pull request bodies
m_bodies = list(map(clean_body, m_bodies))
u_bodies = list(map(clean_body, u_bodies))

# convert numpy arrays
X_orig = m_bodies + u_bodies
y_orig = list(repeat(1, len(m_bodies))) + list(repeat(0, len(u_bodies)))

X = np.asarray(X_orig)
y = np.asarray(y_orig)

# transform documents to tfidf vectors
class MyTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: filter(lambda s: not any(c.isdigit() for c in s), filter(lambda s: not '_' in s, (w for w in analyzer(doc))))

vect = MyTfidfVectorizer(stop_words='english')
X_trans = vect.fit_transform(X)

# train naive bayes model with K-Fold
kf = KFold(n=len(X), n_folds=5, shuffle=True)

for train, test in kf:
    X_train, X_test = X_trans[train], X_trans[test]
    y_train, y_test = y[train], y[test]

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

n = 20
coefs_feats = sorted(zip(clf.coef_[0], vect.get_feature_names()))
top = list(zip(coefs_feats[:n], coefs_feats[:-(n + 1):-1]))
for (c1, f1), (c2, f2) in top:
    print("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (c1, f1, c2, f2))
