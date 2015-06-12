import bson.json_util
import json
import pprint
import pymongo


# load the full names of all projects if necessary
# with open('data/projects.json') as input:
#     projects = json.load(input)
# projects = [p.split('/') for p in projects]

# pprint.pprint(projects)


# prepare database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.msr14

# pprint.pprint(db.collection_names())


# split full name into owner and repo
full_name = 'rails/rails'
owner, repo = full_name.split('/')

# pprint.pprint(owner)
# pprint.pprint(repo)


# extract the ids of merged/unmerged pull requests
pull_requests = db.pull_requests
query = {
    '$and': [
        {'owner': owner},
        {'repo': repo},
        {'closed_at': {'$ne': None}},
        {'merged_at': {'$ne': None}}
    ]
}

pull_ids = [p['number'] for p in pull_requests.find(query)]

# pprint.pprint(pull_ids)


# get the issue comments associated with the specific pull request number
issue_comments = db.issue_comments

for issue_id in pull_ids:
    query = {
        '$and': [
            {'owner': owner},
            {'repo': repo},
            {'issue_id': issue_id}
        ]
    }
    comments = issue_comments.find(query)
    for c in comments:
        fname = 'data/{}.json'.format(c['id'])
        with open(fname, 'w') as output:
            output.write(bson.json_util.dumps(c))
            output.write('\n')
