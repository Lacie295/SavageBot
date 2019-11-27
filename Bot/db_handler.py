# created by Sami Bosch on Friday, 27 November 2019

# This class handles all accesses to db

import json
import os

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

if "FCs" not in db:
    db['FCs'] = {}


def write():
    with open(filename, "w+") as file:
        json.dump(db, file)
        file.truncate()
        file.close()


def set_fc(u_id, fc):
    db['FCs'][str(u_id)] = fc
    write()


def get_fc(u_id):
    return db['FCs'][str(u_id)] if str(u_id) in db['FCs'] else "No FC provided."
