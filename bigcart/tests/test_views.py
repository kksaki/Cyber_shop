from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from django.core.management import call_command


class BigcartViewsTest(TestCase):

    fixtures = ['cart.json']

    # test the home page
    # 9
    def test_home(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, "Start shopping now!")

    # 10
    def test_views_home_use_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'home.html')

    # test the product page
    # 11
    def test_produt_list(self):
        client = Client()
        response = client.get('/list')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1")
        self.assertContains(response, "All Product")


    # 12
    def test_views_list_use_correct_template(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'product/product_table.html')


    # test the search page
    # 13
    def test_search_page(self):
        client = Client()
        response = client.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sort by rating1:")

    # 14
    def test_views_all_use_correct_template(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'product/search.html')

    # 15
    def test_product_detail(self):
        client = Client()
        response = client.get('/details/7000')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail of Product No.7000")
        self.assertContains(response, "Very Tasty - cod")
        self.assertContains(response, "fish")


    # test the home page
    # 16
    def test_cart(self):
        client = Client()
        response = client.get('/cart-detail/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Cart")

    # 17
    def test_views_cart_use_correct_template(self):
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'order/basket.html')




