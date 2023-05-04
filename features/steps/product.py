import urllib
from urllib.parse import urljoin
from behave import given, when, then
from PIL import Image
import tempfile
from selenium.webdriver.support.ui import Select


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
