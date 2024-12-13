from django.contrib import admin
from .models import SubscriptionPlan,User,Item,Transaction

# Register your models here.
admin.site.register(SubscriptionPlan)
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Transaction)