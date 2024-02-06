from django.contrib import admin
from .models import Blog,Comments,Reply,Categories,SubCategory

# Register your models here.
admin.site.register(Blog)
admin.site.register(Comments)
admin.site.register(Reply)
admin.site.register(Categories)
admin.site.register(SubCategory)

