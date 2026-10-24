from django.contrib import admin
from myapp.models import CategoryDb, ProductDb

# Register your models here.

admin.site.register(CategoryDb)
admin.site.register(ProductDb)
