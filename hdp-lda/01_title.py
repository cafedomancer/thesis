import pymongo
import sys

from collections import defaultdict
from gensim import corpora, models, similarities
from operator import itemgetter
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from features import analyze_title
from utils import find_pull_requests


# prepare database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.msr14

# split full name into owner and repo
full_name = 'rails/rails'
owner, repo = full_name.split('/')

# extract pull request titles
pullreqs = find_pull_requests(db, owner, repo, is_merged=False)
titles = [p['title'] for p in pullreqs]

# analyze pull request titles
titles = list(map(analyze_title, titles))

# count frequency
usage = defaultdict(int)
for t in titles:
    for w in t:
        usage[w] += 1

# remove words that only appear once
titles = [[w for w in t if usage[w] > 1] for t in titles]

# create topic model
dictionary = corpora.Dictionary(titles)
corpus = [dictionary.doc2bow(t) for t in titles]
model = models.hdpmodel.HdpModel(corpus, id2word=dictionary)

# print topics
# pprint(model.show_topics(formatted=False))
for topic in model.show_topics(topics=10, topn=10, formatted=False):
    topic = itemgetter(1)(topic)
    topic = list(map(itemgetter(0), topic))
    topic = ' '.join(topic)
    print(topic)
