import pymongo
import re
from collections import defaultdict
from gensim import corpora, models, similarities
from sklearn.feature_extraction.text import CountVectorizer


def find_pull_requests(db, owner=None, repo=None, is_merged=True):
    query = {'$and': [
        {'closed_at': {'$ne': None}}
    ]}

    if owner and repo:
        query['$and'].append({'owner': owner})
        query['$and'].append({'repo': repo})

    if is_merged:
        query['$and'].append({'merged_at': {'$ne': None}})
    else:
        query['$and'].append({'merged_at': None})

    return db.pull_requests.find(query)


def analyze_pull_request_title(title):
    tag = re.compile(r'\[(.*?)\]', re.MULTILINE | re.DOTALL)
    title = tag.sub('', title)

    code = re.compile(r'\w*::\w*[.#]*\w*\.?\(?\w*\)?\??', re.MULTILINE | re.DOTALL)
    title = code.sub('', title)

    code = re.compile(r'\w*#\w*', re.MULTILINE | re.DOTALL)
    title = code.sub('', title)

    issue = re.compile(r'#[0-9]+', re.MULTILINE | re.DOTALL)
    title = issue.sub('', title)

    url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.MULTILINE | re.DOTALL)
    title = url.sub('', title)

    vectorizer = CountVectorizer(stop_words='english')
    analyzer = vectorizer.build_analyzer()

    title = analyzer(title)

    title = list(filter(lambda s: not '_' in s, title))
    title = list(filter(lambda s: not s.isdigit(), title))

    return title


if __name__ == '__main__':
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
    titles = list(map(analyze_pull_request_title, titles))

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

    import pprint
    pprint.pprint(model.show_topics(formatted=False))
