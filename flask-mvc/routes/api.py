from flask_restful import Api
########################## User ##########################
from controllers.users.profile.favorites import AddFavorite, DeleteFavorite, FavoriteList
from controllers.users.profile.favoritePlaces import AddFavoritePlace, DeleteFavoritePlace, FavoritePlaceList
from controllers.users.profile.userOperation import ProfileEdit, ProfileDelete, GetUserDataByToken, UpdateUserProfileImage, ResetPassword
from controllers.users.register.login import UserLogin
from controllers.users.register.signup import UserSignup
from controllers.users.register.driverSignup import DriverSignup
from controllers.users.vehicles.vehicleOp import AddVehicle, EditVehicle, DeleteVehicle, UserVehicleList, GetVehicleDataById, GetVehicleServiceHelperData
from controllers.users.vehicles.services import AddVehicleInService, GetVehicleServiceCost 
from controllers.users.vehicles.ownersOp import GetAllDriversList, GetDriverDataById, CheckIfDriverAdded 
from controllers.users.vehicles.driverOp import GetAllOwnersList, GetOwnerDataById 
from controllers.users.serviceBooking.rentalBooking import RentalBooking

########################## Admin ##########################
from controllers.admin.fuel_type.fuelTypeOperation import FuelTypeList, AddFuelType, EditFuelType, FuelTypeById
from controllers.admin.register.login import AdminLogin
from controllers.admin.register.signup import AdminSignup
from controllers.admin.appSetup.setupPage import GetAppSetupData, UpdateAppSetupData
from controllers.admin.vehicles.adminVehicleTypeOp import AddVehicleType, EditVehicleType, VehicleTypeById, DeleteVehicleType, VehicleTypeList,AddBrandWithVehicleType, EditBrandWithVehicleType, BrandWithVehicleTypeById, VehicleBrandList
from controllers.admin.users.adminUser import UserList, DeleteUser, AddUser
from controllers.admin.users.drivers import VerifyDriver, DriverList, GetFreeDriverList, GetDriverInfoById
from controllers.admin.vehicles.adminVehicleOp import AdminVehicleList, AdminVehicleStatusChange, GetVehicleData
########################## Frontend ##########################
from controllers.frontEnd.vehicleProfile import VehicleProfile
from controllers.frontEnd.homepage import GetRentalList, GetDriverList
from controllers.frontEnd.searchVehicle import SearchVehicle

########################## Locations ##########################
from controllers.frontEnd.addressByLocationDiv import GetDivisionList, GetDistrictList, GetUpazillaList,GetUnionList, GetVillageList, GetMunicipleList, GetWordList


