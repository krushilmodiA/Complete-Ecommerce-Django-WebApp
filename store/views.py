from django.shortcuts import render,redirect

# authentication,login and logout functionality.
from django.contrib.auth import authenticate, login, logout
# for runtime messages 
from django.contrib import messages
# import .models.
from .models import *
# in-build User models from django models
from django.contrib.auth.models import User
# django in-build form handler.
from django.contrib.auth.forms import UserCreationForm
from django import forms 
# import form from forms.py
from .forms import *
# import from payment app.
# import payment app forms.py
from payment.forms import ShippingForm
from payment.models import ShippingAddress
# import Q for search multiple data simutanously.
from django.db.models import Q
import json
# import cart from cart app.
from cart.cart import Cart


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products': products})

# update user function
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been loggedIn!!!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, "you must be loggedIn to access that page!!!")
        return redirect('home')

# update information of user
def update_info(request):
    if request.user.is_authenticated:
         # get Current user
        current_user = Profile.objects.get(user__id = request.user.id)
        # Get Current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        # Get User's Form.
        form = UserInfoForm(request.POST or None, instance = current_user)
         # Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        #  if form or shipping form is valid then it will save all data.
        if form.is_valid() or shipping_form.is_valid():
            #  save form data.
            form.save()
            # Save shipping form
            shipping_form.save()
           
            messages.success(request, "User Information has been Updated!!!")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form,'shipping_form': shipping_form})
    else:
         messages.success(request, "you must be loggedIn to access that page!!!")
         return redirect('home')


# update user password
def update_password(request):
       if request.user.is_authenticated:
           current_user = request.user
           
           if request.method == "POST":
                form = ChangePasswordForm(current_user, request.POST)
                # is the form valid.
                if form.is_valid():
                    form.save()
                    messages.success(request, "your password has been changed!")
                    login(request, current_user)
                    return redirect('update_user')
                
                else:
                    for error in list(form.errors.values()):
                        messages.error(request, error)
                        return redirect('update_password')  
           else:
               form = ChangePasswordForm(current_user)
               return render(request, 'update_password.html',{'form': form})
 
       else:
            messages.success(request, ("you must be logged in to view that page!!!"))
            return redirect('home')

def about(request):
    return render(request, 'about.html')

# This is a login function.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # do shpping cart
            current_user = Profile.objects.get(user__id = request.user.id)
            # get their saved cart from database.
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                # convert dictionary to json.
                converted_cart = json.loads(saved_cart)
                
                #Add the lodded dictionary to our session.
                # Get the cart.
                cart = Cart(request)
                # Loop through the cart and add the items from database.
                for key, value in converted_cart.items():
                   cart.db_add(product=key, quantity=value)

            messages.success(request, ("Login successfully"))
            return redirect('home')
        else:
            messages.success(request, ("there was an error, please try again !!!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

# logout function 
def logout_user(request):
    logout(request)
    messages.success(request, ("you have been logged out !!!"))
    return redirect('home')

# register function 
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ("welcome you have Registered , Now fill up this information !!!"))
            return redirect('update_info')
        else:
            messages.success(request, ("there was an error in register page, please try again !!!"))
            return redirect('register')
    
    else:
        return render(request, 'register.html',{'form': form})
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product': product , 'product_id': product.id})

def category(request, foo):
    # replace hyphens with space.
    foo = foo.replace('-', ' ')

    try:
        category = Category.objects.get(name = foo)
        products = Product.objects.filter(category = category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ("That category dosen't exist"))
        return redirect('home')

def category_summary(request):  
        categories = Category.objects.all() 
        return render(request, 'category_summary.html', {'categories': categories})


# searched products
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains = searched))
        if not searched:
             messages.success(request, ("That product dosen't exist"))
             return redirect('search')
        else:
            return render(request, 'search.html',{'searched': searched})

    else:
       return render(request, 'search.html',{})