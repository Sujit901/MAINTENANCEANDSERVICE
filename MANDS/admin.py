from django.contrib import admin
from .models import CustomUser, Profile, Banner, Ads, Service, Product, Book, Parts
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Ads)
admin.site.register(Banner)
admin.site.register(Profile)
admin.site.register(Service)
admin.site.register(Product)
admin.site.register(Book)
admin.site.register(Parts)