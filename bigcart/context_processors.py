from .cart import Cart
from .forms import SearchConditionForm

def cart(request):
    return {'cart': Cart(request)}

def search_form(request):
    return {'search_form': SearchConditionForm(request)}