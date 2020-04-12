from django.shortcuts import render,redirect
from .models import cart
from products.models import Product
# Create your views here.

def cart_create(user=None):
    cart_obj = cart.objects.create(user=None)
    print("New cart created")
    return cart_obj

def  cart_home(request):
    cart_obj,new_obj = cart.objects.new_or_get(request)
    return render(request,"carts/home.html",{"cart":cart_obj})


def cart_update(request):
    print(request.POST)

    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product does not exist")
            return redirect("cart:home")

        cart_obj,new_obj = cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)

    # cart_obj.title = "add"
    # cart_obj.save()
    return redirect("carts:home")


