from django.contrib import admin
from .models import User
# from blog_contents.models import Blog

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name','email']
admin.site.register(User,UserAdmin)
# admin.site.register(Blog)