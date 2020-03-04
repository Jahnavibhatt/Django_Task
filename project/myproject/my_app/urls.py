from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    url('dashboard/', views.dash_board, name='dashboard/'),
    url('login/', views.login_user, name='login/'),
    # url('connection/',views.formView, name = 'loginform'),
    # url('connection/',views.formView,name='loginform')
    url('home/', views.order_menu, name='home/'),
    url('order/', views.admin_view, name='order/'),
    path('user_details/<int:id>', views.user_details, name='user_details'),
    path('bill_show/',views.Bill_pdf_view,name='bill_show/'),
    url('register/', views.register_user, name='register/'),
    url('logout/', views.logout_user, name='logout/'),
    url('menu/', views.pdf_view, name='menu/'),
    url('menu/', views.pdf_view, name='menu/'),
    url('order_placed/', views.Order_view, name="order_placed/"),
    url(r'^forgetPassword', views.forget_password, name='forgetPassword'),
    path('resetpassword/<int:id>', views.reset_password, name='resetpassword/'),
    url('change_password/',views.change_password,name='change_password/'),
    url('password_reset_complete/', views.password_reset_complete, name="password_reset_complete/")
]


from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)