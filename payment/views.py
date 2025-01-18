from django.shortcuts import render,redirect
# for runtime messages 
from django.contrib import messages
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime

# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html')


def checkout(request):
    # get the Cart
    cart = Cart(request)
    cart_products = cart.get_prods 
    quantities = cart.get_quants  #<!-- product quantities in cart -->
    totals = cart.cart_total()

    if request.user.is_authenticated:
       shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
       shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
       return render(request, 'payment/checkout.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals,'shipping_form': shipping_form})

    else:
       shipping_form = ShippingForm(request.POST or None)
       return render(request, 'payment/checkout.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals,'shipping_form': shipping_form})
    
# billing_info
def billing_info(request):
    if request.POST:
      cart = Cart(request)
      cart_products = cart.get_prods 
      quantities = cart.get_quants  #<!-- product quantities in cart -->
      totals = cart.cart_total()
       
      # Create session with shipping
      my_shipping = request.POST
      request.session['my_shipping'] = my_shipping
        
        # check to see if user is login or not?  
      if request.user.is_authenticated:
            #get the billing form.
           billing_form = PaymentForm()    
           return render(request, 'payment/billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals,'shipping_info': request.POST,'billing_form': billing_form})
      else:
          #not logged in 
           billing_form = PaymentForm() 
           return render(request, 'payment/billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals,'shipping_info': request.POST,'billing_form': billing_form})
    
    #   shipping_info = request.POST
    #   return render(request, 'payment/billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals,'shipping_info': shipping_info})

    else:
        messages.success(request, ("Access Denied"))
        return redirect('home')
    

def process_order(request):
    if request.POST:
        # get the cart
        cart = Cart(request)
        cart_products = cart.get_prods 
        quantities = cart.get_quants  #<!-- product quantities in cart -->
        totals = cart.cart_total()

        # get Billing info from PaymentForm
        payment_form = PaymentForm(request.POST or None)
        # get shipping session data.
        my_shipping = request.session.get('my_shipping')

         # gether Order Info.
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # create shipping address from session info.
        shipping_address = F"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n" 
        amount_paid = totals

         #check if user is logged in or not?  
        if request.user.is_authenticated:
            user = request.user 
            # Create Order for loggin user.
            create_order = Order(user = user,full_name = full_name,email = email,shipping_address = shipping_address,amount_paid = amount_paid)
            create_order.save()

            # Add order Items
            # Get the orderID
            order_id = create_order.pk

            # get product info.
            for product in cart_products():
                # get product id.
                product_id = product.id
                # get product price.
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                
                # get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # create order item
                        create_order_item = OrderItem(order_id = order_id,product_id = product_id, user = user, quantity = value, price = price)
                        create_order_item.save()
            
            # delete our cart form session after it complte the whole process of payment. 
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete the kkeys
                    del request.session[key]

            # Delete cart from database (old_cart field)
            current_user = Profile.objects.filter(user__id = request.user.id)
            # reset old_cart in database.
            current_user.update(old_cart = "")

            
            messages.success(request, ("User Order placed"))
            return redirect('home')
        else:
              # Create Order for guest .
            create_order = Order(full_name = full_name,email = email,shipping_address = shipping_address,amount_paid = amount_paid)
            create_order.save()

            # Add order Items
            # Get the orderID
            order_id = create_order.pk

            # get product info.
            for product in cart_products():
                # get product id.
                product_id = product.id
                # get product price.
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                
                # get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # create order item
                        create_order_item = OrderItem(order_id = order_id,product_id = product_id, quantity = value, price = price)
                        create_order_item.save()

             # delete our cart form session after it complte the whole process of payment.
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete the kkeys
                    del request.session[key]


            messages.success(request, ("Guest Order placed"))
            return redirect('home')
        
    else:
      messages.success(request, ("Access Denied"))
      return redirect('home')
    

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        # update shipped changes.
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # grab the order id.
            order = Order.objects.filter(id=num)
            order.update(shipped=False)

            messages.success(request, "Shipping Status updated")
            return redirect('home')
        
        return render(request, 'payment/shipped_dash.html',{'orders': orders})
    else:
      messages.success(request, ("Access Denied"))
      return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
               # grab the order id.
            order = Order.objects.filter(id=num)

            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)

            messages.success(request, "Shipping Status updated")
            return redirect('home')
        return render(request, 'payment/not_shipped_dash.html',{'orders': orders})
    else:
      messages.success(request, ("Access Denied"))
      return redirect('home')
    
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # get the order.
        order = Order.objects.get(id = pk)
        # get the order items.
        items = OrderItem.objects.filter(order = pk)

        if request.POST:
            status = request.POST['shipping_status']
            # check if true or false
            if status == "true":
                # get the order
                order = Order.objects.filter(id = pk)
                # Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # get the order
                order = Order.objects.filter(id = pk)
                # Update the status
                order.update(shipped=False)
            messages.success(request, "Shipping Status updated")
            return redirect('home')

        return render(request, 'payment/orders.html',{"order": order, "items": items})
    else:
      messages.success(request, ("Access Denied"))
      return redirect('home')
    