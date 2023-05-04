from django import forms
from .models import Type, Brand, Category, Product, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    """ Form used for search conditions in /new /edit page """

    class Meta:
        model = Product
        fields = '__all__'

    # called on validation of the form
    def clean(self):
        # run the standard clean method first
        cleaned_data = super(ProductForm, self).clean()

        for k, v in cleaned_data.items():
            if v == '':
                cleaned_data[k] = None
            if str(v).isdecimal():
                cleaned_data[k] = int(v)

        return cleaned_data

    # For '*' in required field
    required_css_class = 'required'

    # Get options from database
    categories = Category.objects.all()
    types = Type.objects.all()
    brands = Brand.objects.all()



    productNo = forms.IntegerField(
        label="ProductNo",
        widget=forms.widgets.NumberInput(attrs={'class': 'form-control col-sm-5'})
    )
    productName = forms.CharField(
        required=False,
        label="ProductName",
        widget=forms.widgets.TextInput(attrs={'class': 'form-control col-sm-5'})
    )
    category = forms.ModelChoiceField(
        required=False,
        label="Category",
        queryset=Category.objects.all(),
        widget=forms.widgets.Select(attrs={'class': 'form-control form-inline'})
    )
    brand = forms.ModelChoiceField(
        required=False,
        label="Brand",
        queryset=Brand.objects.all(),
        widget=forms.widgets.Select(attrs={'class': 'form-control form-inline'})
    )
    price = forms.FloatField(
        required=False,
        label="Price",
        widget=forms.widgets.NumberInput(attrs={'class': 'form-control col-sm-5'})
    )
    types = forms.ModelChoiceField(
        required=False,
        label="Type",
        queryset=Type.objects.all(),
        widget=forms.widgets.Select(attrs={'class': 'form-control form-inline'})
    )
    rating = forms.FloatField(
        required=False,
        label="Rating",
        widget=forms.widgets.NumberInput(attrs={'class': 'form-control col-sm-5'})
    )
    description = forms.CharField(
        required=False,
        label="Description",
        widget=forms.widgets.TextInput(attrs={'class': 'form-control col-sm-5'})
    )
    sub_category = forms.CharField(
        required=False,
        label="Sub Category",
        widget=forms.widgets.TextInput(attrs={'class': 'form-control col-sm-5'})
    )
    image = forms.ImageField(
        required=False,
        label="Image",
        widget=forms.widgets.FileInput(attrs={'class': 'form-control col-sm-5'})
    )

class SearchConditionForm(forms.Form):
    """ Form used for search conditions in /search page """
    categories = Category.objects.all()
    types = Type.objects.all()
    brands = Brand.objects.all()

    productName = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(attrs={'class': 'form-control col-sm-5','placeholder': 'e.g egg, fish'})
    )
    category = forms.fields.ChoiceField(
        required=False,
        choices=[('', 'All')] + [(item.id, item.id) for item in categories],
        widget=forms.widgets.Select(attrs={'class': 'form-control col-sm-5'})
    )
    type = forms.fields.ChoiceField(
        required=False,
        choices=[('', 'All')] + [(item.id, item.id) for item in types],
        widget=forms.widgets.Select(attrs={'class': 'form-control col-sm-5'})
    )
    brand = forms.fields.ChoiceField(
        required=False,
        choices=[('', 'All')] + [(item.id, item.id) for item in brands],
        widget=forms.widgets.Select(attrs={'class': 'form-control form-inline'})
    )
    sort_by = forms.fields.ChoiceField(
        required=False,
        choices=[
            ('productNo', ' productNo - Asc'),
            ('-productNo', ' productNo - Desc'),
            ('rating', ' rating - Asc'),
            ('-rating', ' rating - Desc'),
            ('price', ' price - Asc'),
            ('-price', ' price - Desc'),
        ],
        # widget=forms.widgets.Select(attrs={'class': 'form-control form-inline'})
        widget=forms.widgets.HiddenInput(),
    )
    Sort_By_Rating1= forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'type': 'button', 'value': 'Ascend↑', 'onclick': "setSortBy('rating'); document.getElementById('search').submit();"}))

    Sort_By_Rating2 = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'type': 'button', 'value': 'Descend↓', 'onclick': "setSortBy('-rating'); document.getElementById('search').submit();"}))

    Sort_By_Price1 = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'type': 'button', 'value': 'Ascend↑', 'onclick': "setSortBy('price'); document.getElementById('search').submit();"}))

    Sort_By_Price2 = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'type': 'button', 'value': 'Descend↓', 'onclick': "setSortBy('-price'); document.getElementById('search').submit();"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices += [(c.id, c.id) for c in Category.objects.all()]
        self.fields['type'].choices += [(t.id, t.id) for t in Type.objects.all()]
        self.fields['brand'].choices += [(b.id, b.id) for b in Brand.objects.all()]



class SearchProduct(forms.Form):
    """ Form used for search conditions in /search page """
    categories = Category.objects.all()
    types = Type.objects.all()
    brands = Brand.objects.all()

    productName = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(attrs={'class': 'form-control col-sm-5','placeholder': 'e.g egg, fish'})
    )
    category = forms.fields.ChoiceField(
        required=False,
        choices=[('', 'All')] + [(item.id, item.id) for item in categories],
        widget=forms.widgets.Select(attrs={'class': 'form-control col-sm-5'})
    )
    type = forms.fields.ChoiceField(
        required=False,
        choices=[('', 'All')] + [(item.id, item.id) for item in types],
        widget=forms.widgets.Select(attrs={'class': 'form-control col-sm-5'})
    )
    brand = forms.fields.ChoiceField(
        required=False,
        choices=[('', 'All')] + [(item.id, item.id) for item in brands],
        widget=forms.widgets.Select(attrs={'class': 'form-control form-inline'})
    )



class SignUpForm(UserCreationForm):
    """ Form used signup user in /signup page """
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',)


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']

class CouponApplyForm(forms.Form):
    code = forms.CharField()