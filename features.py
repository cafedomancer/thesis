import re

from email_reply_parser import EmailReplyParser
from sklearn.feature_extraction.text import CountVectorizer


def clean_title(title):
    tag = re.compile(r'\[(.*?)\]', re.MULTILINE | re.DOTALL)
    title = tag.sub('', title)

    ruby = re.compile(r'(\w+/)*\w*\.rb', re.MULTILINE | re.DOTALL)
    title = ruby.sub('', title)

    code = re.compile(r'\w+::\w+(?:::\w+)*(?:\.\w+\??|#\w+\??)?', re.MULTILINE | re.DOTALL)
    title = code.sub('', title)

    return title


def analyze_title(title):
    vectorizer = CountVectorizer(stop_words='english')
    analyzer = vectorizer.build_analyzer()

    title = analyzer(clean_title(title))

    title = list(filter(lambda s: not '_' in s, title))
    body = list(filter(lambda s: not any(c.isdigit() for c in s), title))

    return title


def clean_body(body):
    block = re.compile(r'```.*?```|<pre>.*?</pre>|^(?: {4,}|\t+).*?$', re.MULTILINE | re.DOTALL)
    body = block.sub('', body)

    inline = re.compile(r'`.*?`', re.MULTILINE | re.DOTALL)
    body = inline.sub('', body)

    link = re.compile(r'!?\[(.*?)\]\(.*?\)', re.MULTILINE | re.DOTALL)
    body = link.sub(r'\1', body)

    url = re.compile(r'\(?https?://\S+\)?', re.MULTILINE | re.DOTALL)
    body = url.sub('', body)

    code = re.compile(r'(?:[A-Z][a-z]*){2,}(?:::(?:[A-Z][a-z]*)+)*(?:\.|#\S+)*', re.MULTILINE | re.DOTALL)
    body = code.sub('', body)

    ruby = re.compile(r'(?:\w+/)*\w*\.rb', re.MULTILINE | re.DOTALL)
    body = ruby.sub('', body)

    return body


def analyze_body(body):
    vectorizer = CountVectorizer(stop_words='english')
    analyzer = vectorizer.build_analyzer()

    body = analyzer(clean_body(body))

    body = list(filter(lambda s: not '_' in s, body))
    body = list(filter(lambda s: not any(c.isdigit() for c in s), body))

    return body


def clean_comment(comment):
    comment = EmailReplyParser.parse_reply(comment)

    block = re.compile(r'`{3,}.*?`{3,}|<pre>.*?</pre>|^(?: {4,}|\t+).*?$', re.MULTILINE | re.DOTALL)
    comment = block.sub('', comment)

    inline = re.compile(r'`.*?`', re.MULTILINE | re.DOTALL)
    comment = inline.sub('', comment)

    link = re.compile(r'!?\[(.*?)\]\(.*?\)', re.MULTILINE | re.DOTALL)
    comment = link.sub(r'\1', comment)

    url = re.compile(r'\(?https?://\S+\)?', re.MULTILINE | re.DOTALL)
    comment = url.sub('', comment)

    code = re.compile(r'(?:[A-Z][a-z]*){2,}(?:::(?:[A-Z][a-z]*)+)*(?:\.|#\S+)*', re.MULTILINE | re.DOTALL)
    comment = code.sub('', comment)

    ruby = re.compile(r'(?:\w+/)*\w*\.rb', re.MULTILINE | re.DOTALL)
    comment = ruby.sub('', comment)

    emoji = re.compile(r':\S+:', re.MULTILINE | re.DOTALL)
    comment = emoji.sub('', comment)

    return comment


def analyze_comment(comment):
    vectorizer = CountVectorizer(stop_words='english')
    analyzer = vectorizer.build_analyzer()

    comment = analyzer(clean_comment(comment))

    comment = list(filter(lambda s: not '_' in s, comment))
    comment = list(filter(lambda s: not any(c.isdigit() for c in s), comment))

    return comment


