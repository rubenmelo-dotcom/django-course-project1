from django.core.exceptions import ValidationError
from .test_base_class import RecipeTestBase, Recipe
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='title',
            description='description',
            slug='recipe-slug-no-default',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='preparation_steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe
    
    # def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
    #     self.recipe.title = 'A' * 70

    #     with self.assertRaises(ValidationError):
    #         self.recipe.full_clean()
        # self.recipe.save()
    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    
    def test_recipe_preparation_steps_is_html_is_false_by_defaul(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html
        )

    def test_recipe_is_published_is_false_by_defaul(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published
        )
    
    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed,
                         msg=f'Recipe string representation must be "{needed}" '\
                         f'but "{str(self.recipe)}" was received.')