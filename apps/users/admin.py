from django.contrib import admin
from apps.users import models as UserModels

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username","uuid","role","profilePic")

admin.site.register(UserModels.User, UserAdmin)


