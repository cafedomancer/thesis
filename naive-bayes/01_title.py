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

from features import clean_title
from utils import find_pull_requests


# prepare database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.msr14

# split full name into owner and repo
full_name = 'rails/rails'
owner, repo = full_name.split('/')

# extract pull request titles
pullreqs = find_pull_requests(db, owner, repo, is_merged=True)
m_titles = [p['title'] for p in pullreqs]

pullreqs = find_pull_requests(db, owner, repo, is_merged=False)
u_titles = [p['title'] for p in pullreqs]

# clean pull request titles
m_titles = list(map(clean_title, m_titles))
u_titles = list(map(clean_title, u_titles))

# convert numpy arrays
X_orig = m_titles + u_titles
y_orig = list(repeat(1, len(m_titles))) + list(repeat(0, len(u_titles)))

X = np.asarray(X_orig)
y = np.asarray(y_orig)

# transform documents to tfidf vectors
vect = TfidfVectorizer(stop_words='english')
X_trans = vect.fit_transform(X)

# train naive bayes model with K-Fold
kf = KFold(n=len(X), n_folds=5, shuffle=True)

for train, test in kf:
    X_train, X_test = X_trans[train], X_trans[test]
    y_train, y_test = y[train], y[test]

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)
    print('TRAIN: {:f}, TEST: {:f}'.format(train_score, test_score))
