import bson.json_util
import json
import os
import pprint
import pymongo

from utils import DATA_DIR


def find_pull_request_ids(db, owner, repo, is_merged=True):
    query = {
        '$and': [
            {'owner': owner},
            {'repo': repo},
            {'closed_at': {'$ne': None}}
        ]
    }

    if is_merged:
        query['$and'].append({'merged_at': {'$ne': None}})
    else:
        query['$and'].append({'merged_at': None})

    return [p['number'] for p in db.pull_requests.find(query)]


def find_issue_comments(db, owner, repo, issue_ids):
    query = {
        '$and': [
            {'owner': owner},
            {'repo': repo},
            {'issue_id': None}
        ]
    }

    all_comments = []
    for issue_id in issue_ids:
        query['$and'][2]['issue_id'] = issue_id  # need to be refactored
        comments = db.issue_comments.find(query)
        all_comments += comments

    return all_comments


# prepare database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.msr14


# split full name into owner and repo
full_name = 'rails/rails'
owner, repo = full_name.split('/')


# extract the ids of merged/unmerged pull requests
merged_ids = find_pull_request_ids(db, owner, repo, is_merged=True)
unmerged_ids = find_pull_request_ids(db, owner, repo, is_merged=False)


# get the issue comments associated with the specific pull request number
merged_comments = find_issue_comments(db, owner, repo, merged_ids)
unmerge_comments = find_issue_comments(db, owner, repo, unmerged_ids)
all_comments = [merged_comments, unmerge_comments]


# dump issue comments
dirs = ['merge', 'unmerge']
dirs = [os.path.join(DATA_DIR, d) for d in dirs]

for d in dirs:
    if not os.path.exists(d):
        os.mkdir(d)

for d, cs in zip(dirs, all_comments):
    for c in cs:
        fn = os.path.join(d, '{}.json'.format(c['id']))
        with open(fn, 'w') as output:
            output.write(bson.json_util.dumps(c))
            output.write('\n')
