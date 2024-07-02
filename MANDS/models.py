from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# create user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=400)
    image = models.ImageField(default='/static/profile.png')
    number = models.CharField(unique=True, max_length=10)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100)
    location = models.CharField(max_length=1000)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
# create user profile
class Profile(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# create banner model
class Banner(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length= 200, blank=True)
    date = models.DateField(auto_now=True)
    

# create Ads model
class Ads(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length= 200, blank=True)
    date = models.DateField(auto_now=True)


# create Service model
CHOICES = [
    ("AVAILABLE", "Available"),
    ("UNAVAILABLE", "Unavailable"),
]
class Service(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(max_length=1000)
    available = models.CharField(max_length=11, choices=CHOICES, default="AVAILABLE")


# create products model
CHOICES = [
    ("AVAILABLE", "Available"),
    ("UNAVAILABLE", "Unavailable"),
]
class Product(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    image = models.ImageField()
    product_name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(max_length=1000)
    available = models.CharField(max_length=11, choices=CHOICES, default="AVAILABLE")
    def name(self):
        return self.service.name
    


# create parts model
CHOICES = [
    ("AVAILABLE", "Available"),
    ("UNAVAILABLE", "Unavailable"),
]
class Parts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()
    parts_name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(max_length=1000)
    available = models.CharField(max_length=11, choices=CHOICES, default="AVAILABLE")
    price = models.IntegerField()
    service_charge = models.IntegerField()
    def product_name(self):
        return self.product.product_name


#create book service model
STATUS = [
    ("Pending", "PENDING"),
    ("Accepted", "ACCEPTED"),
    ("Completed", "COMPLETED"),
]
class Book(models.Model):
    STATUS = (
        ("Pending", "PENDING"),
        ("Accepted", "ACCEPTED"),
        ("Completed", "COMPLETED"),
    )
    email = models.EmailField(max_length=400)
    number = models.CharField(max_length=10)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100)
    location = models.CharField(max_length=1000)
    book_date = models.DateField(auto_now_add=True)
    date = models.DateField()
    time = models.TimeField()
    price = models.IntegerField()
    service_charge = models.IntegerField()
    parts_name = models.CharField(max_length=100)
    status = models.CharField(max_length=11, choices=STATUS, default="Pending")

    def set_status(self, new_status):
        if new_status in dict(self.STATUS):
            self.status = new_status
            self.save()
        else:
            raise ValueError("Invalid status value")
##########################################################################################################################################
##########################################################################################################################################