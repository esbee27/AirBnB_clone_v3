#!/usr/bin/python3

from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.engine import file_storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    msg = {"status": "OK"}
    return jsonify(msg)

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    dic = {}
    for cls in file_storage.classes.keys():
        dic[cls] = storage.count(cls)
    return jsonify(dic)


if __name__ == "__main__":
    pass