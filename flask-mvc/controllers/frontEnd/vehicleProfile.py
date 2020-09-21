from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class VehicleProfile(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.vehicles.aggregate(
                [{
                    "$match": {
                        "_id": bsonO.ObjectId(data["_id"])
                    }
                },
                    {
                    "$lookup": {
                        "from": "vehicle_types",
                        "localField": "vehicle_type",
                        "foreignField": "_id",
                        "as": "vehicle_type_details"
                    },

                },
                    {
                    "$lookup": {
                        "from": "users",
                        "localField": "user_id",
                        "foreignField": "_id",
                        "as": "user_details"
                    }
                },
                    {
                    "$lookup": {
                        "from": "locationCity",
                        "localField": "city",
                        "foreignField": "_id",
                        "as": "location_details"
                    }
                }
                ])
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True

        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
