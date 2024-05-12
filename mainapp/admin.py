from django.contrib import admin
from .models import *
@admin.register(UserAccount)
class userAccountAdmin(admin.ModelAdmin):
    list_display=["id","name","username","phone","email","otp"]