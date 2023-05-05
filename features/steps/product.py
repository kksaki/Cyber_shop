import urllib
from urllib.parse import urljoin
from behave import given, when, then
from PIL import Image
import tempfile
from selenium.webdriver.support.ui import Select


from django.test import Client
from bigcart.models import User
from django.contrib.auth.hashers import make_password
import random
import string


with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
    im = Image.new('RGB', (100, 100))
    im.save(f.name)

@given(u'we want to add a product')
def user_on_product_newpage(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    print(base_url)
    open_url = urljoin(base_url,'/new')
    context.browser.get(open_url)


@when(u'we fill in the form')
def user_fills_in_the_form(context):
    # use print(context.browser.page_source) to aid debugging
    # only prints page source if there is an error in the step
    print(context.browser.page_source)

    productNo_IntegerField = context.browser.find_element('name', 'productNo')
    productNo_IntegerField.send_keys(7000)

    productName_TextField = context.browser.find_element('name','productName')
    print(productName_TextField)
    productName_TextField.send_keys('VeryTasty')

    category_ChoiceField = Select(context.browser.find_element_by_name('category'))
    category_ChoiceField.select_by_visible_text('seafood')
    category_ChoiceField.select_by_value('seafood')

    sub_category_TextField = context.browser.find_element('name', 'sub_category')
    sub_category_TextField.send_keys('fish')

    brand_ChoiceField = Select(context.browser.find_element_by_name('brand'))
    brand_ChoiceField.select_by_visible_text('fishman')
    brand_ChoiceField.select_by_value('fishman')

    price_FloatField = context.browser.find_element('name', 'price')
    price_FloatField.send_keys(10)

    types_ChoiceField = Select(context.browser.find_element_by_name('types'))
    types_ChoiceField.elect_by_visible_text('organic')
    types_ChoiceField.select_by_value('organic')

    rating_FloatField = context.browser.find_element('name', 'rating')
    rating_FloatField.send_keys(5)

    description_TextField = context.browser.find_element('name', 'description')
    description_TextField.send_keys('very nice')

    image_ImageField = context.browser.find_element('name', 'image')
    image_ImageField.send_keys(f.name)

    context.browser.find_element('name','submit').click()


@then(u'it succeeds')
def specific_products(context):
    assert '7000' in context.browser.page_source


@given(u'we have specific product to add')
def specific_products(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url,'/new')
    for row in context.table:
        context.browser.get(open_url)
        productNo_IntegerField = context.browser.find_element('name', 'productNo')
        productNo_IntegerField.send_keys(7000)

        productName_TextField = context.browser.find_element('name','productName')
        productName_TextField.send_keys('VeryTasty')

        category_ChoiceField = Select(context.browser.find_element_by_name('category'))
        category_ChoiceField.select_by_visible_text('seafood')
        category_ChoiceField.select_by_value('seafood')


        sub_category_TextField = context.browser.find_element('name', 'sub_category')
        sub_category_TextField.send_keys('fish')

        brand_ChoiceField = Select(context.browser.find_element_by_name('brand'))
        brand_ChoiceField.select_by_visible_text('fishman')
        brand_ChoiceField.select_by_value('fishman')

        price_FloatField = context.browser.find_element('name', 'price')
        price_FloatField.send_keys(10)

        types_ChoiceField = Select(context.browser.find_element_by_name('types'))
        types_ChoiceField.elect_by_visible_text('organic')
        types_ChoiceField.select_by_value('organic')

        rating_FloatField = context.browser.find_element('name', 'rating')
        rating_FloatField.send_keys(5)

        description_TextField = context.browser.find_element('name', 'description')
        description_TextField.send_keys('very nice')

        image_ImageField = context.browser.find_element('name', 'image')
        image_ImageField.send_keys(f.name)

        context.browser.find_element('name','submit').click()
        assert row['name'] in context.browser.page_source


@when(u'we visit the list page')
def step_impl(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url,'/details/7000')
    context.browser.get(open_url)
    print(context.browser.page_source)
    assert '7000' in context.browser.page_source


@then(u'we will find \'7000\'')
def step_impl(context):
    assert '7000' in context.browser.page_source




@given('a customer is logging in')
def step_given_a_user_is_logged_in(context):
    # Create a test user and log them in
    User.objects.filter(username='admin-test').delete()
    context.user = User.objects.create(username='admin-test', password=make_password('123456'))
    context.client = Client()  # Initialize Django test client
    response = context.client.post('/accountslogin/', {'username': 'admin-test', 'password': '123456'})
    assert response.status_code == 302

@when('the customer is accessing their cart')
def step_when_the_customer_visits_their_cart(context):
    # Access the cart page
    response = context.client.get('/cart-detail/')
    context.cart_response = response

@then('the cart should be displayed with the correct products and quantities')
def step_then_the_cart_should_be_displayed_with_the_correct_products_and_quantities(context):
    # Check the cart response
    assert context.cart_response.status_code == 200

@when('the customer is accessing their order history')
def step_when_the_customer_visits_their_order_history(context):
    # Access the order history page
    context.order_response = context.client.get('/order_list/')

@then('the order history should display the correct orders with product information')
def step_then_the_order_history_should_display_the_correct_orders_with_product_information(context):
    # Check the order history response
    assert context.order_response.status_code == 200