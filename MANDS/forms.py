from django.contrib.auth import models
from .models import CustomUser, Banner, Ads, Service, Product, Parts, Book
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm

# create Banner Form
class AddBanner(ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"


# create Service Form
class AddService(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"


# create Product Form
class AddProduct(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"



# create Parts Form
class AddParts(ModelForm):
    class Meta:
        model = Parts
        fields = "__all__"



# create Book Form
class AddBook(ModelForm):
    class Meta:
        model = Book
        fields = ["email", "number", "firstname", "middlename", "lastname", "location", "date", "time", "price", "service_charge", "parts_name"]


# create staff form
class CreateStaff(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "firstname", "middlename", "lastname", "number", "location", "password"]


class ProblemBook(ModelForm):
    class Meta:
        model = Book
        fields = ["email", "number", "firstname", "middlename", "lastname", "location", "date", "time", "price", "service_charge", "parts_name"]
        widgets = {
            "price": forms.NumberInput(attrs={"value": 0}),  # Set your desired default value here
            "service_charge": forms.NumberInput(attrs={"value": 0}),  # Set your desired default value here
            "parts_name": forms.TextInput(attrs={"value": "Problem Unknown"}),  # Set your desired default value here
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length = 100)
    subject = forms.CharField(max_length = 200)
    email_address = forms.EmailField(max_length = 320)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000)




# create Edit profile form
class EditProfile(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["image","firstname", "middlename", "lastname", "number", "location"]

# create password change form
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ["old_password", "new_password1", "new_password2"]