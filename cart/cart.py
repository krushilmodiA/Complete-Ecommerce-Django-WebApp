# import store models
from store.models import *

# create session code

class Cart():
    def __init__(self, request):
        self.session = request.session
        
        #get request 
        self.request = request

        # get the current session key if it exists.
        cart = self.session.get('session_key')

        # if user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available in all pages of site
        self.cart = cart                
    
        # add to cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            # return quantity
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

         #deal with logged in user
        if self.request.user.is_authenticated:
            
            # get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
             
            # Convert {'3':1,'2':4} to {"3":1,"2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            
            # save carty to the profile.
            current_user.update(old_cart=str(carty))
         
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity) #<!-- product quantities in cart -->

        # if product_id already present in cart then pass
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            # return quantity
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

         #deal with logged in user
        if self.request.user.is_authenticated:
            
            # get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
             
            # Convert {'3':1,'2':4} to {"3":1,"2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            
            # save carty to the profile.
            current_user.update(old_cart=str(carty))

    # for Total sum of the all product in cart.
    def cart_total(self):
        # get product ids
        product_ids = self.cart.keys()
        # lookup those keys in our products database models.
        products = Product.objects.filter(id__in = product_ids)
        
        # get quantities
        quantities = self.cart

        # sart counting at 0

        total = 0

        for key, value in quantities.items():
            # convert key string into integer for math operation.
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        
        return total

     # update cart quantity (or) total items length.
       
    def __len__(self):
        return len(self.cart)
    
     
     #
    def get_prods(self):
        
        # get ids from cart
        product_ids = self.cart.keys()
        
        #use ids to lookup products in database models.
        products = Product.objects.filter(id__in = product_ids)

        return products
    
        
        #<!-- product quantities in cart -->

    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # get the cart
        ourcart = self.cart

        # update cart/quantity
        ourcart[product_id] = product_qty

        self.session.modified = True

        #deal with logged in user
        if self.request.user.is_authenticated:
            
            # get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
             
            # Convert {'3':1,'2':4} to {"3":1,"2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            
            # save carty to the profile.
            current_user.update(old_cart=str(carty))

        thing = self.cart 
        return thing
    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        
        self.session.modified = True

         #deal with logged in user
        if self.request.user.is_authenticated:
            
            # get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
             
            # Convert {'3':1,'2':4} to {"3":1,"2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            
            # save carty to the profile.
            current_user.update(old_cart=str(carty))
