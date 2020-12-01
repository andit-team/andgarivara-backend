from re import error
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants
        
class GetDivisionList(Resource):
    @staticmethod
    def get() -> Response:
        msg = ""
        data = None
        error = False
        try:
            data = mongo.db.divisions.find()
            print(data.count())
            msg = "SUCCESSFULL"
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class GetDistrictList(Resource):
    @staticmethod
    def get(id) -> Response:
        msg = ""
        data = []
        error = False
        try:
            data = mongo.db.districts.find({"division_id" : id})
            print(data.count())
            msg = "SUCCESSFULL"
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })
class GetUpazillaList(Resource):
    @staticmethod
    def get(id) -> Response:
        msg = ""
        data = []
        error = False
        try:
            data = mongo.db.upazillas.find({"district_id" : id})
            print(data.count())
            msg = "SUCCESSFULL"
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })

class GetUnionList(Resource):
    @staticmethod
    def get(id) -> Response:
        msg = ""
        data = []
        error = False
        try:
            data = mongo.db.unions.find({"upazila_id" : id})
            print(data.count())
            msg = "SUCCESSFULL"
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })
class GetVillageList(Resource):
    @staticmethod
    def get(id) -> Response:
        msg = ""
        data = []
        error = False
        try:
            data = mongo.db.villages.find({"union_id" : id})
            print(data.count())
            msg = "SUCCESSFULL"
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })
class GetMunicipleList(Resource):
    @staticmethod
    def get(id) -> Response:
        msg = ""
        data = []
        error = False
        try:
            data = mongo.db.municipals.find({"district_id" : id})
            print(data.count())
            msg = "SUCCESSFULL"
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })

class GetWordList(Resource):
    @staticmethod
    def get(id) -> Response:
        msg = ""
        data = []
        error = False
        try:
            data = mongo.db.words.find({"municipal_id" : id})
            print(data.count())
            msg = "SUCCESSFULL"
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })