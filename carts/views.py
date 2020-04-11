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

    products = cart_obj.products.all()
    total = 0
    for x in products:
        total += x.price
    print(total)
    cart_obj.total = total
    cart_obj.save()

    # del request.session['cart_id']
    # request.session['cart_id'] = "12"
    # cart_id  = request.session.get('cart_id',None)
    # # if cart_id is None:
    #     cart_obj = cart_create()
    #     request.session['cart_id']=cart_obj.id
    # else:
    # qs = cart.objects.filter(id=cart_id)
    # if qs.count()==1:
    #     cart_obj = qs.first()
    #     if request.user.is_authenticated and cart_obj.user is None:
    #         cart_obj.user = request.user
    #         cart_obj.save()
    # else:
    #     cart_obj = cart.objects.new(user=request.user)
    #     request.session['cart_id'] = cart_obj.id
    return render(request,"carts/home.html",{})


def cart_update(request):
    product_id = 1
    product_obj = Product.objects.get(id=product_id)
    cart_obj,new_obj = cart.objects.new_or_get(request)
    cart_obj.products.add(product_obj)
    cart_obj.title = "add"
    cart_obj.save()
    return redirect("carts:home")

