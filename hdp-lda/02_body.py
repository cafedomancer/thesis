import os
import pymongo
import sys

from collections import defaultdict
from gensim import corpora, models, similarities
from operator import itemgetter
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from features import analyze_body
from utils import find_pull_requests


# prepare database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.msr14

# split full name into owner and repo
full_name = 'rails/rails'
owner, repo = full_name.split('/')

# extract pull request bodies
pullreqs = find_pull_requests(db, owner, repo, is_merged=False)
bodies = [p['body'] for p in pullreqs]

# remove None and empty string
bodies = list(filter(bool, bodies))

# analyze pull request bodies
bodies = list(map(analyze_body, bodies))

# count frequency
usage = defaultdict(int)
for b in bodies:
    for w in b:
        usage[w] += 1

# remove words that only appear once
bodies = [[w for w in b if usage[w] > 1] for b in bodies]

# cut off common words
limit = len(bodies) / 10
common = [w for w in usage if usage[w] > limit]
common = set(common)
bodies = [filter(lambda w: w not in common, b) for b in bodies]

# create topic model
dictionary = corpora.Dictionary(bodies)
corpus = [dictionary.doc2bow(t) for t in bodies]
model = models.hdpmodel.HdpModel(corpus, id2word=dictionary)

# print topics
# pprint(model.show_topics(formatted=False))
for topic in model.show_topics(topics=10, topn=10, formatted=False):
    topic = itemgetter(1)(topic)
    topic = list(map(itemgetter(0), topic))
    topic = ' '.join(topic)
    print(topic)
