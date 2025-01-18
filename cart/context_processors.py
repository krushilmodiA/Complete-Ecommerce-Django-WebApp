# session and add to cart

from .cart import *

# create a context processor so our cart can work on all the pages
def cart(request):
    # Return the default data from our Cart class inside the cart.py
    return {'cart': Cart(request)}
