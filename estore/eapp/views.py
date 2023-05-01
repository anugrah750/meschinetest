
from django.contrib.auth import authenticate, login ,logout
from django.shortcuts import redirect, render
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
# Create your views here.

# def home(request):
#     return render(request,"../eapp/estore/templates/eapp/main.html")



def home(request):
    return render(request,"home.html")

def signup(request):

    if request.method=="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1!=pass2:
            messages.error(request,"password not match")

        if User.objects.filter(username=username):
            messages.error(request,"username already taken")
            return redirect('home')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name =lname

        myuser.save()

        messages.success(request,"your account created successfully")
        return redirect('signin')
    
    return render(request,"signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']


        user = authenticate(username=username,password=pass1)

        if user is not None:
            login(request, user)
            fname =user.first_name
            return render(request,"store.html",{'fname': fname})
        else:
            messages.error(request,"please retry")

    return render(request,"signin.html")
def signout(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect('home')

def store(request):

    # if request.user.is_authenticated:
    #     complete = request.user.complete
    #     order, created = Order.objects.get_or_create(customer=complete, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
    #     items = []
    #     order = {'get_cart_total':0, 'get_cart_items':0}
    #     cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products}
    # , 'cartItems':cartItems
    return render(request,'store.html', context)

def cart(request):

    # if request.user.is_authenticated:
    #     customer = request.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    # else:
    #     items = []
    #     order = {'get_cart_total':0, 'get_cart_items':0}
    #     cartItems = order.get_cart_items

    # context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request,"cart.html")

def updateItem(request):
    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:


        return JsonResponse('item was added', safe=False)






