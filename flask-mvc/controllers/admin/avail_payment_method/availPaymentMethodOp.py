from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class AvailPaymentMethodTypeList(Resource):
    @staticmethod
    def get() -> Response:
        try:
            dt = mongo.db.availPaymentMethod.find()
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


class AddAvailPaymentMethodType(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        dt = {
            "title": data["title"],
            "image": data["image"],
            "create_date": datetime.datetime.now()
        }
        try:
            indexCreate = mongo.db.availPaymentMethod.create_index(
                'title', unique=True)
            _insertOp = mongo.db.availPaymentMethod.insert_one(dt)
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


class EditAvailPaymentMethodType(Resource):
    @staticmethod
    def put() -> Response:
        data = request.get_json()
        try:

            _updateOp = mongo.db.availPaymentMethod.update_one(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set":
                        {
                            "title": data["title"],
                            "image": data["image"],
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


class DeleteAvailPaymentMethodType(Resource):
    @staticmethod
    def delete() -> Response:
        data = request.get_json()
        try:
            mongo.db.availPaymentMethod.delete_one(
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
