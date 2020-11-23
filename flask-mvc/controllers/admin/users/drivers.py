
from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required
import constants.constantValue as constants

class VerifyDriver(Resource):
    @staticmethod
    @jwt_required
    def put(id) -> Response:
        data = request.get_json()
        data["status_change_date"] = datetime.datetime.now()
        try:
            update_ = mongo.db.userRegister.update_one(
                {
                    "del_status": False,
                    "_id": bson.ObjectId(id)
                },
                {
                    "$set": data
                }
            )
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })

class DriverList(Resource):
    @staticmethod
    @jwt_required
    def get(status) -> Response:
        msg = ""
        driverList = []
        i=None
        try:
            driverList= mongo.db.userRegister.find({"driverStatus": status,"del_status": False})           
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(driverList))
        })


class GetFreeDriverList(Resource):
    @staticmethod
    @jwt_required
    def get() -> Response:
        msg = ""
        driverList = []
        i=None
        try:
            driverList= mongo.db.userRegister.find({"driverStatus": constants.STATUS_VERIFIED,"del_status": False, "driverOccupied": False})            
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(driverList))
        })
        
        
class AssignDriver(Resource):
    @staticmethod
    @jwt_required
    def get() -> Response:
        msg = ""
        i=None
        try:
            _updateDriver= mongo.db.vehicles.update_one({"driverStatus": constants.STATUS_VERIFIED,"del_status": False, "driverOccupied": False})
            _updateUser= mongo.db.userRegister.update_one({"driverStatus": constants.STATUS_VERIFIED,"del_status": False, "driverOccupied": False})
           
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error
        })
        
class GetDriverInfoById(Resource):
    @staticmethod
    @jwt_required
    def get(id) -> Response:
        msg = ""
        driverInfo = None
        try:
            driverInfo = mongo.db.userRegister.find_one(
                {
                    "_id" : bson.ObjectId(id),
                    "del_status": False
                },
                {
                    "driverInfo" : 1,
                    "reference" : 1,
                    "default_contact_number" : 1
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
            "data" : json.loads(dumps(driverInfo))
        })