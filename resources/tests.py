from django.test import TestCase, Client
from django.urls import reverse
import os

# Create your tests here.


class TestResourcesApp(TestCase):
    """
    This testcase tests all the functions in the resources app
    """

    def setUp(self):
        """
        This method runs before the execution of each test case.
        """
        self.client = Client()


    def test_upload_resource_method_returns_correct_output(self):
        with open('test_file.pdf', "rb") as fp:
            response = self.client.post(
                '/resources/upload', {"file": fp, "category": 'DevOps', "fname": 'test_file.pdf'})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["name"], "test_file.pdf")
        self.assertEquals(
            response.json()["path_display"], "/DevOps/test_file.pdf")


    def test_upload_resource_method_category_is_valid(self):
        with open('test_file.pdf', "rb") as fp:

            with self.assertRaises(Exception) as context:
                self.client.post(
                    '/resources/upload', {"file": fp, "category": 'Marketing', "fname": 'test_file.pdf'})
            self.assertEqual('Category is invalid.', str(context.exception))


    def test_get_all_resources_method(self):
        response = self.client.get('/resources/all')
        self.assertEquals(response.status_code, 200)
        self.assertIn("resources", response.json())


    def test_search_by_category_method(self):
        response = self.client.post(
            '/resources/search/category', {"category": 'DevOps', "query": 'test'})
        self.assertEquals(response.status_code, 200)
        self.assertIn("resources", response.json())


    def test_search_by_category_method_category_is_valid(self):

        with self.assertRaises(Exception) as context:
            self.client.post('/resources/search/category',
                             {"category": 'Marketing', "query": 'test'})
        self.assertEqual('Category is invalid.', str(context.exception))


    def test_search_by_query_method(self):
        response = self.client.post(
            '/resources/search/query', {"query": 'test'})
        self.assertEquals(response.status_code, 200)
        self.assertIn("resources", response.json())
