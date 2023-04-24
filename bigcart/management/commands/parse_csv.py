import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from bigcart.models import Product, Category, Type, Brand, Customer, User
from django.apps import apps
from django.contrib.auth.models import User

apps.clear_cache()

def convert_blank(value):
    return None if value == '' else value

class Command(BaseCommand):
    help = 'Load data from csv'


    def handle(self, *args, **options):
        # Delete data from tables to avoid duplicate values when the file is rerun

        Product.objects.all().delete()
        Category.objects.all().delete()
        Type.objects.all().delete()
        Brand.objects.all().delete()


        print("table dropped successfully")

        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        with open(str(base_dir) + '/data/BigBasket Products.csv', newline='', encoding='latin-1') as product:
            reader = csv.reader(product, delimiter=",")
            next(reader)

            products = []
            categories = set()
            types = set()
            brands = set()


            for row in reader:
                category = row[2]
                type = row[7]
                brand = row[4]

                categories.add(Category(id=category))
                types.add(Type(id=type))
                brands.add(Brand(id=brand))

                product = Product(
                    productNo = (row[0]),
                    productName = (row[1]),
                    category_id = category,
                    sub_category = convert_blank(row[3]),
                    brand_id = brand,
                    price = convert_blank(row[5]),
                    types_id = type,
                    rating = convert_blank(row[8]),
                    description = convert_blank(row[9]),
                )
                products.append(product)

            Category.objects.bulk_create(categories)
            Type.objects.bulk_create(types)
            Brand.objects.bulk_create(brands)
            Product.objects.bulk_create(products)

            print("data parsed successfully")