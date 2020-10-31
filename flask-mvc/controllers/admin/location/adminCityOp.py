from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class CityList(Resource):
    @staticmethod
    def get() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.cities.find({})
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
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
            indexCreate = mongo.db.cities.create_index(
                'city', unique=True)
            dt = mongo.db.cities.insert_one(
                {
                    "city": data["city"].upper(),
                    "create_date": datetime.datetime.now()
                }
            )
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class EditCity(Resource):
    @staticmethod
    def put() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.cities.update_one(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set":
                        {
                            "city": data["city"].upper(),
                            "update_date": datetime.datetime.now()
                        }
                }
            )
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class DeleteCity(Resource):
    @staticmethod
    def delete() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.cities.delete_one(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                }
            )
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })
