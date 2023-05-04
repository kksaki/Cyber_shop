from django.test import TestCase
from bigcart.forms import SearchConditionForm,ProductForm
from bigcart.models import Product,Category,Brand,Type
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

class ProductFormTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.category = Category.objects.create(id='seafood')
        cls.brand= Brand.objects.create(id='fishman')
        cls.types = Type.objects.create(id='organic')

        image_data = b'binary image data'
        image_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')

        Product.objects.create(
            productNo=7000,
            productName='Very Tasty - cod',
            category=cls.category,
            sub_category='fish',
            brand=cls.brand,
            price=10,
            types=cls.types,
            rating=5,
            description='very nice',
            image=image_file
        )

    def test_valid_form(self):
        form = ProductForm(
            data={
                'productNo': 7000,
                'productName': 'Very Tasty - cod',
                'category': self.category.id,
                'sub_category': 'fish',
                'brand': self.brand.id,
                'price': 10,
                'types': self.types.id,
                'rating': 5,
                'description': 'very nice',
                'image': SimpleUploadedFile('test_image.jpg', b'binary image data', content_type='image/jpeg')
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        product = form.save(commit=False)
        product.created_date = timezone.now()
        product.save()


class SearchConditionFormTestCase(TestCase):

    fixtures = ['cart.json']

    def setUp(self):
        self.types = ['All'] + [t.id for t in Type.objects.all()]
        self.category = ['All'] + [c.id for c in Category.objects.all()]
        self.brand = ['All'] + [r.id for r in Brand.objects.all()]

    def test_valid_form(self):
        form = SearchConditionForm(data={
            'productName': 'Very Tasty - cod',
            'category': 'seafood',
            'type': 'organic',
            'brand': 'fishman',
            'sort_by': '-rating',
        })

        self.assertTrue(form.is_valid(), form.errors)






