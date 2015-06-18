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
