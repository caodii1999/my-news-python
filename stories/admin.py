from django.contrib import admin

# Register your models here.
from .models import Category,Story, Contact, UserProfileInfo

admin.site.register(Category)
admin.site.register(Story)
admin.site.register(Contact)
admin.site.register(UserProfileInfo)

