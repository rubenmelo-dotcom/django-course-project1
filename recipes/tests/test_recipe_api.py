from django.urls import reverse
from recipes.tests.test_base_class import RecipeMixin
from rest_framework import test
from unittest.mock import patch


class RecipeAPIv2TestMixin(RecipeMixin):
    def get_recipe_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url
    
    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_list_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response
    
    def get_auth_data(self, username='user', password='pass'):
        userdata = {
            'username': username,
            'password': password,
        }
        user = self.make_author(
            username=userdata.get('username'),
            password=userdata.get('password')
        )
        response = self.client.post(
            reverse('recipes:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
            }

    def get_recipe_raw_data(self):
        return {
            'title': 'This is the title',
            'description': 'This is the description',
            'preparation_time': 2,
            'preparation_time_unit': 'Minutes',
            'servings': 1,
            'servings_unit': 'Person',
            'preparation_steps': 'This is the preparation steps',
        }


class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(
            response.status_code,
            200
        )
    
    @patch('recipes.views.api.RecipeAPIV2Pagination.page_size', new=3)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 3
        self.make_recipe_in_batch(qtd=6)
        response = self.get_recipe_api_list()
        qtd_of_loaded_recipes = len(response.data.get('results'))
        self.assertEqual(
            wanted_number_of_recipes,
            qtd_of_loaded_recipes
        )

    @patch('recipes.views.api.RecipeAPIV2Pagination.page_size', new=3)
    def test_recipe_api_list_pagination_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 3
        self.make_recipe_in_batch(qtd=6)
        response = self.client.get(reverse('recipes:recipes-api-list') + '?page=2')
        qtd_of_loaded_recipes = len(response.data.get('results'))
        self.assertEqual(
            wanted_number_of_recipes,
            qtd_of_loaded_recipes
        )

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipe = self.make_recipe_in_batch(qtd=1)
        recipe_not_published = recipe[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            0
        )

    @patch('recipes.views.api.RecipeAPIV2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')
        recipes = self.make_recipe_in_batch(qtd=10)

        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()
        
        recipes[0].category = category_not_wanted
        recipes[0].save()
        
        api_url = reverse('recipes:recipes-api-list') + \
            f'?category_id={category_wanted.id}'
        response = self.get_recipe_api_list(reverse_result=api_url)

        self.assertEqual(
            len(response.data.get('results')),
            9
        )
        
    def test_recipe_api_list_user_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )
    
    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        access_token = auth_data.get('jwr_access_token')
        response = self.client.post(
            path=self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        self.assertEqual(
            response.status_code,
            201
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        jwt_access_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()

        wanted_new_title = f'The new title updated by {author.username}'

        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.pk,)),
            data={
                'title': wanted_new_title,
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            response.data.get('title'),
            wanted_new_title
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe_owned_by_another_user(self): # noqa
        recipe = self.make_recipe(author_data={'username': 'user', 'password': 'pass'})
        access_data = self.get_auth_data(username='test_patch')
        jwt_access_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.save()

        new_title = f'The new title updated by {author.username}'

        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.pk,)),
            data={
                'title': new_title,
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )

        self.assertEqual(
            response.status_code,
            403
        )


