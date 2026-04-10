from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination
import os

PER_PAGE = 3


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id,
        is_published=True)
    return render(
        request,
        'recipes/pages/recipe-view.html',
        context={
            'recipe': recipe,
            'is_detail_page': True,
        }
    )


