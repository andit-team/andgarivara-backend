from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class CityList(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.locationCity.find({})
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


class AddCity(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()

        try:
            dt = mongo.db.locationCity.insert_one(
                {
                    "city": data["city"],
                    "create_date": str(datetime.datetime.now())
                }
            )
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class EditCity(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.locationCity.update_one(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set":
                        {
                            "city": data["city"],
                            "update_date": str(datetime.datetime.now())
                        }
                }
            )
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class DeleteCity(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.locationCity.delete_one(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                }
            )
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })
