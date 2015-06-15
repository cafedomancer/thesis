import bson.json_util
import sys
import misaka


with open(sys.argv[1]) as f:
    bson = bson.json_util.loads(f.read())
comment = bson['body']
print(misaka.html(comment))
