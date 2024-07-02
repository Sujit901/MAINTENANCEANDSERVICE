import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Banner, Ads, Profile, Service, Product, Parts, Book
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import random
from random import randint
import random
import itertools
from django.db import models
from .forms import AddBanner, AddService, AddProduct, AddParts, AddBook, EditProfile, PasswordChangingForm, ProblemBook, ContactForm
from datetime import datetime

# Create your views here.


#index view
def index_view(request):
    banner = Banner.objects.all()
    service = Service.objects.all()
    context ={
        'banner':banner,
        'service':service,
    }
    return render(request, 'index.html', context)


def signup_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        number = request.POST.get('number')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        try:
            if CustomUser.objects.filter(email = email).first():
                error = "Email has been already taken!!."
                return render(request,'signup.html', {'error':error})
            
            if CustomUser.objects.filter(username = username).first():
                error = "Username is already taken."
                return render(request,'signup.html', {'error':error})
            
            if password != confirm_password:
                error = "Password and Confirm Password don't match!!!."
                return render(request, 'signup.html',{'error':error})
            
            filename = f"{uuid.uuid4().hex}.{image.name.split('.')[-1]}"
            fs = FileSystemStorage()
            fs.save(filename, image)
            user_obj = CustomUser(username = username , email = email, firstname=firstname, image = filename, middlename=middlename, lastname=lastname, number=number, location=location)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('token_send')
        except Exception as e:
            print(e)
    return render(request, 'signup.html')


# create success view of signup
def success(request):
    return render(request, 'email/success.html')

# create Token_send view for signup
def token_send(request):
    return render(request, 'email/token_send.html')


# verify view
def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                success="Your account is already verified."
                return render(request,'login.html', {'success':success})
            profile_obj.is_verified = True
            profile_obj.save()
            success = "Your account has been verified."
            return render(request,'login.html', {'success':success})
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')

# error view
def error_page(request):
    return  render(request , 'email/error.html')

# send mail view
def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi, click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

# login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = CustomUser.objects.filter(email=email).first()
        if user_obj is None:
            error ="User not found!!!."
            return render(request,'login.html',{'error':error})
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            error ="Profile is not verified check your mail."
            return render(request,'login.html',{'error':error})

        user = authenticate(request, email = email , password = password)
        if user is None:
            error = "Invalid Credentials !!! Signup to create account."
            return render(request,'login.html',{'error':error})
        
        login(request , user)
        return redirect('/')

    return render(request , 'login.html')

# logout view
@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect('login_view')


############################################################################################################################
# Add Banner
@login_required(login_url="/login/")
def addBanner(request):
    if request.user.is_superuser:
        if(request.method=='POST'):
            name = request.POST.get('name')
            image = request.FILES.get('image')
            banner_obj = Banner(image=image, name=name)
            banner_obj.save()
            return redirect('banner')
        return render(request,'addBanner.html')
    return redirect('/')

# Banner
@login_required(login_url="/login/")
def banner(request):
    if request.user.is_superuser:
        banner = Banner.objects.all()
        context = {
            'banner':banner,
        }
        return render (request, 'banner.html', context)
    return redirect('/')

# Edit banner
@login_required(login_url="/login/")
def editBanner(request, id):
    if request.user.is_superuser:
        banner = Banner.objects.get(id=id)
        form = AddBanner(instance=banner)
        if request.method == "POST":
            banner = Banner.objects.get(id=id)
            form = AddBanner(request.POST, request.FILES, instance=banner)
            if form.is_valid():
                form.save()
                return redirect('banner')
        return render(request,'editBanner.html', {'form':form, 'banner':banner})
    return redirect('/')

# Delete banner
@login_required(login_url="/login/")
def deleteBanner(request, id):
    if request.user.is_superuser:
        banner = Banner.objects.get(id=id)
        banner.delete()
        return redirect('banner')
    return redirect('/')


# sure banner
@login_required(login_url="/login/")
def sureBanner(request, id):
    if request.user.is_superuser:
        banner = Banner.objects.get(id=id)
        context = {
            'banner':banner
        }
        return render(request, 'surebanner.html', context)
    return redirect('/')
##########################################################################################################################

# Add Service
@login_required(login_url="/login/")
def addService(request):
    if request.user.is_superuser:
        if(request.method=='POST'):
            name = request.POST.get('name')
            image = request.FILES.get('image')
            description = request.POST.get('description')
            available = request.POST.get('available')
            service_obj = Service(image=image, name=name, description=description, available=available)
            service_obj.save()
            return redirect('service')
        return render(request,'addService.html')
    return redirect('/')


