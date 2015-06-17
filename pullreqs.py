import numpy as np
import pymongo
import re
from pprint import pprint
from matplotlib import pylab
from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve, roc_curve, auc
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


def plot_roc(auc_score, name, tpr, fpr, label=None):
    pylab.clf()
    pylab.figure(num=None, figsize=(5, 4))
    pylab.grid(True)
    pylab.plot([0, 1], [0, 1], 'k--')
    pylab.plot(fpr, tpr)
    pylab.fill_between(fpr, tpr, alpha=0.5)
    pylab.xlim([0.0, 1.0])
    pylab.ylim([0.0, 1.0])
    pylab.xlabel('False Positive Rate')
    pylab.ylabel('True Positive Rate')
    pylab.title('ROC curve (AUC = %0.2f) / %s' %
                (auc_score, label), verticalalignment="bottom")
    pylab.legend(loc="lower right")
    filename = name.replace(" ", "_")
    pylab.savefig("charts/roc_" + filename + ".png", bbox_inches="tight")


def plot_pr(auc_score, name, phase, precision, recall, label=None):
    pylab.clf()
    pylab.figure(num=None, figsize=(5, 4))
    pylab.grid(True)
    pylab.fill_between(recall, precision, alpha=0.5)
    pylab.plot(recall, precision, lw=1)
    pylab.xlim([0.0, 1.0])
    pylab.ylim([0.0, 1.0])
    pylab.xlabel('Recall')
    pylab.ylabel('Precision')
    pylab.title('P/R curve (AUC=%0.2f) / %s' % (auc_score, label))
    filename = name.replace(" ", "_")
    pylab.savefig('charts/pr_%s_%s.png' % (filename, phase), bbox_inches="tight")


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

# remove URLs
# url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.MULTILINE | re.DOTALL)
# m_titles = [url.sub('', t) for t in m_titles]
# u_titles = [url.sub('', t) for t in u_titles]


# create topic model
from gensim import corpora, models, similarities
vectorizer = CountVectorizer(stop_words='english')
analyzer = vectorizer.build_analyzer()

m_titles = [analyzer(t) for t in m_titles]
u_titles = [analyzer(t) for t in u_titles]

dictionary = corpora.Dictionary(m_titles)
corpus = [dictionary.doc2bow(t) for t in m_titles]
tfidf = models.TfidfModel(corpus)
model = models.hdpmodel.HdpModel(corpus, id2word=dictionary)

pprint(model.show_topics(formatted=False))


'''
# prepare numpy arrays
X_orig = m_titles + u_titles
y_orig = ['merge' for _ in range(len(m_titles))] + ['unmerge' for _ in range(len(u_titles))]
y_orig = [1 for _ in range(len(m_titles))] + [0 for _ in range(len(u_titles))]

X = np.asarray(X_orig)
y = np.asarray(y_orig)


# count ngram frequency
vect = CountVectorizer(ngram_range=(2, 2), stop_words='english')
#trans = vect.fit_transform(m_titles)
trans = vect.fit_transform(u_titles)
freq = [(t, trans[:, i].sum()) for t, i in vect.vocabulary_.items()]
pprint(sorted(freq, key=lambda x: x[1], reverse=True)[:50])


# transform documents to tfidf vectors
vect = TfidfVectorizer(ngram_range=(1, 3), stop_words='english')
X_trans = vect.fit_transform(X)


# train naive bayes model with K-Fold
kf = KFold(n=len(X), n_folds=5, shuffle=True)

name = 'NB ngram'
phase = '01'
scores = []
pr_scores = []
precisions, recalls, thresholds = [], [], []

roc_scores = []
fprs, tprs = [], []

for train_index, test_index in kf:
    X_train, X_test = X_trans[train_index], X_trans[test_index]
    y_train, y_test = y[train_index], y[test_index]

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)
    print('train:', train_score, 'test:', test_score)

    scores.append(test_score)

    # for plotting precision recall curve
    proba = clf.predict_proba(X_test)

    fpr, tpr, roc_thresholds = roc_curve(y_test, proba[:, 1])
    precision, recall, pr_thresholds = precision_recall_curve(y_test, proba[:, 1])

    roc_scores.append(auc(fpr, tpr))
    fprs.append(fpr)
    tprs.append(tpr)

    pr_scores.append(auc(recall, precision))
    precisions.append(precision)
    recalls.append(recall)
    thresholds.append(pr_thresholds)

print('MEAN:', np.mean(scores), 'STDDEV:', np.std(scores))

# scores_to_sort = pr_scores
# median = np.argsort(scores_to_sort)[len(scores_to_sort) / 2]
# plot_pr(pr_scores[median], name, phase, precisions[median], recalls[median], label=name)

# scores_to_sort = roc_scores
# median = np.argsort(scores_to_sort)[len(scores_to_sort) / 2]
# plot_roc(roc_scores[median], name, tprs[median], fprs[median], label=name)
'''
