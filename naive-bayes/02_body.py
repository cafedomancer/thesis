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
vect = TfidfVectorizer(stop_words='english')
X_trans = vect.fit_transform(X)

# train naive bayes model with K-Fold
kf = KFold(n=len(X), n_folds=5, shuffle=True)

train_scores = []
test_scores = []

for train, test in kf:
    X_train, X_test = X_trans[train], X_trans[test]
    y_train, y_test = y[train], y[test]

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)

    train_scores.append(train_score)
    test_scores.append(test_score)

print('         MEAN     STDDEV')
print('TRAIN: {:f}, {:f}'.format(np.mean(train_scores), np.std(train_scores)))
print('TEST : {:f}, {:f}'.format(np.mean(test_scores), np.std(test_scores)))
