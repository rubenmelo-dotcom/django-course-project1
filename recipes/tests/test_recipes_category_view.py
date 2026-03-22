from django.urls import reverse, resolve
from recipes import views
from .test_base_class import RecipeTestBase, Recipe, Category


class RecipesCategoryViewsTest(RecipeTestBase):

    def test_recipes_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipes_category_view_return_404_if_no_recipes_found(self):
        response = self.client.get(reverse(
            'recipes:category', kwargs={'category_id': 1000})
            )
        self.assertEqual(response.status_code, 404)

    def test_recipes_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipes_category_template_dont_load_recipe_not_published(self):
        '''Test recipe is_published False dont show'''
        # Need a recipe for this test
        recipe: Recipe = self.make_recipe(is_published=False)
        id_ = recipe.category.pk

        response = self.client.get(reverse(
            'recipes:category', 
            kwargs={'category_id': id_}))

        # Check is one recipe exists
        self.assertEqual(response.status_code, 404)

