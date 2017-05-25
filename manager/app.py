#!/usr/bin/env python3

from flask import Flask
from flask import render_template
import pymongo
import base64

import yaml
import os

app = Flask(__name__)

# https://stackoverflow.com/questions/8299270/ultimate-answer-to-relative-python-imports/8300343#8300343
# yaml config
with open(os.path.dirname(os.path.realpath(__file__)) + '/..' '/config.yml') as yamlfile:
    cfg = yaml.load(yamlfile)
    cfg_mongo = cfg['mongo']

# mongo db
collection = pymongo.MongoClient(cfg_mongo['host'], cfg_mongo['port']) \
    .get_database(cfg_mongo['database']) \
    .get_collection('page')


def find_images(mongo_collection, start=0, size=20):
    return list(map(
        lambda c: {
            'id': c['_id'],
            'contentType': c['response:headers']['Content-Type'].strip(),
            'imageBase64': base64.b64encode(c['response:content']).decode('utf-8').strip(),
        },
        mongo_collection
            .find({'response:headers.Content-Type': {'$regex': '^image'}})
            .sort([('_id', pymongo.DESCENDING)])
            .skip(start)
            .limit(size)
    ))


@app.route('/')
@app.route('/<int:start>')
@app.route('/<int:start>/<int:size>')
def home(start=0, size=20):
    return render_template('images.html', images=find_images(collection, start, size))


if __name__ == '__main__':
    app.run()
