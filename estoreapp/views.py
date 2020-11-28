from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View,FormView, RedirectView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import RegisterForm, LoginForm
from django.contrib.auth.models import User
from .models import Profile,ShippingAddress, Item,Order,OrderItem
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
# from estoreapp.tasks import send_email_task
from .tasks import send_email_task



def EMAIL(request):
    if request.method == "POST":
        # task = Post.objects.get(post_id=id)
        # task = Post.objects.select_related('author').get(post_id=id)
        # client_ = CustomUser.objects.get(username=self.request.user)
        # client_ = CustomUser.objects.select_related('client').get(username=self.request.user)
        print('user========',request.user)
        item = Item.objects.all()
        for stock in item:
            product_quantity = stock.quantity
            cart_stock = OrderItem.objects.all().filter(id=stock.id)
            for cart in cart_stock:
                cart_quantity = cart.quantity
                product_quantity -= cart_quantity
                stock.quantity = product_quantity
                stock.save()

        check_out_of_stock = Item.objects.filter(quantity=0)
        for i in check_out_of_stock:
            i.out_of_stock = True
            i.save()
        subject = 'new service'
        message = f' wants your  service.'
        To =['parthardeshana82@gmail.com']
        From = settings.EMAIL_HOST_USER,
        send_email_task(subject, message, From, To)
        return redirect('/my-account/')
    return render(request, 'cart.html')

def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        username=request.POST.get('username')
        print('username',username)
        if form.is_valid():
            new = form.save()
            new.set_password(new.password)
            new.save()
            filter = User.objects.filter(username=username)
            user = filter[0]
            create = Profile.objects.create(user_id=user)
            return redirect('/')
        else:
            return redirect('/register')
    return render(request, 'login.html')

# class RegisterView(CreateView):
#     form_class = RegisterForm
#     template_name = 'login.html'
#     success_url = '/temp'



def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pass')
        print(f'username={username} password={password}')
        user = authenticate(username=username, password=password)
        print("iser", user)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            print('not in  login')
            return redirect('/login')
    return render(request, 'login.html')



class ShowView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'register.html'
    context_object_name = 'show'


class BrandView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'product-list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        product = self.model.objects.all()
        print('product---', product)
        if query:
            object_list = self.model.objects.filter(item_name__icontains=query)
        else:
            object_list = self.model.objects.none()



class IndexView(LoginRequiredMixin,ListView):
    model = Item
    template_name = 'index.html'

class SearchView(LoginRequiredMixin,ListView):
    model = Item
    template_name = 'product-list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(item_name__icontains=query)
        else:
            object_list = self.model.objects.none()
        print('object_list--',object_list)
        return object_list


class ProductView(LoginRequiredMixin,ListView):
    model = Item
    template_name = "product-list.html"

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
    model = Item
    template_name = 'product-detail.html'


class ProductListView(LoginRequiredMixin,ListView):
    model = Item
    template_name = "product-list.html"


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
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("estoreapp:product", pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("estoreapp:product", pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("estoreapp:product", pk=pk)



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
            messages.info(request, "Item remove from your cart")
            return redirect("estoreapp:product", pk=pk)
        else:
            # order.items.remove(order_item)
            messages.info(request, "This Item not in your cart")
            return redirect("estoreapp:product", pk=pk)
    else:
        # add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("estoreapp:product", pk=pk)



class Template(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'index.html'
    context_object_name = 'temp'





class CheckoutView(LoginRequiredMixin,TemplateView):
    template_name = 'checkout.html'


class ContactView(LoginRequiredMixin,TemplateView):
    template_name = 'contact.html'



class Login(TemplateView):
    template_name = 'login.html'


class WishlishView(LoginRequiredMixin,TemplateView):
    template_name = 'wishlist.html'


class LogOutView(RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)