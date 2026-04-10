from django.http import Http404
from django.contrib import messages
from recipes.models import Recipe
from django.views.generic import ListView, DetailView
from utils.pagination import make_pagination
import os
from django.db.models import Q

PER_PAGE = os.environ.get('PER_PAGE', 2)


class RecipeListViewBase(ListView):
    
    model = Recipe
    context_object_name = 'recipes'
    ordering = '-id',
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True,
        ).order_by('-id')
        return query_set
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE,
        )
        
        context.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
             }
        )
        return context
        

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'
    paginate_by = 9


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True,
        ).order_by('-id')

        if not query_set:
            raise Http404()
        
        return query_set
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {
                'title': f'{context.get(
                    "recipes")[0].category.name} - Category | ',
             }
        )
        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()
        
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            ),     
            is_published=True,
            ).order_by('-id')
        
        if not query_set:
            raise Http404()

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')
        context.update(
            {
                'page_title': f'Search for "{search_term}" | ',
                'search_term': search_term,
                'aditional_url_query': f'&q={search_term}',
             }
        )
        return context
    

class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)
        context.update({
            'is_detail_page': True,
        })

        return context
