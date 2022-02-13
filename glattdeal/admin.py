from django.contrib import admin
from .models import Deal,User,UserDetail,Payment,Supplier,Reviews,Cart,Category,Location
# Register your models here.
admin.site.register(Deal)
admin.site.register(UserDetail)
admin.site.register(Payment)
admin.site.register(Supplier)
admin.site.register(Reviews)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Location)