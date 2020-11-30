from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import RedirectView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from .form import RegisterForm, ShippingAddressFrom
from .models import Profile, Item,Order,OrderItem, ShippingAddress
from .tasks import send_email_task
from .form import ProfileFrom, LoginForm


class UserProfile(LoginRequiredMixin,TemplateView):
    model = Profile
    form_class = ProfileFrom
    template_name = 'profile.html'

    def get_context_data(self, *args,**kwargs):
        context = super(UserProfile,self).get_context_data(*args, **kwargs)
        user = Profile.objects.all().filter(user_id=self.request.user)
        context["userprofile"] = user

        return context


class UpdateUserView(UpdateView):
    model = Profile
    form_class = ProfileFrom
    template_name = "my-account.html"
    success_url = '/index/'


def EMAIL(request):
    if request.method == "POST":
        item = Item.objects.all()
        for stock in item:
            product_quantity = stock.quantity
            cart_stock = OrderItem.objects.all().filter(id=stock.id)
            for cart in cart_stock:
                cart_quantity = cart.quantity
                product_quantity -= cart_quantity
                stock.quantity = product_quantity
                stock.save()

        check_out_of_stock = Item.objects.filter(quantity__lt=0)
        for i in check_out_of_stock:
            i.out_of_stock = True
            i.save()
        send_email_task(request.user.id)
        return redirect('/profile/')
    return render(request, 'cart.html')


def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        username = request.POST.get('username')

        if form.is_valid():
            new = form.save()
            new.set_password(new.password)
            new.save()
            filter = User.objects.filter(username=username)
            user = filter[0]
            create = Profile.objects.create(user_id=user)
            return redirect('/loginuser/')
        else:
            return redirect('/register/')
    return render(request, 'login.html')


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pass')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('/index/')
        else:
            return redirect('/loginuser/')
    return render(request, 'login.html')


class ShowView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'register.html'
    context_object_name = 'show'


class BrandView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'product-list.html'


    def get_context_data(self, **kwargs):
        context = super(BrandView, self).get_context_data(**kwargs)
        object_list = self.model.objects.filter(brand='AD')
        total_product = 0
        i = 0
        for product in object_list:
            i += 1
            total_product = i

        context['add_total'] = total_product

        list_fm = self.model.objects.filter(brand='FM')
        total_fm = 0
        i = 0
        for product in list_fm:
            i += 1
            total_fm = i
        context['fm_total'] = total_fm

        list_px = self.model.objects.filter(brand='PX')
        total_px = 0
        i = 0
        for product in list_px:
            i += 1
            total_px = i
        context['px_total'] = total_px

        list_se = self.model.objects.filter(brand='SE')
        total_se = 0
        i = 0
        for product in list_se:
            i += 1
            total_px = i
        context['se_total'] = total_se
        return context


class IndexView(LoginRequiredMixin,ListView):
    model = Item
    template_name = 'index.html'

    def get_queryset(self):
        object_list = self.model.objects.all().order_by('-quantity')
        return object_list


class SearchView(LoginRequiredMixin,ListView):
    model = Item
    template_name = 'product-list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(item_name__icontains=query)
        else:
            object_list = self.model.objects.none()
        return object_list


class ProductView(LoginRequiredMixin,ListView):
    model = Item
    template_name = "product-list.html"

    def get_queryset(self):
        object_list = self.model.objects.all().order_by('-quantity')
        return object_list


class CartView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class MyAccView(LoginRequiredMixin,ListView):
    model = OrderItem
    template_name = 'my-account.html'
    context_object_name = 'acc'


class ProductDetailView(LoginRequiredMixin,DetailView):
    model = OrderItem
    template_name = 'product-detail.html'


class ProductListView(LoginRequiredMixin,ListView):
    model = Item
    template_name = "product-list.html"

    def get_queryset(self):
        object_list = self.model.objects.all().order_by('-quantity')
        return object_list


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            item.description = order_item.quantity * item.price
            item.save()
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("estoreapp:product", pk=order_item.id)
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("estoreapp:product", pk=order_item.id)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("estoreapp:product", pk=order_item.id)


def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()
            return redirect("estoreapp:product", pk=order_item.id)
        else:
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            return redirect("estoreapp:product", pk=order_item.id)
    else:
        return redirect("estoreapp:product", pk=pk)


class Template(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'index.html'
    context_object_name = 'temp'


class LogOutView(RedirectView):
    url = '/loginuser/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)