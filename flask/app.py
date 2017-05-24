#!/usr/bin/env python3

from flask import Flask
from flask import render_template
import pymongo
import base64

app = Flask(__name__)

collection = pymongo.MongoClient('localhost', 27017).mitm.page


def find_images(mongo_collection, start=0, size=20):
    return list(map(
        lambda c: {
            'id': c['_id'],
            'contentType': c['response:headers']['Content-Type'].strip(),
            'imageBase64': base64.b64encode(c['response:content']).decode('utf-8').strip(),
        },
        mongo_collection.find({'response:headers.Content-Type': {'$regex': '^image'}}).skip(start).limit(size)
    ))


@app.route('/')
@app.route('/<int:start>')
@app.route('/<int:start>/<int:size>')
def home(start=0, size=20):
    return render_template('images.html', images=find_images(collection, start, size))


if __name__ == '__main__':
    app.run()
