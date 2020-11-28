from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


class FuelTypeList(Resource):
    @staticmethod    
    def get() -> Response:
        dt = None        
        try:
            dt = mongo.db.fuelType.find().sort("create_date")
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
    @jwt_required
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
    @jwt_required
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

class FuelTypeById(Resource):
    @staticmethod
    @jwt_required
    def get(id) -> Response: 
        allData = None
        try:
            allData = mongo.db.fuelType.find_one(
                {
                    "_id": bsonO.ObjectId(id)
                })            
            msg = "SUCCESSFUL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "data": json.loads(dumps(allData)),
            "msg": msg,
            "error": error
        })

class DeleteFuelType(Resource):
    @staticmethod
    @jwt_required
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
