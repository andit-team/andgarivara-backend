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
        perDayRent = float(data["perDayRent"])
        perHourRentIncludeFuel = float(data["perHourRentIncludeFuel"])
        perHourRentExcludedFuel = float(data["perHourRentExcludedFuel"])
        fuelCost = float(data["fuelCost"])
        fuelCostUpDown = float(data["fuelCostUpDown"])
        totalDistance = float(data["totalDistance"])        
        voucher = float(data["voucher"])
        voucherType = data["voucherType"]
        totalFare = data["totalFare"]
        grandTotalFare = float(data["grandTotalFare"])
        paymentType = data["paymentType"]        
        passengerId = bson.ObjectId(get_jwt_identity())
        driverData = mongo.db.vehicles.find_one({"_id" : bson.ObjectId(id)},{"driver" : 1})
        driverId = bson.ObjectId(driverData["driver"])
        totalFareCalculated = 0
        grandtoTalFareCalculated = 0
        
        if journeyDurationUnit == constants.UNIT_DAY:
            if fuelPackage == constants.INCLUDED_FUEL_COST:
                totalFareCalculated = perDayRent*journeyDuration + (totalDistance*fuelCostUpDown)
            else:
                totalFareCalculated = perDayRent*journeyDuration
        else:
            if fuelPackage == constants.INCLUDED_FUEL_COST:
                totalFareCalculated = journeyDuration*perHourRentIncludeFuel
            else:
                totalFareCalculated = journeyDuration*perHourRentExcludedFuel
                
                
        # if fuelPackage == constants.INCLUDED_FUEL_COST:            
        #     if journeyDurationUnit == constants.UNIT_DAY:
        #         totalFareCalculated = perDayRent*journeyDuration + (totalDistance*fuelCostUpDown)
        #     else:
        #         totalFareCalculated = 0           
        # else:
        #     if journeyDurationUnit == constants.UNIT_DAY:
        #         totalFareCalculated = perDayRent*journeyDuration
        #     else:
        #         totalFareCalculated = 0
        
        
        if voucherType == constants.VOUCHER_TYPE_TK and voucher != 0:
            grandtoTalFareCalculated = totalFareCalculated - voucher
        elif voucherType == constants.VOUCHER_TYPE_PERCENTAGE and voucher != 0:
            grandtoTalFareCalculated = totalFareCalculated - totalFareCalculated *(voucher/100)
        else:
            grandtoTalFareCalculated = totalFareCalculated    
        if totalFareCalculated != totalFare or grandtoTalFareCalculated !=grandTotalFare:
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
            "perDayRent" : perDayRent,
            "fuelTypeTitle" : data["fuelTypeTitle"],
            "fuelCost" : fuelCost,
            "fuelCostUpDown" : fuelCostUpDown,
            "voucher" : voucher,
            "voucherType" : voucherType,
            "totalFare" : totalFare,
            "grandTotalFare" : grandTotalFare,
            "paymentType" : paymentType,            
            "from" : data["from"],
            "to" : data["to"],
            "totalDistance" : totalDistance,
            "vaehicleId" : bson.ObjectId(id),
            "driverId" : driverId,
            "passengerId" : passengerId,
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
    
    