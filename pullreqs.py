import numpy as np
import pymongo
import re
from pprint import pprint
from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def find_pull_requests(db, owner, repo, is_merged=True):
    query = {
        '$and': [
            {'owner': owner},
            {'repo': repo},
            {'closed_at': {'$ne': None}}
        ]
    }

    if is_merged:
        query['$and'].append({'merged_at': {'$ne': None}})
    else:
        query['$and'].append({'merged_at': None})

    return db.pull_requests.find(query)
    # return list(db.pull_requests.find(query))


# prepare database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.msr14


# split full name into owner and repo
full_name = 'rails/rails'
owner, repo = full_name.split('/')


# extract merged or unmerged pull requests
m_pulls = find_pull_requests(db, owner, repo, is_merged=True)
u_pulls = find_pull_requests(db, owner, repo, is_merged=False)


# extract titles of pull requests
m_titles = [p['title'] for p in m_pulls]
u_titles = [p['title'] for p in u_pulls]


# remove square bracket tags
tag = re.compile('(^\[(.*?)\]|\[(.*?)\]$)', re.MULTILINE | re.DOTALL)
m_titles = [tag.sub('', t) for t in m_titles]
u_titles = [tag.sub('', t) for t in u_titles]


# train logistic regression model
pipeline = Pipeline([
    ('vect', TfidfVectorizer(stop_words='english')),
    ('clf', LogisticRegression())
])

X = m_titles + u_titles
y = ['merge' for _ in range(len(m_titles))] + ['unmerge' for _ in range(len(u_titles))]

X = np.asarray(X)
y = np.asarray(y)

cv = KFold(n=len(X), n_folds=5, shuffle=True)

for train, test in cv:
    X_train, y_train = X[train], y[train]
    X_test, y_test = X[test], y[test]

    pipeline.fit(X_train, y_train)
    print(pipeline.score(X_test, y_test))
