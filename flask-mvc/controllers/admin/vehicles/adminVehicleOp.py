from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants


class AddVehicleAdmin(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        flag = insertData(data)
        return flag


def insertData(data):
    userId = bsonO.ObjectId(data["user_id"])
    err_msg = None
    dt = {
        "user_id": userId,
        "title": data["title"],
        "vehicle_type": bsonO.ObjectId(data["vehicle_type"]),
        "description": data["description"],
        "country": data["country"],
        "city": bsonO.ObjectId(data["city"]),
        "area": bsonO.ObjectId(data["area"]),
        "car_location": data["car_location"],
        "total_seat": data["total_seat"],
        "min_price_per_day": data["min_price_per_day"],
        "cover_img": data["cover_img"],
        "brand": data["brand"],
        "model": data["model"],
        "year_of_manufacture": data["year_of_manufacture"],
        "color": data["color"],
        "ac": data["ac"],
        "vehicle_imgs": data["vehicle_imgs"],
        "del_status": False,
        "create_date": datetime.datetime.now()
    }
    try:
        ins = mongo.db.vehicles.insert(dt)
        msg = "SUCCESS"
        error = False
    except Exception as ex:
        msg = "FAILED"
        error = True
        err_msg = ex
        dt = None
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg": str(err_msg),
        "data": json.loads(dumps(dt))
    })


class AdminVehicleListv(Resource):
    @staticmethod
    def get() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.vehicles.aggregate(
                [
                    {
                        "$lookup": {
                            "from": "vehicle_types",
                            "localField": "vehicle_type",
                            "foreignField": "_id",
                            "as": "vehicle_type_details"
                        }
                    }
                ])
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = "FAILED"
            error = True
            err_msg = ex
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })


class DeleteVehicleAdmin(Resource):
    @staticmethod
    def delete() -> Response:
        data = request.get_json()
        err_msg = None
        try:
            update_ = mongo.db.vehicles.update(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set": {
                        "del_status": True,
                        "del_resone": "Deleted By Admin",
                        "del_date": datetime.datetime.now()
                    }
                }
            )
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = "FAILED"
            error = True
            err_msg = ex
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class AdminVehicleList(Resource):
    @staticmethod
    @jwt_required
    def get(status) -> Response:
        msg = ""
        vehicleList = []
        i = None
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bsonO.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
            vehicleList = mongo.db.vehicles.find({"activeStatus": status, "del_status": False})
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vehicleList))
        })


class AdminVehicleStatusChange(Resource):
    @staticmethod
    @jwt_required
    def put(id) -> Response:
        data = request.get_json()
        dataSet = None
        driverId = None
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bsonO.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
            if data["activeStatus"] == constants.STATUS_REJECTED:
                dataSet = {
                    "activeStatus": constants.STATUS_REJECTED,
                    "comment": data["comment"],
                    "status_change_date": datetime.datetime.now()
                }
                _updateVehicle = vehicleStatusUpdate(dataSet, id)

            else:
                if data["refType"] == constants.REFFERENCE_TYPE_ADMIN:
                    driverId = bsonO.ObjectId(data["driverId"])
                else:
                    driverOfV = mongo.db.vehicles.find_one({"del_status": False, "_id": bsonO.ObjectId(id)},
                                                           {"_id": 0, "driver": 1})
                    driverId = bsonO.ObjectId(driverOfV["driver"])
                dataSet = {
                    "activeStatus": constants.STATUS_VERIFIED,
                    "driver": driverId,
                    "status_change_date": datetime.datetime.now()
                }
                _updateVehicle = vehicleStatusUpdate(dataSet, id)
                _updateDriver = mongo.db.userRegister.update_one(
                    {
                        "del_status": False,
                        "_id": driverId
                    },
                    {
                        "$set": {
                            "driverOccupied": True,
                            "driverStatus": constants.STATUS_VERIFIED,
                            "status_change_date": datetime.datetime.now()
                        }
                    }
                )

            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


def vehicleStatusUpdate(dataSet, id):
    update_ = mongo.db.vehicles.update_one(
        {
            "del_status": False,
            "_id": bsonO.ObjectId(id)
        },
        {
            "$set": dataSet
        }
    )


class GetVehicleData(Resource):
    @staticmethod
    @jwt_required
    def get(id) -> Response:
        msg = ""
        try:
            # adminCount = mongo.db.adminRegister.find({"_id": bsonO.ObjectId(get_jwt_identity())}).count()
            # if adminCount == 0:
            #     return jsonify({
            #         "msg": "Your Are not Authenticate Admin",
            #         "error": True,
            #         "data": None
            #     })
            vehicleData = mongo.db.vehicles.find_one({"_id": bsonO.ObjectId(id), "del_status": False})
            if vehicleData["refType"] == constants.REFFERENCE_TYPE_OWNER:
                allDetails = mongo.db.userRegister.find_one({
                    "_id": bsonO.ObjectId(vehicleData["userId"]),
                    "drivers": {
                        "$elemMatch": {
                            "_id": bsonO.ObjectId(vehicleData["driver"])
                        }
                    }

                }, {"_id": 0, "drivers.$": 1, "first_name": 1, "last_name": 1, "phone_no": 1, "address": 1})
                vehicleData["driverDetails"] = allDetails["drivers"]
                ownerDetails = {
                    "name": allDetails["first_name"] + " " + allDetails["last_name"],
                    "contact": allDetails["phone_no"],
                    "address": allDetails["address"],
                }
                vehicleData["ownerDetails"] = [ownerDetails]
            elif vehicleData["refType"] == constants.REFFERENCE_TYPE_DRIVER:
                allDetails = mongo.db.userRegister.find_one({
                    "_id": bsonO.ObjectId(vehicleData["userId"]),
                    "owners": {
                        "$elemMatch": {
                            "vehicleId": bsonO.ObjectId(id)
                        }
                    }

                }, {"_id": 0, "owners.$": 1, "drivers": 1})
                vehicleData["ownerDetails"] = allDetails["owners"]
                vehicleData["driverDetails"] = [allDetails["drivers"]]
            else:
                if "driver" in vehicleData:
                    driverDetails = mongo.db.userRegister.find_one({
                        "_id": bsonO.ObjectId(vehicleData["driver"]),

                    },
                        {
                            "_id": 0, "drivers": 1
                        })
                    vehicleData["driverDetails"] = [driverDetails["drivers"]]
                else:
                    vehicleData["driverDetails"] = []
                allDetails = mongo.db.userRegister.find_one({
                    "_id": bsonO.ObjectId(vehicleData["userId"]),

                },
                    {"_id": 0, "first_name": 1, "last_name": 1, "phone_no": 1, "address": 1})
                ownerDetails = {
                    "name": allDetails["first_name"] + " " + allDetails["last_name"],
                    "contact": allDetails["phone_no"],
                    "address": allDetails["address"],
                }
                vehicleData["ownerDetails"] = [ownerDetails]
            # vehicleDataList.append(i)
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
