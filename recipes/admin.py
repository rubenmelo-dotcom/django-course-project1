from recipes import models
from django.contrib import admin


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'author', 'title', 'category', \
        'author', 'is_published'
    list_display_links = 'id',
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps',
    list_filter = 'category', 'author', 'is_published', \
        'preparation_steps_is_html',
    list_per_page = 15
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',),
    }