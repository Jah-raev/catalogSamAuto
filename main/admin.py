from django.contrib import admin
from .models import Cars, Brands, CarCompartments, Details, Key, Profile, DetailsInformation, DetailFiles
from django.contrib.auth.models import User
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import Group
from import_export.admin import ImportExportModelAdmin


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('name', 'dateCreate', 'dateUpdate')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('name', 'inform', 'date_create', 'date_update')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(CarCompartments)
class CarCompartmentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_create', 'date_update')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'identifier', 'id', 'compartment_id', 'brand_id', 'date_update', 'date_create')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(DetailsInformation)
class DetailsInformationAdmin(ImportExportModelAdmin):
    list_display = ('partName', 'partNumber', 'LR', 'QTY', 'detail')

    
@admin.register(DetailFiles)
class DetailFilesAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_create', 'date_update')

# @admin.register(Clients)
# class ClientsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'login', 'password', 'email', 'date_create', 'date_update')
#     fields = (('name', 'email'), ('login', 'password'), 'address', 'information')
#
#
# @admin.register(Employees)
# class EmployeesAdmin(admin.ModelAdmin):
#     list_display = ('name', 'login', 'password', 'email', 'phone', 'date_create', 'date_update')
#     fields = ('name', ('login', 'password'), ('department', 'position'), 'email', 'phone', )
#

@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'date_create', 'date_update')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','department', 'position', 'phoneNumber', 'date_update')


class UserInLine(admin.TabularInline):
    model = Group.user_set.through
    extra = 0