def create_routes(api: Api):
   ########################## User.Setuppage ##########################
   api.add_resource(GetAppSetupData, '/api/admin/get_app_setup')
   # api.add_resource(AddAppSetupData, '/api/admin/add_app_setup')
   api.add_resource(UpdateAppSetupData, '/api/admin/update_app_setup')
   ########################## User.Reg ##########################
   api.add_resource(UserSignup, '/api/signup')
   api.add_resource(UserLogin, '/api/login')
   api.add_resource(DriverSignup, '/api/driver_registration')
   ########################## User.Profile ##########################
   api.add_resource(ProfileEdit, '/api/profile_update')
   api.add_resource(ProfileDelete, '/api/delete_profile')
   api.add_resource(GetUserDataByToken, '/api/user/profile_info')
   api.add_resource(UpdateUserProfileImage, '/api/user/update_profile_image')
   api.add_resource(ResetPassword, '/api/user/reset_password')
   ########################## User.vehicle ##########################
   api.add_resource(UserVehicleList, '/api/vehicle_list')
   api.add_resource(AddVehicle, '/api/add_vehicle')
   api.add_resource(GetVehicleDataById, '/api/edit_vehicle/<string:id>')
   api.add_resource(EditVehicle, '/api/update_vehicle/<string:id>')
   api.add_resource(DeleteVehicle, '/api/delete_vehicle/<string:id>')
   api.add_resource(GetVehicleServiceHelperData, '/api/get_service_helper_data/<string:id>')
   ########################## User.vehicle.service ##########################
   api.add_resource(AddVehicleInService, '/api/add_service_cost/<string:id>')
   api.add_resource(GetVehicleServiceCost, '/api/get_service_cost/<string:id>')
   ########################## User.vehicle.OwnerOp ##########################
   api.add_resource(GetAllDriversList, '/api/owner/get_all_drivers')
   api.add_resource(CheckIfDriverAdded, '/api/check_if_driver_added')
   api.add_resource(GetDriverDataById, '/api/get_driver_data/<string:id>')
   ########################## User.vehicle.DriverOp ##########################
   api.add_resource(GetAllOwnersList, '/api/driver/get_all_owners')
   api.add_resource(GetOwnerDataById, '/api/get_owner_data/<string:id>')
   ########################## User.favorite ##########################
   api.add_resource(FavoriteList, '/api/favorite_list')
   api.add_resource(AddFavorite, '/api/add_favorites/<string:id>')
   api.add_resource(DeleteFavorite, '/api/delete_favorites/<string:id>')
   ########################## User.favoritePlaces ##########################
   api.add_resource(FavoritePlaceList, '/api/user/favorite_place_list')
   api.add_resource(AddFavoritePlace, '/api/user/add_favorite_place')
   api.add_resource(DeleteFavoritePlace, '/api/user/delete_favorite_place/<string:id>')
   ########################## User.serviceBooking.Rental ##########################
   # api.add_resource(GetAllOwnersList, '/api/driver/get_all_owners')
   api.add_resource(RentalBooking, '/api/rental_booking/<string:id>')
   ########################## Admin.FuelType ##########################
   api.add_resource(FuelTypeList, '/api/fuel_type_list')
   api.add_resource(AddFuelType, '/api/admin/add_fuel_type')
   api.add_resource(FuelTypeById, '/api/admin/edit_fuel_type/<string:id>')
   api.add_resource(EditFuelType, '/api/admin/update_fuel_type')

   ########################## Admin.register ##########################
   api.add_resource(AdminLogin, '/api/admin/login')
   api.add_resource(AdminSignup, '/api/admin/signup')
   ########################## Admin.vehicle.vehicleTYpe ##########################
   api.add_resource(VehicleTypeList, '/api/vehicle_type_list')
   api.add_resource(AddVehicleType, '/api/admin/add_vehicle_type')
   api.add_resource(VehicleTypeById, '/api/admin/edit_vehicle_type/<string:id>')
   api.add_resource(EditVehicleType, '/api/admin/update_vehicle_type/<string:id>')
   api.add_resource(DeleteVehicleType, '/api/admin/delete_vehicle_type')
   ########################## Admin.vehicle.vehicleBrand ##########################
   api.add_resource(AddBrandWithVehicleType, '/api/admin/add_vehicle_brand')
   api.add_resource(BrandWithVehicleTypeById, '/api/admin/edit_vehicle_brand/<string:id>')
   api.add_resource(EditBrandWithVehicleType, '/api/admin/update_vehicle_brand')
   api.add_resource(VehicleBrandList, '/api/vehicle_brand_list/<string:id>')
   ########################## Admin.User ##########################
   api.add_resource(UserList, '/api/admin/user_list')
   ########################## Admin.Driver ##########################
   api.add_resource(VerifyDriver, '/api/admin/driver_verification/<string:id>')
   api.add_resource(GetDriverInfoById, '/api/get_driver_info/<string:id>')
   api.add_resource(DriverList, '/api/admin/driver_list/<string:status>')
   api.add_resource(GetFreeDriverList, '/api/admin/unoccupied_driver_list/<string:type>')

   # api.add_resource(DeleteUser, '/api/admin/delete_user')
   # api.add_resource(AddUser, '/api/admin/add_user')

   ########################## Admin.Vehicle ##########################
   # api.add_resource(AddVehicleAdmin, '/admin/add_vehicle')
   # api.add_resource(EditVehicleAdmin, '/admin/edit_vehicle')
   # api.add_resource(DeleteVehicleAdmin, '/admin/delete_vehicle')AdminVehicleVerifyList
   api.add_resource(AdminVehicleList, '/api/admin/vehicle_list/<string:status>')
   api.add_resource(AdminVehicleStatusChange, '/api/admin/vehicle_verification/<string:id>')
   api.add_resource(GetVehicleData, '/api/get_vehicle_data/<string:id>')
   ########################## Frontend ##########################
   api.add_resource(GetRentalList, '/api/rental_list')
   api.add_resource(GetDriverList, '/api/home_driver_list')
   api.add_resource(SearchVehicle, '/api/search_vehicle')
   api.add_resource(VehicleProfile, '/api/vehicle_details/<string:id>')
   ########################## Location ##########################
   api.add_resource(GetDivisionList, '/api/get_division')
   api.add_resource(GetDistrictList, '/api/get_district/<string:id>')
   api.add_resource(GetUpazillaList, '/api/get_upazila/<string:id>')
   api.add_resource(GetUnionList, '/api/get_union/<string:id>')
   api.add_resource(GetVillageList, '/api/get_village/<string:id>')
   api.add_resource(GetMunicipleList, '/api/get_municiple/<string:id>')
   api.add_resource(GetWordList, '/api/get_ward/<string:id>')


