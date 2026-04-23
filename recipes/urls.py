from django.urls import path, include
from recipes import views
from rest_framework.routers import SimpleRouter

from recipes.views.api import RecipeAPIV2ViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    prefix='recipes/api/v2',
    viewset=views.RecipeAPIV2ViewSet,
)


urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(),
         name='search'
         ),
    path('recipes/tag/<slug:slug>/', views.RecipeListViewTag.as_view(),
         name='tag'
         ),
    path('recipes/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(),
         name='category'
         ),
    path('recipes/<int:pk>/',
         views.RecipeDetailView.as_view(),
         name='recipe'),
    path('recipes/api/v1/',
         views.RecipeListViewHomeApi.as_view(),
         name='recipe_api_v1'),
    path('recipes/api/v1/<int:pk>/',
         views.RecipeDetailViewApi.as_view(),
         name='recipe_detail_api_v1'),
    path('recipes/theory/',
         views.theory,
         name='recipe_theory'),
    path('recipes/api/v2/tag/<int:pk>/',
         views.tag_api_detail,
         name='recipe_api_v2_tag'),
    path('recipes/api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('recipes/api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('recipes/api/token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
    path('', include(recipe_api_v2_router.urls)),
]
