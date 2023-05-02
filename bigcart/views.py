from django.shortcuts import render,get_object_or_404, redirect
from .models import Product, OrderItem, Order
from django.core.paginator import Paginator
from .forms import ProductForm, SearchConditionForm, SignUpForm, CartAddProductForm, OrderCreateForm
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .cart import Cart
from django.urls import reverse
from .tasks import order_created
from .models import Coupon
from .forms import CouponApplyForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def is_superuser(user):
    return user.is_superuser

def base(request):
    form2 = SearchConditionForm()
    return render(request, 'base.html',{'form2': form2})

def home(request):
    form2 = SearchConditionForm()
    return render(request, 'home.html',{'form2': form2})

def product_list(request):
    form2 = SearchConditionForm()
    product_list = Product.objects.all()
    product_list = Product.objects.order_by('productNo')
    paginator = Paginator(product_list, 20) # 每页展示10条数据
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/list.html', {'page_obj': page_obj, 'cnt': len(product_list),'form2': form2})

def details(request, productNo):
    form2 = SearchConditionForm()
    product = get_object_or_404(Product, productNo=productNo)
    cart_product_form = CartAddProductForm()
    return render(request, 'product/product_details.html', {'product': product, 'cart_product_form': cart_product_form,'form2': form2})

@user_passes_test(lambda u: u.is_superuser)
def management(request):
    form2 = SearchConditionForm()
    return render(request, 'management/management.html',{'form': form2})




def product_new(request):
    form2 = SearchConditionForm()
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES,)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('details', productNo=product.productNo)
    else:
        form = ProductForm()
    return render(request, 'product/product_edit.html', {'form': form,'form2': form2})


def product_edit(request, productNo):
    form2 = SearchConditionForm()
    product = get_object_or_404(Product, productNo=productNo)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            product = form.save()
            product.created_date = timezone.now()
            product.save()
            return redirect('details', productNo=product.productNo)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_edit.html', {'form': form, 'product': product, 'form2':form2})


def product_delete(_request, productNo):
    form2 = SearchConditionForm()
    product = get_object_or_404(Product, productNo=productNo)
    product.delete()
    return redirect('list')


def chart(request):
    form2 = SearchConditionForm()
    category_rows = Product.objects.values('category').annotate(count=Count('productNo')).order_by('-count')
    return render(request, 'management/management.html',
                  {'form2':form2,'category_rows': {'label': [row["category"] for row in category_rows],
                                 'data': [row["count"] for row in category_rows]},
                   })

# def product_list(request):
#     product_list = Product.objects.all()
#     product_list = Product.objects.order_by('productNo')
#     paginator = Paginator(product_list, 20) # 每页展示10条数据
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'product/list.html', {'page_obj': page_obj, 'cnt': len(product_list)})





def search(request):
    products = Product.objects.all()
    productName = ''
    category = ''
    d_type = ''
    brand = ''
    sort_by = "productNo"
    page = ''

    if request.method == 'GET':  # check if request method is POST
        # Get values from POST data
        page = request.GET.get('page', 1)
        if "productName" in request.GET:
            productName = request.GET["productName"]
        if "category" in request.GET:
            category = request.GET["category"]
        if "type" in request.GET:
            d_type = request.GET["type"]
        if "brand" in request.GET:
            brand = request.GET["brand"]
        if "sort_by" in request.GET:
            sort_by = request.GET["sort_by"]

        # Initialise form values
        form2 = SearchConditionForm(initial={
            'productName': productName,
            'category': category,
            'type': d_type,
            'brand': brand,
            'sort_by': sort_by,
        })

        # Create WHERE clause from query strings
        where = []
        if productName != '':
            where.append(Q(productName__contains=productName))
        if category != '':
            where.append(Q(category=category))
        if d_type != '':
            where.append(Q(types_id=d_type))
        if brand != '':
            where.append(Q(brand_id=brand))

        if sort_by != '':
            sort_by = sort_by

        # Do not show results in first access (without any conditions)
        if len(request.GET) > 0:
            products = Product.objects.all().filter(*where).order_by(sort_by)

    else:  # if request method is not GET, show all products
        form2 = SearchConditionForm()

    paginator = Paginator(products, 40)  # Show 20 products per page
    page_number = request.GET.get('page',1)
    products = paginator.get_page(page_number)

    return render(request, 'product/search.html', {'products': products, 'cnt': len(products), 'form2': form2})



