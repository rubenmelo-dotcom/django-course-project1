from django.http import Http404, JsonResponse
from django.contrib import messages
from recipes.models import Recipe
from django.views.generic import ListView, DetailView
from utils.pagination import make_pagination
from django.shortcuts import render
from django.db.models import Q
from django.forms.models import model_to_dict
from tag.models import Tag


PER_PAGE = 9


def theory(request, *args, **kwargs):
    return render(
        request,
        'recipes/pages/theory.html',
    )


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
        query_set = query_set.select_related('author', 'category')
        query_set = query_set.prefetch_related('tags')
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


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()
        
        return JsonResponse(
                list(recipes_list),
                safe=False,
        )
    

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


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(tags__slug=self.kwargs.get('slug', ''))

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
            ).first()
        
        if not page_title:
            page_title = 'No recipes found'
        
        page_title = f'{page_title} - Tag | '

        context.update(
            {
                'page_title': page_title,
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
    

class RecipeDetailViewApi(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = recipe_dict['cover'].url
        else:
            recipe_dict['cover'] = ''
        
        del recipe_dict['is_published']
        
        return JsonResponse(
            recipe_dict,
            safe=False,
        )

