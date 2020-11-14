from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import get_jwt_identity, jwt_required
import constants.constantValue as constants
from pymongo import UpdateOne

class DriverSignup(Resource):
    @staticmethod
    @jwt_required
    def put() -> Response:
        msg = None
        error = None
        data = request.get_json()
        userId = bsonO.ObjectId(get_jwt_identity())
        print(get_jwt_identity())
        driverInfo = data["driverInfo"]
        try:            
            bulkAction = mongo.db.userRegister.bulk_write(
                [
                    UpdateOne(
                    {
                        "_id":userId,
                        "del_status" : False
                    },
                    {
                        "$addToSet": {
                            "role":constants.ROLL_DRIVER,
                            "reference":data["reference"]
                        }
                    }
                    ),
                    UpdateOne(
                        {
                            "_id":userId
                        },
                        {
                            "$set": {
                                "drivers" : driverInfo,
                                "driverStatus": constants.STATUS_PENDING,
                                "default_contact_number":data["default_contact_number"]
                            }
                        }
                    )
                ]
            )
            msg = "Registered Successfully"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data" : json.loads(dumps(data))
        })
