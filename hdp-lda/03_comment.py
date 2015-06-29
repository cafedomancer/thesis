import os
import pymongo
import sys

from collections import defaultdict
from gensim import corpora, models, similarities
from operator import itemgetter
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from features import analyze_comment
from utils import load_issue_comments


# prepare database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.msr14

# split full name into owner and repo
full_name = 'rails/rails'
owner, repo = full_name.split('/')

# load issue comments
comments = load_issue_comments(is_merged=False)

# analyze issue comments
comments = list(map(analyze_comment, comments))

# count frequency
usage = defaultdict(int)
for c in comments:
    for w in c:
        usage[w] += 1

# remove words that only appear once
comments = [[w for w in c if usage[w] > 1] for c in comments]

# cut off common words
limit = len(comments) / 10
common = [w for w in usage if usage[w] > limit]
common = set(common)
comments = [filter(lambda w: w not in common, c) for c in comments]

# create topic model
dictionary = corpora.Dictionary(comments)
corpus = [dictionary.doc2bow(c) for c in comments]
model = models.hdpmodel.HdpModel(corpus, id2word=dictionary)

# print topics
# pprint(model.show_topics(formatted=False))
for topic in model.show_topics(topics=10, topn=10, formatted=False):
    topic = itemgetter(1)(topic)
    topic = list(map(itemgetter(0), topic))
    topic = ' '.join(topic)
    print(topic)
