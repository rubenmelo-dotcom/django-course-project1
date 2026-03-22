from django.urls import reverse, resolve
from recipes import views
from .test_base_class import RecipeTestBase, Recipe, Category


class RecipesRecipeViewsTest(RecipeTestBase):

    def test_recipes_recipe_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipes_recipe_view_return_404_if_no_recipes_found(self):
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': 1000})
            )
        self.assertEqual(response.status_code, 404)

    def test_recipes_recipe_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse(
            'recipes:recipe', 
            kwargs={'id': 1}
            ))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipes_recipe_template_dont_load_recipe_not_published(self):
        '''Test recipe is_published False dont show'''
        # Need a recipe for this test
        recipe: Recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe', 
            kwargs={'id': recipe.pk}))

        # Check is one recipe exists
        self.assertEqual(response.status_code, 404)
    
