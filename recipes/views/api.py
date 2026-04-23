
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe
from django.db.models import F, Value
from django.db.models.functions import Concat
from recipes.serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from tag.models import Tag
from recipes.serializers import TagSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from recipes.permissions import IsOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 5


class RecipeAPIV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.filter(is_published=True)\
        .annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id').select_related('category', 'author')\
        .prefetch_related('tags')
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    http_method_names = ['get', 'options', 'head', 'patch', 'post', 'delete']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            queryset = queryset.filter(
                is_published=True,
                category_id=category_id,
            )

        return queryset

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()
    
    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
        serialiser = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serialiser.is_valid(raise_exception=True)
        serialiser.save()
        return Response(
            serialiser.data
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED, headers=headers
        )

# class RecipeAPIv2List(ListCreateAPIView):
#     queryset = Recipe.objects.filter(is_published=True)\
#         .annotate(
#             author_full_name=Concat(
#                 F('author__first_name'), Value(' '),
#                 F('author__last_name'), Value(' ('),
#                 F('author__username'), Value(')'),
#             )
#         ).order_by('-id').select_related('category', 'author')\
#         .prefetch_related('tags')
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIV2Pagination


# class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
#     queryset = Recipe.objects.filter(is_published=True)\
#         .annotate(
#             author_full_name=Concat(
#                 F('author__first_name'), Value(' '),
#                 F('author__last_name'), Value(' ('),
#                 F('author__username'), Value(')'),
#             )
#         ).order_by('-id').select_related('category', 'author')\
#         .prefetch_related('tags')
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIV2Pagination


    # def get_recipe(self, pk):
    #     recipe = get_object_or_404(
    #         Recipe.objects.filter(
    #             is_published=True, pk=pk
    #         ))
    #     return recipe
    
    # def get(self, request, pk):
    #     recipe = self.get_recipe(pk)
    #     serializer = RecipeSerializer(
    #         instance=recipe,
    #         many=False,
    #         context={'request': request}
    #         )
    #     return Response(serializer.data)
    
    # def patch(self, request, pk):
    #     recipe = self.get_recipe(pk)
    #     serializer = RecipeSerializer(
    #         instance=recipe,
    #         data=request.data,
    #         many=False,
    #         partial=True,
    #         context={'request': request},
    #         )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    
    # def delete(self, request, pk):
    #     recipe = self.get_recipe(pk)
    #     recipe.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(http_method_names=['get', 'post'])
# def recipe_api_list(request):
#     if request.method == 'GET':
#         recipes = Recipe.objects.filter(
#             is_published=True
#         ).annotate(
#             author_full_name=Concat(
#                 F('author__first_name'), Value(' '),
#                 F('author__last_name'), Value(' ('),
#                 F('author__username'), Value(')'),
#             )
#         ).order_by('-id').select_related('category', 'author').prefetch_related('tags')

#         serializer = RecipeSerializer(
#             instance=recipes,
#             many=True,
#             context={'request': request}
#         )
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = RecipeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED
#         )


# @api_view(['get', 'patch', 'delete'])
# def recipe_api_detail(request, pk):
#     recipe = get_object_or_404(
#         Recipe.objects.filter(
#             is_published=True, pk=pk
#         ))
#     if request.method == 'GET':
#         serializer = RecipeSerializer(
#             instance=recipe,
#             many=False,
#             context={'request': request}
#             )
#         return Response(serializer.data)
    
#     if request.method == 'PATCH':
#         serializer = RecipeSerializer(
#             instance=recipe,
#             data=request.data,
#             many=False,
#             partial=True,
#             context={'request': request},
#             )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     if request.method == 'DELETE':
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(), pk=pk)
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request}
)
    return Response(serializer.data)
