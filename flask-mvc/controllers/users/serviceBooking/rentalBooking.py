from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants

class RentalBooking(Resource):
    @staticmethod
    @jwt_required
    def post(id) -> Response:
        data = request.get_json()
        serviceId = "AGV-R-" + str("{0:0=8d}".format(mongo.db.serviceBooking.find({"serviceType" : constants.SERVICE_RENTAL}).count() + 1))
        journeyDuration = int(data["journeyDuration"])
        journeyDurationUnit = data["journeyDurationUnit"]
        fuelPackage = data["fuelPackage"]
        driverId = bson.ObjectId(data["driver"])
        totalFareCalculated = 0
        grandtoTalFareCalculated = 0
        unitRate = 0
        
        if journeyDurationUnit == constants.UNIT_DAY:
            if fuelPackage == constants.INCLUDED_FUEL_COST:
                if journeyDuration > 1:
                    unitRate = float(data["perDayBodyRentNightStay"])
                    totalFareCalculated = float(data["perDayBodyRentNightStay"])*journeyDuration + (float(data["totalDistance"]) *float(data["fuelCostUpDown"]))
                else:
                    unitRate = float(data["perDayBodyRent"])
                    totalFareCalculated = float(data["perDayBodyRent"])*journeyDuration + (float(data["totalDistance"]) *float(data["fuelCostUpDown"]))
            else:
                if journeyDuration > 1:
                    unitRate = float(data["perDayBodyRentNightStay"])
                    totalFareCalculated = float(data["perDayBodyRentNightStay"])*journeyDuration
                else:
                    unitRate = float(data["perDayBodyRent"])
                    totalFareCalculated = float(data["perDayBodyRent"])*journeyDuration
        else:
            if fuelPackage == constants.INCLUDED_FUEL_COST:
                unitRate = float(data["perHourRentIncludeFuel"])
                totalFareCalculated = journeyDuration*float(data["perHourRentIncludeFuel"])
            else:
                unitRate = float(data["perHourRentExcludedFuel"])
                totalFareCalculated = journeyDuration* float(data["perHourRentExcludedFuel"])
          
        if data["voucherType"] == constants.VOUCHER_TYPE_TK and float(data["voucher"]) != 0:
            grandtoTalFareCalculated = totalFareCalculated - float(data["voucher"])
        elif data["voucherType"] == constants.VOUCHER_TYPE_PERCENTAGE and float(data["voucher"]) != 0:
            grandtoTalFareCalculated = totalFareCalculated - totalFareCalculated *(float(data["voucher"])/100)
        else:
            grandtoTalFareCalculated = totalFareCalculated    
        if totalFareCalculated != float(data["totalFare"]) or grandtoTalFareCalculated != float(data["grandTotalFare"]):
            print(grandtoTalFareCalculated)
            return jsonify({
            "msg": "Calculation is not correct!!!",
            "error": True
        })                
                
        bookingData = {
            "serviceType" : constants.SERVICE_RENTAL,
            "serviceId" : serviceId,
            "pickupDate" : data["pickupDate"],
            "pickupTime" : data["pickupTime"],
            "journeyDuration" : journeyDuration,
            "journeyDurationUnit" : journeyDurationUnit,
            "fuelPackage" : fuelPackage,
            "unitRate" : unitRate,
            "fuelTypeTitle" : data["fuelTypeTitle"],
            "fuelCost" : data["fuelCost"],
            "fuelCostUpDown" : data["fuelCostUpDown"],
            "voucher" : data["voucher"],
            "voucherType" : data["voucherType"],
            "totalFare" : data["totalFare"],
            "grandTotalFare" : data["grandTotalFare"],
            "paymentType" : data["paymentType"],            
            "from" : data["from"],
            "to" : data["to"],
            "totalDistance" : data["totalDistance"],
            "vaehicleId" : bson.ObjectId(id),
            "driverId" : driverId,
            "passengerId" : bson.ObjectId(get_jwt_identity()),
            "bookingDate" : datetime.datetime.now(),
            "status" : constants.STATUS_PENDING,            
        }
        try:
            _insert = mongo.db.serviceBooking.insert_one(bookingData)
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
    
    