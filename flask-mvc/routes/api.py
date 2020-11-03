from flask_restful import Api
########################## User ##########################
from controllers.users.profile.favorites import AddFavorite, DeleteFavorite, FavoriteList
from controllers.users.profile.userOperation import ProfileEdit, ProfileDelete
from controllers.users.register.login import UserLogin
from controllers.users.register.signup import UserSignup
from controllers.users.vehicles.vehicleOp import AddVehicle, GetVehicleTypeDataField, EditVehicle, DeleteVehicle, UserVehicleList

########################## Admin ##########################
from controllers.admin.fuel_type.fuelTypeOperation import FuelTypeList, AddFuelType, EditFuelType
from controllers.admin.location.adminAreaOp import AreaList, AddArea, EditArea, DeleteArea
from controllers.admin.location.adminCityOp import CityList, AddCity, EditCity, DeleteCity
from controllers.admin.register.login import AdminLogin
from controllers.admin.register.signup import AdminSignup
from controllers.admin.vehicles.adminVehicleTypeOp import AddVehicleType, EditVehicleType, DeleteVehicleType, VehicleTypeList,AddBrandWithVehicleType, EditBrandWithVehicleType, VehicleBrandList
from controllers.admin.users.adminUser import UserList, DeleteUser, AddUser
from controllers.admin.vehicles.adminVehicleOp import AdminVehicleList, AddVehicleAdmin, EditVehicleAdmin, DeleteVehicleAdmin
########################## Frontend ##########################
from controllers.frontEnd.vehicleProfile import VehicleProfile
from controllers.frontEnd.homepage import HomePage
from controllers.frontEnd.searchVehicle import SearchVehicle

def create_routes(api: Api):
   ########################## User ##########################
    api.add_resource(UserSignup, '/api/signup')
    api.add_resource(UserLogin, '/api/login')
    api.add_resource(ProfileEdit, '/api/profile_edit')
    api.add_resource(ProfileDelete, '/api/delete_profile')
    api.add_resource(UserVehicleList, '/api/vehicle_list')
    api.add_resource(GetVehicleTypeDataField, '/api/vehicle_type_field')
    api.add_resource(AddVehicle, '/api/add_vehicle')
    api.add_resource(EditVehicle, '/api/edit_vehicle')
    api.add_resource(DeleteVehicle, '/api/delete_vehicle')
    api.add_resource(FavoriteList, '/api/favorite_list')
    api.add_resource(AddFavorite, '/api/add_favorites')
    api.add_resource(DeleteFavorite, '/api/delete_favorites')
    ########################## Admin.FuelType ##########################
    api.add_resource(FuelTypeList, '/api/fuel_type_list')
    api.add_resource(AddFuelType, '/api/admin/add_fuel_type')
    api.add_resource(EditFuelType, '/api/admin/edit_fuel_type')
    
    ########################## Admin.register ##########################
    api.add_resource(AdminLogin, '/api/admin/login')
    api.add_resource(AdminSignup, '/api/admin/signup')
    ########################## Admin.vehicle.vehicleTYpe ##########################
    api.add_resource(VehicleTypeList, '/api/vehicle_type_list')
    api.add_resource(AddVehicleType, '/api/admin/add_vehicle_type')
    api.add_resource(EditVehicleType, '/api/admin/edit_vehicle_type')
    api.add_resource(DeleteVehicleType, '/api/admin/delete_vehicle_type')
    api.add_resource(AddBrandWithVehicleType, '/api/admin/add_vehicle_brand')
    api.add_resource(EditBrandWithVehicleType, '/api/admin/edit_vehicle_brand')
    api.add_resource(VehicleBrandList, '/api/vehicle_brand_list')
    api.add_resource(UserList, '/api/admin/user_list')
    # api.add_resource(DeleteUser, '/admin/delete_user')
    # api.add_resource(AddUser, '/admin/add_user')
    # api.add_resource(AdminVehicleList, '/admin/vehicle_list')
    # api.add_resource(AddVehicleAdmin, '/admin/add_vehicle')
    # api.add_resource(EditVehicleAdmin, '/admin/edit_vehicle')
    # api.add_resource(DeleteVehicleAdmin, '/admin/delete_vehicle')
    ########################## Frontend ##########################
    api.add_resource(HomePage, '/api/and_gari_vara/list_homepage')
    api.add_resource(SearchVehicle, '/api/and_gari_vara/search_result_page')
    api.add_resource(VehicleProfile, '/api/and_gari_vara/vehicle_profile')
