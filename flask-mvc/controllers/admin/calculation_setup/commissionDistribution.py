from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


class GetAllComDistData(Resource):
    @staticmethod 
    @jwt_required   
    def get() -> Response:
        dt = None        
        try:
            dt = mongo.db.commissionDistribution.find_one()
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
        
class SetupComDistData(Resource):
    @staticmethod 
    @jwt_required   
    def get() -> Response:
        data = request.get_json()
        dt = None 
        dataList = {
            "ownerCom": data["ownerCom"],
            "driverCom": data["driverCom"],
            "driverCom": data["title"],
            "passCom": data["title"],
            "awardPointRental": data["title"],
            "awardPointLease": data["title"],
            "awardPointRideShare": data["title"],
            "awardPointInstantRide": data["title"],
            "discountRental": data["title"],
            "discountLease": data["title"],
            "discountRideShare": data["title"],
            "discountInstantRide": data["title"],
            "update_date": datetime.datetime.now()
        }       
        try:
            dt = mongo.db.commissionDistribution.find_one()
            if dt == None:
                _insertData = mongo.db.insert_one(dataList)
            else:
                _updateOp = mongo.db.commissionDistribution.update_one(
                    {
                    },
                    {
                        "$set":
                           dataList
                    })
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