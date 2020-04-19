from django.shortcuts import render,redirect
from .models import cart
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from accounts.forms import LoginForm,GuestForm
from accounts.models import GuestEmail
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

    request.session['cart_items'] = cart_obj.products.count()

    # cart_obj.title = "add"
    # cart_obj.save()
    return redirect("carts:home")


def checkout_home(request):
    cart_obj,cart_created       = cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count()==0:
        return redirect("cart:home")

    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        print("yayaya")
        billing_profile,billing_profile_created = BillingProfile.objects.get_or_create(user=user,email=user.email)
    elif guest_email_id is not None:
        print("aahoaaho")
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile,billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass

    if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True)
        if order_qs.count()==1:
            order_obj = order_qs.first()
        else:
            # old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
            # if old_order_qs.exists():
            #     old_order_qs.update(active=False)

            order_obj = Order.objects.create(billing_profile=billing_profile,cart=cart_obj)



    context = {
        "object":order_obj,
        "billing_profile":billing_profile,
        "login_form":login_form,
        "guest_form":guest_form,

    }
    return render(request,"carts/checkout.html",context)
