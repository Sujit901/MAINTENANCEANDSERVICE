"""MaintenanceANDService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MANDS.views import index_view, signup_view, login_view, logout_view, token_send, success, verify, error_page
from MANDS.views import addBanner, banner, editBanner, deleteBanner, sureBanner
from MANDS.views import addService, service, editService, deleteService, sureService
from MANDS.views import addProduct, product, editProduct, deleteProduct, sureProduct
from MANDS.views import addParts, parts, editParts, deleteParts, sureParts
from MANDS.views import bookService, viewBookService, editBook, sureBook, deleteBook, userViewBook, acceptBook, viewAcceptedBook
from MANDS.views import completeBook, viewCompletedBook, pendingBook, sureCompletedBook, deleteCompletedBook, problemUnknown
from MANDS.views import sureAcceptedStatus, surePendingStatus, contact, successsend
from MANDS.views import createStaff, showStaff, staffSearchView, deleteStaff, surestaff
from MANDS.views import profile, deleteprofile, sureprofile, editprofile, PasswordChangeView, password_success
from MANDS.views import serviceSearchView, partsSearchView, productSearchView
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index_view'),
    path('signup/', signup_view, name='signup_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('profile/<int:id>/', profile, name='profile'),
    path('deleteprofile/<int:id>/', deleteprofile, name='deleteprofile'),
    path('suredeleteprofile/<int:id>/', sureprofile, name='sureprofile'),
    path('editprofile/<int:id>/', editprofile, name='editprofile'),
    ##########################################

    # change Password
    path('change_password/', PasswordChangeView.as_view(template_name="password/password_change.html"), name='change-password'),
    path('password_success/', password_success, name='password_success'),
    #########################################
    # path('social-auth/', include('social_django.urls', namespace='social')),

    # reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="password/password_reset_form.html"),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_done.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_complete.html"),name='password_reset_complete'),

    # sigup email verification
    path('token/', token_send, name='token_send'),
    path('success/' , success, name='success'),
    path('verify/<auth_token>/', verify, name='verify'),
    path('error/', error_page, name='error'),
    #################################################

    # banner
    path('addBanner/', addBanner, name='addBanner'),
    path('banner/', banner, name='banner'),
    path('editBanner/<int:id>/', editBanner, name='editBanner'),
    path('deleteBanner/<int:id>/', deleteBanner, name='deleteBanner'),
    path('sureBanner/<int:id>/', sureBanner, name='sureBanner'),
    ####################################################

    # service
    path('addService/', addService, name='addService'),
    path('service/', service, name='service'),
    path('editService/<name>/', editService, name='editService'),
    path('deleteService/<name>/', deleteService, name='deleteService'),
    path('sureService/<name>/', sureService, name='sureService'),
    ############################################################

    # product
    path('addProduct/', addProduct, name='addProduct'),
    path('<name>/product/', product, name='product'),
    path('editProduct/<product_name>/', editProduct, name='editProduct'),
    path('deleteProduct/<product_name>/', deleteProduct, name='deleteProduct'),
    path('sureProduct/<product_name>/', sureProduct, name='sureProduct'),
    ############################################################

    # product
    path('addParts/', addParts, name='addParts'),
    path('<product_name>/parts/', parts, name='parts'),
    path('editParts/<parts_name>/', editParts, name='editParts'),
    path('deleteParts/<parts_name>/', deleteParts, name='deleteParts'),
    path('sureParts/<parts_name>/', sureParts, name='sureParts'),
    ############################################################

    # book
    path('<parts_name>/book/', bookService, name='bookService'),
    path('viewBookService/', viewBookService, name='viewBookService'),
    path('userViewBook/', userViewBook, name='userViewBook'),
    path('<int:id>/editBook/', editBook, name='editBook'),
    path('deleteBook/<int:id>/', deleteBook, name='deleteBook'),
    path('sureBook/<int:id>/', sureBook, name='sureBook'),
    path('acceptBook/<int:id>/', acceptBook, name='acceptBook'),
    path('viewAcceptedBook/', viewAcceptedBook, name='viewAcceptedBook'),
    path('completeBook/<int:id>/', completeBook, name='completeBook'),
    path('viewCompletedBook/', viewCompletedBook, name='viewCompletedBook'),
    path('pendingBook/<int:id>/', pendingBook, name='pendingBook'),
    path('deleteCompletedBook/<int:id>/', deleteCompletedBook, name='deleteCompletedBook'),
    path('sureCompletedBook/<int:id>/', sureCompletedBook, name='sureCompletedBook'),
    path('sureAcceptedStatus/<int:id>/', sureAcceptedStatus, name='sureAcceptedStatus'),
    path('surePendingStatus/<int:id>/', surePendingStatus, name='surePendingStatus'),
    path('problemUnknown/', problemUnknown, name='problemUnknown'),
    ###################################################################

    # staff
    path('addstaff/', createStaff, name='createStaff'),
    path('staff/', showStaff, name='showstaff'),
    path('deleteStaff/<int:id>', deleteStaff, name='deleteStaff'),
    path('suredeletestaff/<int:id>', surestaff, name='surestaff'),
    path('staffsearch/', staffSearchView, name='staffsearch'),






    path('contact/', contact, name='contact'),
    path('successsend/', successsend, name='successsend'),



    #search
    path('servicesearch/', serviceSearchView, name='serviceSearchView'),
    path('productsearch/<name>/', productSearchView, name='productSearchView'),
    path('partssearch/<product_name>/', partsSearchView, name='partsSearchView'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
