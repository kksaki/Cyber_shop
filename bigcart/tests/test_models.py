from django.test import Client, TestCase
from ..models import Product, Category,Brand, Type, Cart,Customer, Coupon
from django.core.files.images import ImageFile
from io import BytesIO


class ProductModelTest(TestCase):

    fixtures = ['cart.json']

    # 1
    def test_product(self):
        product = Product.objects.get(productNo=7000)
        self.assertEqual(product.price, 10)
        products = Product.objects.all()
        self.assertEqual(products.count(), 1)

    # 2
    def test_category(self):
        category = Category.objects.get(pk="seafood")
        self.assertEqual(category.id, "seafood")
        categorys =Category.objects.all()
        self.assertEqual(categorys.count(), 1)

    # 3
    def test_region(self):
        brand = Brand.objects.get(pk="fishman")
        self.assertEqual(brand.id, "fishman")
        brands = Brand.objects.all()
        self.assertEqual(brands.count(), 1)

    # 4
    def test_type(self):
        type_p = Type.objects.get(pk="organic")
        self.assertEqual(type_p.id, "organic")
        types = Type.objects.all()
        self.assertEqual(types.count(), 1)

class CartModelTest(TestCase):

    fixtures = ['cart.json']

    # 5
    def test_cart(self):
        cart = Cart.objects.get(product__productNo=7000)
        self.assertEqual(cart.quantity, 2)
        carts = Cart.objects.all()
        self.assertEqual(carts.count(), 1)


class CustomerModelTest(TestCase):

    fixtures = ['cart.json']

    # 6
    def test_customer(self):
        customer = Customer.objects.get(user__id=1)
        self.assertEqual(customer.email, "kk@outlook.com")
        customers = Customer.objects.all()
        self.assertEqual(customers.count(), 1)


class CouponModelTest(TestCase):

    fixtures = ['cart.json']

    # 7
    def test_coupon(self):
        coupon = Coupon.objects.get(pk="999")
        self.assertEqual(coupon.discount, 80)
        coupons = Coupon.objects.all()
        self.assertEqual(coupons.count(), 1)

class ImageTest(TestCase):

    fixtures = ['cart.json']

    # 8
    def test_product_image(self):
        product = Product.objects.get(productNo=7000)
        if product.image:
            # Load the image data from the fixture
            with open(product.image.path, 'rb') as f:
                fixture_image_data = f.read()

            # Create an in-memory file from the image data
            fixture_image_file = BytesIO(fixture_image_data)

            # Create an ImageFile object from the in-memory file
            fixture_image = ImageFile(fixture_image_file)

            # Compare the fixture image to the product image
            self.assertEqual(product.image.read(), fixture_image.read())