def signup(request):
    form2 = SearchConditionForm()
    form = SignUpForm(request.POST)
    errors = []

    if request.method == "POST":
        errors = form.errors

    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.customer.first_name = form.cleaned_data.get('first_name')
        user.customer.last_name = form.cleaned_data.get('last_name')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')

    return render(request, 'registration/signup.html',
                  {'form': form, 'password_helper': form.fields["password1"].help_text, 'errors': errors, 'form2':form2})




@login_required
def user_list(request):
    form2 = SearchConditionForm()
    user = request.user
    if user.is_authenticated & user.is_staff:
        users = User.objects.all()
        return render(request, 'management/user_list.html', {'users' : users, 'form2':form2})
    else:
        return redirect('login')

def log_out(request):
    form2 = SearchConditionForm()
    logout(request)
    return render(request, 'registration/log_out.html',{'form2':form2})



@login_required
def customer_detail(request, username):
    form2 = SearchConditionForm()
    user = get_object_or_404(User, username=username)
    return render(request, 'customer_detail.html', {'user' : user,'form2':form2})

@login_required
def user_detail(request, username):
    form2 = SearchConditionForm()
    user = get_object_or_404(User, username=username)
    return render(request, 'management/customer_detail.html', {'user' : user,'form2':form2})


@require_POST
def cart_add(request, productNo):
    cart = Cart(request)
    product = get_object_or_404(Product, productNo=productNo)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    return redirect('cart_detail')

@require_POST
def cart_remove(request, productNo):
    cart = Cart(request)
    product = get_object_or_404(Product, productNo=productNo)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    form2 = SearchConditionForm()
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                          initial={'quantity': item['quantity'],
                          'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'order/basket.html', {'cart': cart,
                   'coupon_apply_form': coupon_apply_form,'form2':form2})




def purchase(request):
    form2 = SearchConditionForm()
    if request.user.is_authenticated:
        user = request.user
        cart = Cart(request)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                customer = request.user.customer
                order.customer = customer
                order.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            price=item['price'],
                                            quantity=item['quantity']
                                            )
                # clear the cart
                cart.clear()

                # launch asynchronous task
                order_created.delay(order.id)
                # set the order in the session
                request.session['order_id'] = order.id
                # redirect for payment
                return redirect(reverse('process'))
        else:
            form = OrderCreateForm()
        return render(request,
                    'order/purchase.html',
                    {'cart': cart, 'form': form, 'form2':form2})
    else:
        return redirect('login')

def order_list(request):
    form2 = SearchConditionForm()
    if request.user.is_authenticated:
        user = request.user
        customer = request.user.id
        orders = Order.objects.filter(customer=customer)
        return render(request, 'order/order_list.html', {'orders' : orders,'form2':form2})
    else:
        return redirect('login')

def all_order_list(request):
    form2 = SearchConditionForm()
    if request.user.is_authenticated:
        orders = Order.objects.all()
        return render(request, 'management/all_order_list.html', {'orders' : orders, 'form2':form2})
    else:
        return redirect('login')

def order_detail(request, id):
    form2 = SearchConditionForm()
    order = get_object_or_404(Order, id=id)
    order_items = OrderItem.objects.filter(order_id=order.id)
    return render(request, 'management/order_detail.html', {'order': order,'order_items':order_items,'form2':form2})


import braintree
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order

def payment_process(request):
    form2 = SearchConditionForm()
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('done')
        else:
            return redirect('canceled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token,'from2':form2})

def payment_done(request):
    form2 = SearchConditionForm()
    return render(request, 'payment/done.html',{'form2':form2})

def payment_canceled(request):
    form2 = SearchConditionForm()
    return render(request, 'payment/canceled.html',{'form2':form2})

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart_detail')