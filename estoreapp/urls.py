from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

# from .views import Template,CartView, IndexView, CheckoutView, ContactView,Login,MyAccView,ProductListView,ProductDetailView,WishlishView,RegisterView,LogOutView
from .views import *
app_name = 'estoreapp'

urlpatterns = [
    path('index/',IndexView.as_view(),name='index'),
    path('cart/',CartView.as_view(),name='cart'),
    path('my-account/',MyAccView.as_view(),name='my_account'),
    path('product-detail/',ProductView.as_view(),name='product_detail'),
    path('product-list/',ProductListView.as_view(),name='product_list'),

    path('register/',RegisterView,name='register'),
    path('loginuser/',loginUser, name='login'),
    path('logout/',LogOutView.as_view(),name='logout'),

    path('product/<pk>/',ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<pk>/',add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/',remove_from_cart, name='remove-from-cart'),

    path('email/',EMAIL, name='email'),
    path('search/',SearchView.as_view(),name='search'),
    path('brand/',BrandView.as_view(),name='brand'),
    path('profile/',UserProfile.as_view(),name='profile'),
    path('update/',UpdateUserView.as_view(),name='update_profile'),
    url(r'^users/(?P<pk>\d+)/edit/$', UpdateUserView.as_view(), name="edit-user-profile") # URL use for complex url

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