# Service
@login_required(login_url="/login/")
def service(request):
    if request.user.is_superuser:
        service = Service.objects.all()
        context = {
            'service':service,
        }
        return render (request, 'service.html', context)
    return redirect('/')


# Edit service
@login_required(login_url="/login/")
def editService(request, name):
    if request.user.is_superuser:
        service = Service.objects.get(pk=name)
        form = AddService(instance=service)
        if request.method == "POST":
            service = Service.objects.get(pk=name)
            form = AddService(request.POST, request.FILES, instance=service)
            if form.is_valid():
                form.save()
                return redirect('service')
        return render(request,'editService.html', {'form':form, 'service':service})
    return redirect('/')

# Delete Service
@login_required(login_url="/login/")
def deleteService(request, name):
    if request.user.is_superuser:
        service = Service.objects.get(pk=name)
        service.delete()
        return redirect('service')
    return redirect('/')


# sure service
@login_required(login_url="/login/")
def sureService(request, name):
    if request.user.is_superuser:
        service = Service.objects.get(pk=name)
        context = {
            'service':service
        }
        return render(request, 'sureService.html', context)
    return redirect('/')

###########################################################################################################################


# Add Product
@login_required(login_url="/login/")
def addProduct(request):
    if request.user.is_superuser:
        service = Service.objects.all()
        form = AddProduct(request.POST, request.FILES)
        if request.method == 'POST':
            form = AddProduct(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/')
        return render(request, 'addProduct.html',{'form':form, 'service':service})
    return redirect('/')



# Product
@login_required(login_url="/login/")
def product(request, name):
    service = Service.objects.get(pk=name)
    product = Product.objects.filter(service=service)
    context = {
        'product':product,
        'service':service
        }
    return render (request, 'product.html', context)


# Edit product
@login_required(login_url="/login/")
def editProduct(request, product_name):
    if request.user.is_superuser:
        service = Service.objects.all()
        product = Product.objects.get(pk=product_name)
        form = AddProduct(instance=product)
        if request.method == "POST":
            product = Product.objects.get(pk=product_name)
            form = AddProduct(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('/')
        return render(request,'editProduct.html', {'form':form, 'product':product, 'service':service})
    return redirect('/')

# Delete product
@login_required(login_url="/login/")
def deleteProduct(request, product_name):
    if request.user.is_superuser:
        product = Product.objects.get(pk=product_name)
        product.delete()
        return redirect('/')
    return redirect('/')


# sure product
@login_required(login_url="/login/")
def sureProduct(request, product_name):
    if request.user.is_superuser:
        product = Product.objects.get(pk=product_name)
        context = {
            'product':product
        }
        return render(request, 'sureProduct.html', context)
    return redirect('/')
###########################################################################################################################


# Add Parts
@login_required(login_url="/login/")
def addParts(request):
    if request.user.is_superuser:
        product = Product.objects.all()
        form = AddParts(request.POST, request.FILES)
        if request.method == 'POST':
            form = AddParts(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/')
        return render(request, 'addParts.html',{'form':form, 'product':product})
    return redirect('/')



# Parts
@login_required(login_url="/login/")
def parts(request, product_name):
    product = Product.objects.get(pk=product_name)
    parts = Parts.objects.filter(product=product)
    context = {
        'product':product,
        'parts':parts
        }
    return render (request, 'parts.html', context)


# Edit parts
@login_required(login_url="/login/")
def editParts(request, parts_name):
    if request.user.is_superuser:
        product = Product.objects.all()
        parts = Parts.objects.get(pk=parts_name)
        form = AddProduct(instance=parts)
        if request.method == "POST":
            parts = Parts.objects.get(pk=parts_name)
            form = AddParts(request.POST, request.FILES, instance=parts)
            if form.is_valid():
                form.save()
                return redirect('/')
        return render(request,'editParts.html', {'form':form, 'parts':parts, 'product':product})
    return redirect('/')

# Delete product
@login_required(login_url="/login/")
def deleteParts(request, parts_name):
    if request.user.is_superuser:
        parts = Parts.objects.get(pk=parts_name)
        parts.delete()
        return redirect('/')
    return redirect('/')


# sure parts
@login_required(login_url="/login/")
def sureParts(request, parts_name):
    if request.user.is_superuser:
        parts = Parts.objects.get(pk=parts_name)
        context = {
            'parts':parts
        }
        return render(request, 'sureParts.html', context)
    return redirect('/')
######################################################################################################################################## 


# Book service
@login_required(login_url="/login/")
def bookService(request, parts_name):
    parts = Parts.objects.get(pk=parts_name)
    current_date = datetime.now().date()
    form = AddBook(request.POST, instance=parts)
    book = Book.objects.all()
    if request.method == "POST":
        parts = Parts.objects.get(pk=parts_name)
        form = AddBook(request.POST)
        if form.is_valid():
            # if book.book_date < current_date:
            #     error = "Date is invalid"
            #     return render(request, "book.html", {'error':error})
            form.save()
            return redirect('/')
    return render(request,'book.html', {'form':form, 'parts':parts})


@login_required(login_url="/login/")
def problemUnknown(request):
    form = ProblemBook(request.POST)
    if request.method == "POST":
        form = ProblemBook(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'problemUnknown.html', {'form':form})


@login_required(login_url="/login/")
def userViewBook(request):
    view = Book.objects.all()
    context = {
        'view':view,
    }
    return render(request, 'UserViewBook.html', context)

@login_required(login_url="/login/")
def editBook(request, id):
    book = Book.objects.get(id=id)
    form = AddBook(instance=book)
    if request.method == "POST":
        book = Book.objects.get(id=id)
        form = AddBook(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'editBook.html', {'form':form, 'book':book})


# Delete book
@login_required(login_url="/login/")
def deleteBook(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('/')


# sure book
@login_required(login_url="/login/")
def sureBook(request, id):
    book = Book.objects.get(id=id)
    context = {
        'book':book
    }
    return render(request, 'sureBook.html', context)


@login_required(login_url="/login/")
def viewBookService(request):
    if request.user.is_staff:
        view = Book.objects.all()
        context = {
            'view':view,
        }
        return render(request, 'viewBook.html', context)
    return redirect('/')





@login_required(login_url="/login/")
def createStaff(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            fname = request.POST.get('firstname')
            mname = request.POST.get('middlename')
            lname = request.POST.get('lastname')
            username = request.POST.get('username')
            location = request.POST.get('location')
            number = request.POST.get('number')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('password2')
            try:
                if CustomUser.objects.filter(email = email).first():
                    error = "Email has been already taken!!."
                    return render(request,'createstaff.html', {'error':error})
                
                if CustomUser.objects.filter(username = username).first():
                    error = "Username is already taken."
                    return render(request,'createstaff.html', {'error':error})
                
                if password != confirm_password:
                    error = "Password and Confirm Password don't match!!!."
                    return render(request, 'createstaff.html',{'error':error})
                user_obj = CustomUser(username = username , email = email, firstname=fname, middlename=mname, lastname=lname, number=number, location=location, is_staff=True)
                user_obj.set_password(password)
                user_obj.save()
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
                profile_obj.is_verified = True
                profile_obj.save()
                return redirect('/')
            except Exception as e:
                print(e)
        return render(request , 'createstaff.html')
    return redirect('/')



# create staff view 
@login_required(login_url="/login/")
def showStaff(request):
    if request.user.is_superuser:
        staff = CustomUser.objects.filter(is_staff=True, is_superuser=False)
        context = {
            'staff':staff
        }
        return render(request, 'staff.html', context)
    return redirect('/')

# create staff view 
@login_required(login_url="/login/")
def deleteStaff(request, id):
    if request.user.is_superuser:
        s = CustomUser.objects.filter(is_staff=True, id=id)
        s.delete()
        staff = CustomUser.objects.filter(is_staff=True, is_superuser=False)
        context = {
            'staff': staff,
        }
        return render(request, 'staff.html', context)
    return redirect('/')


# create sure delete staff view
@login_required(login_url="/login/")
def surestaff(request, id):
    if request.user.is_superuser:
        staff = CustomUser.objects.filter(is_staff=True, id=id)
        context = {
            'staff':staff
        }
        return render(request, 'surestaff.html', context)
    return redirect('/')


@login_required(login_url="/login/")
def staffSearchView(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            query = request.GET.get('search')
            post = CustomUser.objects.filter(models.Q(firstname__icontains=query) | models.Q(middlename__icontains=query) | models.Q(lastname__icontains=query) | models.Q(email__icontains=query) | models.Q(username__icontains=query))
            staff = CustomUser.objects.filter(is_staff=True, is_superuser = False)
            context = {
                'staff':staff,
                'post': post,
            }
            return render(request, 'searchstaff.html', context)
        return redirect('/')
    


@login_required(login_url="/login/")
def viewAcceptedBook(request):
    if request.user.is_staff:
        view = Book.objects.all()
        context = {
            'view':view,
            }
        return render(request, 'viewAcceptedBook.html', context)
    return redirect('/')


@login_required(login_url="/login/")
def acceptBook(request, id):
    if request.user.is_staff:
        view = Book.objects.get(id=id)
        view.set_status("Accepted")
        return redirect('viewAcceptedBook')
    return redirect('/')



@login_required(login_url="/login/")
def viewCompletedBook(request):
    if request.user.is_staff:
        view = Book.objects.all()
        context = {
            'view':view,
            }
        return render(request, 'viewCompletedBook.html', context)
    return redirect('/')


@login_required(login_url="/login/")
def completeBook(request, id):
    if request.user.is_staff:
        view = Book.objects.get(id=id)
        view.set_status("Completed")
        return redirect('viewCompletedBook')
    return redirect('/')


@login_required(login_url="/login/")
def pendingBook(request, id):
    if request.user.is_staff:
        view = Book.objects.get(id=id)
        view.set_status("Pending")
        return redirect('viewBookService')
    return redirect('/')


# Delete book
@login_required(login_url="/login/")
def deleteCompletedBook(request, id):
    if request.user.is_staff:
        book = Book.objects.get(id=id)
        book.delete()
        return redirect('/')
    return redirect('/')


# sure book
@login_required(login_url="/login/")
def sureCompletedBook(request, id):
    if request.user.is_staff:
        book = Book.objects.get(id=id)
        context = {
            'book':book
        }
        return render(request, 'sureCompletedBook.html', context)
    return redirect('/')


@login_required(login_url="/login/")
def sureAcceptedStatus(request, id):
    if request.user.is_staff:
        book = Book.objects.get(id=id)
        context = {
            'book':book
        }
        return render(request, 'sureAcceptedStatus.html', context)
    return redirect('/')


@login_required(login_url="/login/")
def surePendingStatus(request, id):
    if request.user.is_staff:
        book = Book.objects.get(id=id)
        context = {
            'book':book
        }
        return render(request, 'surePendingStatus.html', context)
    return redirect('/')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Check if the email provided by the user is valid
        if not email:
            return redirect('/')  # Handle invalid email gracefully, you may want to display an error message to the user

        receiver = [settings.EMAIL_HOST_USER]
        message_body = f"From: {name} <{email}>\n\nMessage:\n{message}"
        
        try:
            send_mail(subject, message_body, email, receiver)
        except Exception as e:
            # Handle email sending errors here, e.g., log the error or show a user-friendly error message
            return redirect('/')  # Redirect back to the contact page or display an error message
        
        return redirect('successsend')
    
    return redirect('/')


def successsend(request):
    return render(request, 'successsend.html')







##################################################################################################
##########***** Profile  *****##########

# create profile view to see the profile
@login_required(login_url="/login/")
def profile(request, id):
    account = CustomUser.objects.get(id=id)
    context = {
        'account':account
    }
    return render(request, 'profile.html', context)

# create profile edit view to edit the profile
@login_required(login_url="/login/")
def editprofile(request, id):
    success= None
    account = CustomUser.objects.get(id=id)
    form = EditProfile(instance=account)
    if request.method == "POST":
        account = CustomUser.objects.get(id=id)
        form = EditProfile(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
            success = "Update Successfully. Please referesh !!!"
            return render(request, 'profile.html', {'success':success})
    return render(request,'editprofile.html', {'form':form})

# create profile delete view to delete the profile from the application
@login_required(login_url="/login/")
def deleteprofile(request, id):
    account = CustomUser.objects.get(id=id)
    account.delete()
    return redirect('login_view')



# create sure delete profile view
@login_required(login_url="/login/")
def sureprofile(request, id):
    account = CustomUser.objects.get(id=id)
    context = {
        'account':account
    }
    return render(request, 'sureprofile.html', context)
##################################################################################################


##################################################################################################
##########***** PASSWORD *****##########

# create password change view
class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, "password/password_change_success.html")
##################################################################################################




#Search view
def serviceSearchView(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        post = Service.objects.filter(models.Q(name__icontains=query))
        service = Service.objects.all()
        context = {
            'post': post,
            'service' : service,
        }
        return render(request, 'searchservice.html', context)
    

def partsSearchView(request, product_name):
    if request.method == 'GET':
        query = request.GET.get('search')
        product = Product.objects.get(pk = product_name)
        parts = Parts.objects.filter(product = product)
        if parts:
            post = Parts.objects.filter(models.Q(parts_name__icontains=query) | models.Q(price__icontains=query) | models.Q(service_charge__icontains=query))
            context = {
                'product': product,
                'post': post,
                'parts' : parts,
            }
            return render(request, 'searchparts.html', context)
    
def productSearchView(request, name):
    if request.method == 'GET':
        query = request.GET.get('search')
        service = Service.objects.get(pk = name)
        product = Product.objects.filter(service = service)
        if product:
            post = Product.objects.filter(models.Q(product_name__icontains=query))
            context = {
                'product': product,
                'post': post,
                'service' : service,
            }
            return render(request, 'searchproduct.html', context)