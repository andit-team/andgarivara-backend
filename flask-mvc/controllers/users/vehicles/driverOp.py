from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from pymongo import GEO2D, UpdateOne, MongoClient, GEOSPHERE 
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants


class GetAllOwnersList(Resource):
    @staticmethod
    @jwt_required
    def get() ->Response:
        userId = bsonO.ObjectId(get_jwt_identity())
        vehicleData = None
        msg = ""
        error = None
        dt = None
        try:            
            vehicleData = mongo.db.userRegister.find_one({ "_id" : userId}, {"owners" : 1})
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vehicleData))
        })
        
class GetOwnerDataById(Resource):
    @staticmethod
    @jwt_required
    def get(id) ->Response:
        vehicleData = None
        msg = ""
        error = None
        try:
            vehicleData = mongo.db.userRegister.find_one({"_id" : bsonO.ObjectId(id)})
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vehicleData))
        })
