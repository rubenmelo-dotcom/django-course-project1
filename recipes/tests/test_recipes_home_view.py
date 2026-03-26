from django.urls import reverse, resolve
from recipes import views
from .test_base_class import RecipeTestBase, Recipe, Category


class RecipesHomeViewsTest(RecipeTestBase):

    def test_recipes_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipes_home_view_return_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
    
    def test_recipes_home_template_shows_no_recipe_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )

    def test_recipes_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes'][0]
        self.assertEqual(response_recipes.title, 'Recipe Title')
        # self.assertEqual(len(response_recipes), 1)
        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('Recipe Title', content)

    def test_recipes_home_template_dont_load_recipe_not_published(self):
        '''Test recipe is_published False dont show'''
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Check is one recipe exists
        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )

