import bson.json_util
import os
import pymongo

from utils import DATA_DIR


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


def jsonify_issue_comments(db, owner, repo, is_merged=True):
    pullreqs = find_pull_requests(db, owner, repo, is_merged)
    pullreq_ids = [p['number'] for p in pullreqs]
    comments = find_issue_comments(db, owner, repo, pullreq_ids)

    dirname = os.path.join(DATA_DIR, 'merge' if is_merged else 'unmerge')

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    for c in comments:
        filename = os.path.join(dirname, '{}.json'.format(c['id']))
        with open(filename, 'w') as f:
            f.write(bson.json_util.dumps(c) + '\n')


if __name__ == '__main__':
    # prepare database connection
    client = pymongo.MongoClient('localhost', 27017)
    db = client.msr14

    # split full name into owner and repo
    full_name = 'rails/rails'
    owner, repo = full_name.split('/')

    # jsonify issue comments
    jsonify_issue_comments(db, owner, repo, is_merged=True)
    jsonify_issue_comments(db, owner, repo, is_merged=False)
