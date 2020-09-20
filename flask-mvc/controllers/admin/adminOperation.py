
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo


class AddVehicleType(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        if data["type_title"] is None:
            return jsonify(message="failed")
        typeID = mongo.db.vehicleTypes.insert(data)
        return jsonify(message="OK")
