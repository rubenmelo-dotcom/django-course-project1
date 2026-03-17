from recipes import models
from django.contrib import admin


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...