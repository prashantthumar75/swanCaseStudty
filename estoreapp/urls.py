from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

# from .views import Template,CartView, IndexView, CheckoutView, ContactView,Login,MyAccView,ProductListView,ProductDetailView,WishlishView,RegisterView,LogOutView
from .views import *
app_name = 'estoreapp'

urlpatterns = [
    path('',Template.as_view(),name='home'),
    path('cart/',CartView.as_view(),name='cart'),
    path('index/',IndexView.as_view(),name='index'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('my-account/',MyAccView.as_view(),name='my_account'),
    path('product-detail/',ProductView.as_view(),name='product_detail'),
    path('product-list/',ProductListView.as_view(),name='product_list'),
    path('wishlist/',WishlishView.as_view(),name='wishlist'),

    path('register/',RegisterView,name='register'),
    path('loginuser/',loginUser, name='login'),
    path('login/',Login.as_view(), name='logi'),
    path('logout/',LogOutView.as_view(),name='logout'),

    path('product/<pk>/',ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<pk>/',add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/',remove_from_cart, name='remove-from-cart'),

    path('email/',EMAIL, name='email'),
    path('search/',SearchView.as_view(),name='search'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
