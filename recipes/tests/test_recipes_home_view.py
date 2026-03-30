from django.urls import reverse, resolve
from recipes import views
from .test_base_class import RecipeTestBase
from unittest.mock import patch


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
        response_recipes = response.context['recipes']
        self.assertEqual(response_recipes[0].title, 'Recipe Title')
        self.assertEqual(len(response_recipes), 1)
        
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

    @patch('recipes.views.PER_PAGE', new=9)
    def test_recipes_home_pagination_show_the_qty_correct_of_objects(self):
        CURRENT_PAGE = 1
        TOTAL_PAGES = 3
        for n in range(21):
            self.make_recipe(
                slug=f'recipe-{n}',
                author_data={'username': f'username{n}'})
        response = self.client.get(reverse('recipes:home'))
        page_obj = response.context['recipes']
        self.assertEqual(page_obj.number, CURRENT_PAGE)
        self.assertEqual(page_obj.paginator.num_pages, TOTAL_PAGES)
        self.assertEqual(len(page_obj.object_list), 9)
        
    @patch('recipes.views.PER_PAGE', new=3)
    def test_invalid_page_query_uses_page_one(self):
        for n in range(8):
            self.make_recipe(
                slug=f'recipe-{n}',
                author_data={'username': f'username{n}'})
        
        response = self.client.get(reverse('recipes:home') + '?page=1A')
        current_page = response.context['recipes'].number
        self.assertEqual(current_page, 1)

        response = self.client.get(reverse('recipes:home') + '?page=2')
        current_page = response.context['recipes'].number
        self.assertEqual(current_page, 2)

        response = self.client.get(reverse('recipes:home') + '?page=3')
        current_page = response.context['recipes'].number
        self.assertEqual(current_page, 3)


