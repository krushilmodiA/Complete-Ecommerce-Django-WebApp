from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile) # Here i have registered profile model. 

# ----User model perameter inline ----
# Mix profile and user info.
class ProfileInline(admin.StackedInline):
    model = Profile

# extend User model.
class UserAdmin(admin.ModelAdmin):
        model = User
        field = ['username','first_name','last_name','email']
        inlines = [ProfileInline]

# un-register the old way.
admin.site.unregister(User)

# re-register the new way.
admin.site.register(User, UserAdmin)

# ----User model perameter inline ----
