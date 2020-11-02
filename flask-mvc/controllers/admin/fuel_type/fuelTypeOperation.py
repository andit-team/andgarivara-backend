from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class FuelTypeList(Resource):
    @staticmethod
    def get() -> Response:
        dt = None
        # data = request.get_json()
        # try:
        #     if data["_id"]:
        #         dt = mongo.db.fuelType.find({"_id":bsonO.objectID(data["_id"])})
        #     else:
        #          dt = mongo.db.fuelType.find()
        try:
            dt = mongo.db.fuelType.find()
            msg = "SUCCESSFUL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "data": json.loads(dumps(dt)),
            "msg": msg,
            "error": error
        })


class AddFuelType(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        dt = {
            "title": data["title"].upper(),
            "rate": data["rate"],
            "create_date": datetime.datetime.now()
        }
        try:
            indexCreate = mongo.db.fuelType.create_index(
                'title', unique=True)
            _insertOp = mongo.db.fuelType.insert_one(dt)
            msg = "SUCCESSFUL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "data": json.loads(dumps(data)),
            "msg": msg,
            "error": error
        })


class EditFuelType(Resource):
    @staticmethod
    def put() -> Response:
        data = request.get_json()
        try:

            _updateOp = mongo.db.fuelType.update_one(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set":
                        {
                            "title": data["title"].upper(),
                            "rate": data["rate"],
                            "update_date": datetime.datetime.now()
                        }
                })
            msg = "SUCCESSFUL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "data": json.loads(dumps(data)),
            "msg": msg,
            "error": error
        })


class DeleteFuelType(Resource):
    @staticmethod
    def delete() -> Response:
        data = request.get_json()
        try:
            mongo.db.fuelType.delete_one(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                })
            msg = "SUCCESSFUL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "data": json.loads(dumps(data)),
            "msg": msg,
            "error": error
        })
