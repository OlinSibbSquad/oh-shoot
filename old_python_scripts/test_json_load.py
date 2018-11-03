import json

from pprint import pprint

with open('SibbSquadV2-8e1c8113e39c.json') as f:
    data = json.load(f)

pprint(data)
print(data["private_key"])
