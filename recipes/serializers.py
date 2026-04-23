from attr import fields
from django.forms import SlugField
from rest_framework import serializers
from authors.validators import AuthorRecipeValidator
from recipes.models import Category, Recipe
from django.contrib.auth.models import User
from tag.models import Tag
from collections import defaultdict
from attr import attr


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'name', 'slug',


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = 'id', 'title', 'description', 'author', \
            'category', 'tags', 'public', 'preparation', \
            'tag_objects', 'tag_links', \
            'preparation_time', 'preparation_time_unit', 'servings', \
            'servings_unit', \
            'preparation_steps', 'cover',
        
    public = serializers.BooleanField(
        source='is_published',
        read_only=True)
    preparation = serializers.SerializerMethodField(
        read_only=True
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True,
        source='tags',
        read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipe_api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings
       
        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time
            
        super_validade = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )
        return super_validade
    
