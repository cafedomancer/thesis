import bson.json_util
import os
import pymongo

from utils import DATA_DIR, find_pull_requests, find_issue_comments


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
