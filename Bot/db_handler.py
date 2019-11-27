# created by Sami Bosch on Friday, 27 November 2019

# This class handles all accesses to db

import json
import os

import discord

data = "../data.json"
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, data)
if not os.path.exists(filename):
    with open(filename, "w+") as f:
        json.dump({"FCs": {}}, f)
        f.truncate()
        f.close()

with open(filename, "r+") as f:
    db = json.load(f)
    f.close()

if "songs" not in db:
    db['FCs'] = {}
