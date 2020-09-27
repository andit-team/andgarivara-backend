from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class HomePage(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        err_msg=None
        try:
            dtLocation = mongo.db.locationCity.find({})
            dtVT = mongo.db.vehicle_types.find({})
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = "FAILED"
            error = True
            err_msg=ex
        return jsonify({
            "msg": msg,
            "error": error,
            "err_msg" : str(err_msg),
            "loc_data": json.loads(dumps(dtLocation)),
            "vichle_type_data": json.loads(dumps(dtVT))
        })