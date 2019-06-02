from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields

from .models import *

# admin.site.register(Product)
# admin.site.register(Country)
# admin.site.register(Favorite)

@admin.register(Product, Country, Favorite, Searchlog)
class ViewAdmin(ImportExportModelAdmin):
    pass