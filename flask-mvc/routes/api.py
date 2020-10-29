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
    api.add_resource(UserSignup, '/signup')
    api.add_resource(UserLogin, '/login')
    api.add_resource(ProfileEdit, '/profile_edit')
    api.add_resource(ProfileDelete, '/delete_profile')
    api.add_resource(UserVehicleList, '/vehicle_list')
    api.add_resource(GetVehicleTypeDataField, '/vehicle_type_field')
    api.add_resource(AddVehicle, '/add_vehicle')
    api.add_resource(EditVehicle, '/edit_vehicle')
    api.add_resource(DeleteVehicle, '/delete_vehicle')
    api.add_resource(FavoriteList, '/favorite_list')
    api.add_resource(AddFavorite, '/add_favorites')
    api.add_resource(DeleteFavorite, '/delete_favorites')
    ########################## Admin.FuelType ##########################
    api.add_resource(FuelTypeList, '/fuel_type_list')
    api.add_resource(AddFuelType, '/admin/add_fuel_type')
    api.add_resource(EditFuelType, '/admin/edit_fuel_type')
    ########################## Admin.Location.city ##########################
    api.add_resource(CityList, '/city_list')
    api.add_resource(AddCity, '/admin/add_city')
    api.add_resource(EditCity, '/admin/edit_city')
    api.add_resource(DeleteCity, '/admin/delete_city')
    ########################## Admin.Location.area ##########################
    api.add_resource(AreaList, '/area_list')
    api.add_resource(AddArea, '/admin/add_area')
    api.add_resource(EditArea, '/admin/edit_area')
    api.add_resource(DeleteArea, '/admin/delete_area')
    ########################## Admin.register ##########################
    api.add_resource(AdminLogin, '/admin/login')
    api.add_resource(AdminSignup, '/admin/signup')
    ########################## Admin.vehicle.vehicleTYpe ##########################
    api.add_resource(VehicleTypeList, '/vehicle_type_list')
    api.add_resource(AddVehicleType, '/admin/add_vehicle_type')
    api.add_resource(EditVehicleType, '/admin/edit_vehicle_type')
    api.add_resource(DeleteVehicleType, '/admin/delete_vehicle_type')
    api.add_resource(AddBrandWithVehicleType, '/admin/add_vehicle_brand')
    api.add_resource(EditBrandWithVehicleType, '/admin/edit_vehicle_brand')
    api.add_resource(VehicleBrandList, '/vehicle_brand_list')
    api.add_resource(UserList, '/admin/user_list')
    # api.add_resource(DeleteUser, '/admin/delete_user')
    # api.add_resource(AddUser, '/admin/add_user')
    # api.add_resource(AdminVehicleList, '/admin/vehicle_list')
    # api.add_resource(AddVehicleAdmin, '/admin/add_vehicle')
    # api.add_resource(EditVehicleAdmin, '/admin/edit_vehicle')
    # api.add_resource(DeleteVehicleAdmin, '/admin/delete_vehicle')
    ########################## Frontend ##########################
    api.add_resource(HomePage, '/and_gari_vara/list_homepage')
    api.add_resource(SearchVehicle, '/and_gari_vara/search_result_page')
    api.add_resource(VehicleProfile, '/and_gari_vara/vehicle_profile')
