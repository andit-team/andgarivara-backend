from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
from pymongo import UpdateOne
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants

class GetAppSetupData(Resource):
    @staticmethod    
    @jwt_required
    def get() -> Response:
        dt = None        
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bsonO.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
            dt = mongo.db.adminAppSetupPage.find({"setupTitle" : constants.APP_SETUP_TITLE})
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

        
class UpdateAppSetupData(Resource):
    @staticmethod
    @jwt_required    
    def put() -> Response:
        dt =  request.get_json() 
        dt["setupTitle"] = constants.APP_SETUP_TITLE  
        try:
            _update = mongo.db.adminAppSetupPage.update_one(
                {
                    "setupTitle" : constants.APP_SETUP_TITLE
                },
                {
                    "$set": dt
                },
                upsert = True
            )
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