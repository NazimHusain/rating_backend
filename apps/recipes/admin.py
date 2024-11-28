from django.contrib import admin
from apps.recipes import models as RecipreModels

class AdminRecipe(admin.ModelAdmin):
    list_display = ("id","seller","name","description","image")

admin.site.register(RecipreModels.Recipe, AdminRecipe)

class AdminRating(admin.ModelAdmin):
    list_display = ("id","customer","recipe","rating")

admin.site.register(RecipreModels.Rating, AdminRating)


