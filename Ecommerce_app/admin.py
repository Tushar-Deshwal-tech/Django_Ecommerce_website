from django.contrib import admin
from .models import UserData, OrderData, ReviewData

admin.site.register(UserData)
admin.site.register(OrderData)
admin.site.register(ReviewData)