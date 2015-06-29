import bson.json_util
import glob
import json
import os


DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data")

CHART_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "charts")

for d in [DATA_DIR, CHART_DIR]:
    if not os.path.exists(d):
        os.mkdir(d)

filename = os.path.join(DATA_DIR, 'projects.json')
with open(filename) as input:
    PROJECT_LIST = json.load(input)


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

    pullreqs = list(db.pull_requests.find(query))

    return pullreqs


def find_issue_comments(db, owner, repo, issue_ids):
    query = {'$and': [
        {'issue_id': None},
        {'owner': owner},
        {'repo': repo}
    ]}

    comments = []

    for ii in issue_ids:
        query['$and'][0].update({'issue_id': ii})
        comments += db.issue_comments.find(query)

    return comments


def load_issue_comments(is_merged=True):
    if is_merged:
        dirname = os.path.join(DATA_DIR, 'merge')
    else:
        dirname = os.path.join(DATA_DIR, 'unmerged')

    filenames = glob.glob('{}/*.json'.format(dirname))

    comments = []

    for fn in filenames:
        with open(fn) as f:
            comment = bson.json_util.loads(f.read())
            comment = comment['body']
            comments.append(comment)

    return comments


if __name__ == '__main__':
    import pymongo

    client = pymongo.MongoClient('localhost', 27017)
    db = client.msr14

    full_name = 'rails/rails'
    owner, repo = full_name.split('/')

    pullreqs = find_pull_requests(db, owner, repo, is_merged=True)
    print(len(pullreqs))

    pullreq_ids = [p['number'] for p in pullreqs]
    comments = find_issue_comments(db, owner, repo, pullreq_ids)
    print(len(comments))

    comments = load_issue_comments(is_merged=True)
    print(len(comments))
