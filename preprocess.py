import bson.json_util
import glob
import misaka
import numpy as np
import os
import pprint
import re

from bs4 import BeautifulSoup
from email_reply_parser import EmailReplyParser
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from utils import DATA_DIR


# load JSON files of issue comments
merge_dir = os.path.join(DATA_DIR, 'unmerge')
merge_glob = glob.glob('{}/*.json'.format(merge_dir))

comments = []
for fn in merge_glob[:5000]:
    with open(fn) as f:
        comments.append(bson.json_util.loads(f.read()))


# extract body text
comments = [c['body'] for c in comments]
# get rid of carriage return
comments = [c.replace('\r\n', '\n') for c in comments]
# retrieve email replay
comments = [EmailReplyParser.parse_reply(c) for c in comments]
# convert markdown to html
comments = [misaka.html(c) for c in comments]
# convert html to plain text
comments = [BeautifulSoup(c).get_text() for c in comments]
# remove URLs
comments = [re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', '', c) for c in comments]


# random.shuffle(comments)
# comments = sorted(comments, key=len, reverse=True)
# comments = comments[:1000]
# for i, c in enumerate(comments):
#     if '```' in c and '(http' in c:
#         print(i)
#         print(c)
#         print('-'*100)


vectorizer = CountVectorizer(min_df=2, ngram_range=(4, 4), stop_words='english')
vectorized = vectorizer.fit_transform(comments).toarray()

freq = []
for term, index in vectorizer.vocabulary_.items():
    freq.append((term, np.sum(vectorized[:, index])))

pprint.pprint(sorted(freq, key=lambda x: x[1], reverse=True))