if __name__ == '__main__':
    import pymongo

    from collections import defaultdict
    from operator import itemgetter
    from pprint import pprint
    from utils import find_pull_requests, load_issue_comments

    client = pymongo.MongoClient('localhost', 27017)
    db = client.msr14

    full_name = 'rails/rails'
    owner, repo = full_name.split('/')

    # pullreqs = find_pull_requests(db, owner, repo, is_merged=True)
    comments = load_issue_comments(is_merged=True)

    usage = defaultdict(int)

    # titles = [p['title'] for p in pullreqs]
    # titles = list(map(analyze_title, titles))
    # for t in titles:
    #     for w in t:
    #         usage[w] += 1

    # bodies = [p['body'] for p in pullreqs]
    # bodies = list(filter(bool, bodies))
    # bodies = list(map(analyze_body, bodies))
    # for b in bodies:
    #     for w in b:
    #         usage[w] += 1

    comments = list(map(analyze_comment, comments))
    for c in comments:
        for w in c:
            usage[w] += 1

    pprint(sorted(usage.items(), key=itemgetter(1), reverse=True))




'''
import bson.json_util
import glob
import misaka
import numpy as np
import os
import pprint
import random
import re

from bs4 import BeautifulSoup
from email_reply_parser import EmailReplyParser
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from utils import DATA_DIR


# load JSON files of issue comments
merge_dir = os.path.join(DATA_DIR, 'merge')
merge_glob = glob.glob('{}/*.json'.format(merge_dir))

taints = ['/Users/cafedomancer/Desktop/thesis/data/merge/1115656.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/13427639.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/20442668.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/24924043.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/6049037.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/6384150.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/6603791.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/6604355.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/6604472.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/6874873.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/6984582.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/7287851.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/7642324.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/8301966.json',
          '/Users/cafedomancer/Desktop/thesis/data/merge/8757750.json']

for t in taints:
    merge_glob.remove(t)

unmerge_dir = os.path.join(DATA_DIR, 'unmerge')
unmerge_glob = glob.glob('{}/*.json'.format(unmerge_dir))

comments = []
for fn in merge_glob:
    with open(fn) as f:
        comment = bson.json_util.loads(f.read())
        comment = comment['body']
        comment = comment.replace('\r\n', '\n')
        comments.append(comment)


raws = comments


# remove code blocks
code_pattern = re.compile('^```(.*?)```$', re.MULTILINE | re.DOTALL)
comments = [code_pattern.sub('', c) for c in comments]

# remove inline codes
inline_code_pattern = re.compile('`(.*?)`', re.MULTILINE | re.DOTALL)
comments = [inline_code_pattern.sub('', c) for c in comments]

# remove email replay
comments = [EmailReplyParser.parse_reply(c) for c in comments]

# remove emojis
emoji_pattern = re.compile(':(.*?)heart:', re.MULTILINE | re.DOTALL)
comments = [emoji_pattern.sub('', c) for c in comments]

# remove URLs
url_pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.MULTILINE | re.DOTALL)
comments = [url_pattern.sub('', c) for c in comments]


# test substitution
zips = list(zip(merge_glob, raws, comments))
for g, r, c in zips:
    if emoji_pattern.search(r):
        # print(g)
        # print('=' * 80)
        print(r)
        print('-' * 80)
        print(c)
        print('=' * 80)


vectorizer = CountVectorizer(min_df=10, ngram_range=(3, 3), stop_words='english')
vectorized = vectorizer.fit_transform(comments).toarray()
freq = []
for term, index in vectorizer.vocabulary_.items():
    freq.append((term, np.sum(vectorized[:, index])))
pprint.pprint(sorted(freq, key=lambda x: x[1], reverse=True))


# extract body text
# comments = [c['body'] for c in comments]
# get rid of carriage return
# comments = [c.replace('\r\n', '\n') for c in comments]
# retrieve email replay
# comments = [EmailReplyParser.parse_reply(c) for c in comments]
# convert markdown to html
# comments = [misaka.html(c) for c in comments]
# convert html to plain text
# comments = [BeautifulSoup(c).get_text() for c in comments]
# remove URLs
# comments = [re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', '', c) for c in comments]
'''
