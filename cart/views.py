from django.shortcuts import render,get_object_or_404, redirect
from .cart  import *
from store.models import *
from django.http import JsonResponse
# for runtime messages 
from django.contrib import messages
# Create your views here.

def cart_summary(request):
    # get the Cart
    cart = Cart(request)
    cart_products = cart.get_prods 
    quantities = cart.get_quants  #<!-- product quantities in cart -->
    totals = cart.cart_total()
    return render(request, 'cart_summary.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals})

def cart_add(request):
    # get the cart
    cart = Cart(request)
    # test for post
    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty')) #<!-- product quantities in cart -->

         # lookup product in database.
        
        product = get_object_or_404(Product, id = product_id)

        # save to session
        cart.add(product = product, quantity = product_qty)
         
        #  get cart quantity 
        cart_quantity = cart.__len__()

        #  return response
        # It will help in future you want to return (product name). 
        # response = JsonResponse({'Product Name:': product.name })

        # return cart quantity
        response = JsonResponse({'qty': cart_quantity }) #<!-- product quantities in cart -->
        messages.success(request, ("Item has been added in cart!!!"))
        return response
    
    return render(request, 'cart_summary.html',{})

def cart_delete(request):
    # get the cart
    cart = Cart(request)
    # test for post
    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))

        cart.delete(product = product_id)
 
        response = JsonResponse({'product': product_id })
        messages.success(request, ("cart item has been deleted!!!"))
        return response
    
def cart_update(request):
     # get the cart
    cart = Cart(request)
    # test for post
    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty')) #<!-- product quantities in cart -->

        # check product id and quantity is post or not? just print?
        # print("views.py")
        # print('product id :', product_id)
        # print('product qty :', product_qty)

        cart.update(product = product_id, quantity = product_qty)

        response = JsonResponse({'qty': product_qty })
        messages.success(request, ("cart item has updated!!!"))
        return response 
        # return redirect('cart_summary')
