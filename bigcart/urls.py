from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('list', views.product_list, name='list'),
    path('details/<slug:productNo>',views.details, name='details'),
    path('search',views.search, name='search'),
    path('management',views.chart, name='management'),
    path('edit/<slug:productNo>', views.product_edit, name='product_edit'),
    path('delete/<slug:productNo>', views.product_delete, name='product_delete'),
    path('new', views.product_new, name='product_new'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.log_out, name='log_out'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<slug:username>', views.customer_detail, name='customer_detail'),
    path('accounts', include('django.contrib.auth.urls')),

    path('cart/add/<slug:productNo>>/', views.cart_add, name='cart_add'),
    path('cart/remove/<slug:productNo>', views.cart_remove, name='cart_remove'),
    path('cart-detail/',views.cart_detail,name='cart_detail'),
    path('purchase/', views.purchase, name ='purchase'),
    path('order_list/',views.order_list, name='order_list'),

    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),

    path('apply/', views.coupon_apply, name='apply'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


