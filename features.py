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
