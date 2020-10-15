from flask_restful import Api
from controllers.users.userLogin import UserLogin
from controllers.users.userSignup import UserSignup
from controllers.users.userOperation import ProfileEdit, ProfileDelete
from controllers.users.vehicles import UserVehicleList, AddVehicle, EditVehicle, DeleteVehicle
from controllers.users.favorites import FavoriteList, AddFavorite, DeleteFavorite
from controllers.admin.adminLogin import AdminLogin
from controllers.admin.adminSignup import AdminSignup
from controllers.admin.adminVehicleTypeOp import AddVehicleType, EditVehicleType, DeleteVehicleType, VehicleTypeList
from controllers.admin.adminUser import UserList, DeleteUser, AddUser
from controllers.admin.adminVehicleOp import AdminVehicleList, AddVehicleAdmin, EditVehicleAdmin, DeleteVehicleAdmin
from controllers.admin.adminCityOp import CityList, AddCity, EditCity, DeleteCity
from controllers.admin.adminAreaOp import AreaList, AddArea, EditArea, DeleteArea
from controllers.frontEnd.vehicleProfile import VehicleProfile
from controllers.frontEnd.homepage import HomePage
from controllers.frontEnd.searchVehicle import SearchVehicle


def create_routes(api: Api):

   ########################## User ##########################
    api.add_resource(UserSignup, '/user/signup')
    api.add_resource(UserLogin, '/user/login')

    api.add_resource(ProfileEdit, '/user/profile_edit')
    api.add_resource(ProfileDelete, '/user/delete_profile')

    api.add_resource(UserVehicleList, '/user/vehicle_list')
    api.add_resource(AddVehicle, '/user/add_vehicle')
    api.add_resource(EditVehicle, '/user/edit_vehicle')
    api.add_resource(DeleteVehicle, '/user/delete_vehicle')

    api.add_resource(FavoriteList, '/user/favorite_list')
    api.add_resource(AddFavorite, '/user/add_favorites')
    api.add_resource(DeleteFavorite, '/user/delete_favorites')

    ########################## Admin ##########################
    api.add_resource(AdminLogin, '/admin/login')
    api.add_resource(AdminSignup, '/admin/signup')

    api.add_resource(VehicleTypeList, '/vehicle_type_list')
    api.add_resource(AddVehicleType, '/admin/add_vehicle_type')
    api.add_resource(EditVehicleType, '/admin/edit_vehicle_type')
    api.add_resource(DeleteVehicleType, '/admin/delete_vehicle_type')

    api.add_resource(UserList, '/admin/user_list')
    api.add_resource(DeleteUser, '/admin/delete_user')
    api.add_resource(AddUser, '/admin/add_user')

    api.add_resource(AdminVehicleList, '/admin/vehicle_list')
    api.add_resource(AddVehicleAdmin, '/admin/add_vehicle')
    api.add_resource(EditVehicleAdmin, '/admin/edit_vehicle')
    api.add_resource(DeleteVehicleAdmin, '/admin/delete_vehicle')

    api.add_resource(CityList, '/city_list')
    api.add_resource(AddCity, '/admin/add_city')
    api.add_resource(EditCity, '/admin/edit_city')
    api.add_resource(DeleteCity, '/admin/delete_city')

    api.add_resource(AreaList, '/area_list')
    api.add_resource(AddArea, '/admin/add_area')
    api.add_resource(EditArea, '/admin/edit_area')
    api.add_resource(DeleteArea, '/admin/delete_area')

    ########################## Frontend ##########################
    api.add_resource(HomePage, '/and_gari_vara/list_homepage')
    api.add_resource(SearchVehicle, '/and_gari_vara/search_result_page')
    api.add_resource(VehicleProfile, '/and_gari_vara/vehicle_profile')
