# from django.shortcuts import render/
from django.http import HttpResponseRedirect
# from django.template import loader
from django.shortcuts import render, redirect
from . models import Product, Cart, Item
from .forms import UserRegistrationForm, FilterForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
global_filter = None
def index(request):
    if global_filter == None:
        all_products = Product.objects.all()
    else:
        all_products = Product.objects.filter(category = global_filter)
    try:
        cart = Cart.objects.get(user=request.user)
    except:
        cart = None
# cart = Cart.objects.get(user=request.user)
# cart of the current user
# template = loader.get_template('shop/index.html')
    context = {'all_products' : all_products,
    'n': Item.objects.filter(cart=cart).count(),
    'items': Item.objects.filter(cart = cart)
    # products in the cart of the current user
    }
    # return HttpResponse(template.render(context, request));
    return render (request , 'shop/index.html', context)

def detail(request,product_id):
    return render(request,'shop/detail.html',{'product':Product.objects.get(pk=product_id)})


def addInCart(request,product_id):
    if request.method == 'POST' and request.user.is_authenticated:
        try :
            cart = Cart.objects.get(user=request.user)
        except:
            cart = None
        try:
            product = Product.objects.get(pk = product_id)
        except :
            product = None

        try:
            item = Item.objects.get(cart = cart, product = product)
        except Item.DoesNotExist:
            item = Item()
            item.cart = cart
            item.product = product
            item.quantity = 1
            item.save()
        else:
            item.quantity += 1
            item.save()
        return redirect('index')

def remove(request,product_id):
    if request.method == "POST" and request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(pk = product_id)

        try:
            item = Item.objects.get(cart = cart , product = product)
        except Item.DoesNotExist:
            return redirect('index')
        if item.quantity != 1:
            item.quantity -= 1
            item.save()
        else :
            item.delete()
        return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()    #create and save a new form
            username = form.cleaned_data.get('username')
            # extract the username for later use
            messages.success(request, f'Account created for {username}!')
            cart = Cart()
            cart.user = User.objects.get(username=username)
            cart.title=request.user.id
            cart.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/register.html', {'form': form})

def filter(request):
    global global_filter
    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            global filter
            filter = form.cleaned_data.get('filter')
            if filter == "electric":
                global_filter = electric
            elif filter == "sports":
                global_filter = "sports"
            else:
                global_filter = None
            return redirect('index')
    else:
        form = FilterForm()
    return render(request, 'shop/filter.html' , {'form' : form})
