from flask_restful import Api

from controllers.user import SignUp
from controllers.user import Login
from controllers.users.userLogin import UserLogin
from controllers.users.userSignup import UserSignup, PhoneVerification
from controllers.users.userOperation import ProfileEdit, ProfileDelete, GetAllUser
from controllers.users.vehicles import UserVehicleList, AddVehicle, EditVehicle, DeleteVehicle


def create_routes(api: Api):

    # Customer
    api.add_resource(UserSignup, '/user/signup')
    api.add_resource(UserLogin, '/user/login')
    api.add_resource(PhoneVerification, '/user/phone_verification')
    #api.add_resource(UserHome, '/user/after_login_home')

    api.add_resource(ProfileEdit, '/user/profile_edit')
    api.add_resource(ProfileDelete, '/user/delete_profile')
    api.add_resource(GetAllUser, '/user/show_users')

    api.add_resource(UserVehicleList, '/user/vehicle_list')
    api.add_resource(AddVehicle, '/user/add_vehicle')
    api.add_resource(EditVehicle, '/user/edit_vehicle')
    api.add_resource(DeleteVehicle, '/user/delete_vehicle')

    #api.add_resource(Favorites, '/user/favorites')
    #api.add_resource(Favorites, '/user/favorites')

    # Admin
    #api.add_resource(Login, '/admin/login')
    #api.add_resource(Dashboard, '/admin/dashboard')
    #api.add_resource(VehicleTypes, '/admin/vehicle_type')
    #api.add_resource(UserList, '/admin/user_list')
    #api.add_resource(VehicleList, '/admin/vehicle_list')
    #api.add_resource(VehicleAdd, '/admin/vehicle_add')

    # Frontend
    #api.add_resource(HomePage, '/and_gari_vara/list_homepage')
    #api.add_resource(SearchResult, '/and_gari_vara/search_result_page')
    #api.add_resource(VehicleProfile, '/and_gari_vara/vehicle_profile')
