from collections import defaultdict
from pickletools import optimize
from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings
from PIL import Image, ImageOps


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/cover/%Y/%m/%d',
                              blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
        )
    tags = models.ManyToManyField(Tag, blank=True, default='')
    
    def get_absolute_url(self):
        return reverse("recipes:recipe", args=(self.pk,))

    @staticmethod
    def resize_image(image, target_width=633, target_height=475):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)

        # ImageOps.fit corta a imagem para preencher exatamente as dimensões
        # mantendo o aspecto original e centralizando o corte.
        # O método centering=(0.5, 0.5) foca exatamente no meio.
        new_image = ImageOps.fit(
            image_pillow,
            (target_width, target_height), 
            method=Image.LANCZOS, 
            centering=(0.5, 0.5)
        )

        new_image.save(image_full_path, quality=90, optimize=True)
        image_pillow.close()

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug
        
        saved = super().save(*args, **kwargs)
        
        if self.cover:
            try:
                self.resize_image(self.cover, 633)
            except FileNotFoundError:
                ...

        return saved

    def __str__(self):
        return self.title
    
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipe with the same title'
                )
        
        if error_messages:
            raise ValidationError(error_messages)
    
