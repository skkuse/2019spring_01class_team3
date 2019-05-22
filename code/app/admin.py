from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields

from .models import *

admin.site.register(Product)
admin.site.register(Country)
admin.site.register(Favorite)

# class BaseModelResource(resources.ModelResource):
#         related_module = fields.Field(
#                                 column_name='related_module',
#                                 attribute='related_module',
#                                 widget=ForeignKeyWidget(Module,'module_name'))
#         question_group = fields.Field(
#                                 column_name='question_group',
#                                 attribute='question_group',
#                                 widget=ForeignKeyWidget(Membership,'member_type'))
#         class Meta:
#               abstract = True
#               skip_unchanged = True
#               report_skipped = False
#               fields = ()
#               export_order = ()

# class ProductResource(BaseModelResource):
#     def save_instance(self, instance, using_transactions=True, dry_run=False):
#         name = self.__class__
#         try:
#             super(name, self).save_instance(
#                 instance, using_transactions, dry_run)
#         except IntegrityError:
#             pass

#     class Meta:
#         model = Product
#         fields = ('pid',
#         'pcode',
#         'brand',
#         'pname',
#         'category',
#         'price',
#         'url',
#         'cid',
#                   )
#         export_order = fields


# @admin.register(Product)
# class ProductAdmin(ImportExportModelAdmin):
#     resource_class = ProductResource
#     list_display = [
#         'pid',
#         'pcode',
#         'brand',
#         'pname',
#         'category',
#         'price',
#         'url',
#         'cid'
#     ]


