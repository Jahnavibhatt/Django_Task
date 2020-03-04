from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from djongo.models import json
from weasyprint import HTML
from .forms import SingUpForm, UserProfileForm, PasswordChange
from .models import UserProfile, Menu, Order
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
import re
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def home(request):
    print("print home")
    return render(request, 'home.html', {})


def login_user(request):
    # print("login user")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # if user.is_superuser:
        #     login(request, user)
        #     messages.success(request, 'you are superuser')
        #     return redirect('order/')
        if user is not None:
            if user.is_superuser:
                login(request, user)
                messages.success(request, 'you are superuser')
                return redirect('order/')
            login(request, user)
            messages.success(request, 'you are sucessfully log in')
            return redirect('home/')
        else:
            messages.success(request, 'Error logged in...please try again later')
            return redirect('login/')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'you have been logged out....')
    return redirect("dashboard/")


def register_user(request):
    print("------register_user-------")
    success = ''
    error = ''
    if request.method == "POST":
        # print("post---------")
        form = SingUpForm(request.POST)
        # print("form 1 :", form)
        profile_form = UserProfileForm(request.POST)
        # print("profile_form :", profile_form)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            # print('user :', user, type(user))
            user.save()
            print(user)
            U = User.objects.get(username=user)
            # userDetails = request.get(username=user.username)
            # print("userDetails :", userDetails, userDetails.id)
            profile = UserProfile()
            profile.user = U
            profile.address = profile_form.cleaned_data['address']
            profile.phone_number = profile_form.cleaned_data['phone_number']
            profile.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            success = 'you have sucessfully register ....'
            # login(request, user)
            return redirect('login/')
        else:
            error = "Form not valid"
    else:
        # print("else--")
        form = SingUpForm()
        # print("form :", form)
        profile_form = UserProfileForm()
        # print('profile_form :', profile_form)
    context = {'form': form, 'profile_form': profile_form, 'success': success, "error": error}
    return render(request, 'register.html', context)


def forget_password(request):
    if request.method == "POST":
        emailto = request.POST['email']
        print('emailto :', emailto)
        if User.objects.filter(email=emailto).exists():
            userData = User.objects.get(email=emailto)
            print("userData id :", userData.id, type(userData.id))
            current_site = get_current_site(request)
            domain = current_site.domain
            print("domain :", domain)
            url = 'http://127.0.0.1:8000/Food/resetpassword/' + str(userData.id)
            print("url :", url)
            subject = "you can change your password.."
            planinMessage = url
            from_email = 'Food Delivary System < janvibhatt1896@gmail.com >'
            mail.send_mail(subject, planinMessage, from_email, [emailto])
            print('mail:', mail)
            success = "sent mail sucessfully"
            return render(request, 'forget_password.html', {'success': success})
        else:
            error = "mailid not register"
            return render(request, 'forget_password.html', {'error': error})

    return render(request, 'forget_password.html')


def reset_password(request, id):
    print("reset pass")
    print(id)
    if request.method == "POST":
        newpassword = request.POST['newpassword']
        confinewpassword = request.POST['confinewpassword']
        if newpassword == confinewpassword:
            flag = 0
            error = ""
            while True:
                print("hello")
                if len(newpassword) < 8:
                    error = "password should be min of 8 character"
                    flag = -1
                    break
                if not re.search("[a-z]", newpassword):
                    error = "password should have atleast one alphabet in lower case"
                    flag = -1
                    break
                if not re.search("[A-Z]", newpassword):
                    flag = -1
                    error = "At least one alphabet should be of Upper Case"
                    break
                if not re.search("[0-9]", newpassword):
                    flag = -1
                    error = "At least 1 number or digit between [0-9]"
                    break
                if re.search("\s", newpassword):
                    flag = -1
                    error = "password should not contain white space"
                    break
                else:
                    flag = 0
                    print("Valid Password")
                    break

            if flag == -1:
                print("Not a Valid Password")
                return render(request, "reset_password.html", {'error': error})
            # if len(newpassword) < 8:
            #     error ="your password should be of 8 characters"
            #     return redirect("password_reset_complete/", {'error': error})
            # elif
            else:
                u = User.objects.get(id=id)
                u.set_password(newpassword)
                u.save()
                print("match pass")
                return redirect("password_reset_complete/")
        else:
            error = "please enter the same password"
            return render(request, "reset_password.html", {'error': error})
    else:
        return render(request, 'reset_password.html')


def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


def dash_board(request):
    print("dashboard ---")
    return render(request, 'dashboard.html')


def pdf_view(request):
    with open('/home/jahanvi/Downloads/DELICIOUS_MENU.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename = menu.pdf'
        return response


@login_required(login_url='login/')
def order_menu(request):
    menus = Menu.objects.all()
    return render(request, 'home.html', {'menu': menus})


@login_required(login_url='login/')
def Order_view(request):
    print("hello 1")
    if request.method == 'GET':
        print("hello 2", request.GET)
        user = request.GET.get('user_id')
        item = request.GET.getlist('item_id[]')
        Quntity = request.GET.getlist('quntity_item[]')
        total = request.GET.get('total')
        # print("user--", user)
        # print("item id---", item)
        # print("total---", total)
        # print("qunatity---",Quntity)
        u = User.objects.get(id=user)
        users = UserProfile.objects.get(user_id=u.id)
        m = Order.objects.create(user=u, item=item, total=total, Quntity=Quntity)
        list = m.item
        # print(list)
        List = m.Quntity
        # print(List)
        itemName = []
        itemprice = []
        Quntity_list = []
        for qun in List:
            print("quntity",qun)
            Quntity_list.append(qun)
            print(Quntity_list)
        for item in list:
            print(item)
            menu = Menu.objects.get(id=item)
            print(menu)
            # print(menu.item_name)
            itemName.append(menu.item_name)
            itemprice.append(menu.price)
        context = {'orders': m, 'users': users, 'menu': itemName, 'menus': itemprice ,'quns':Quntity_list}
        # m = Order.objects.create(user=request.get(id=user), item=item, total=total)
        # return HttpResponse("Success!")  # Sending an success response
        return render(request, 'Bill.html', context)


@login_required(login_url='login/')
def admin_view(request):
    orders = Order.objects.all()
    # for order in orders:
    #     print(order.user_id)
    return render(request, 'orderlist.html', {'orders': orders})


def user_details(request, id):
    print("order id is", id)
    orders = Order.objects.get(id=id)
    print(orders.item)
    list = orders.item
    print("user id ", orders.user_id)
    users = UserProfile.objects.get(user_id=orders.user_id)
    itemName = []
    itemprice = []
    for item in list:
        # print(item)
        menu = Menu.objects.get(id=item)
        # print(menu)
        # print(menu.item_name)
        itemName.append(menu.item_name)
        itemprice.append(menu.price)
        # print("itemName--", itemName)
        # print("itemprice--", itemprice)
    context = {'orders': orders, 'users': users, 'menu': itemName, 'menus': itemprice}
    return render(request, 'user_order.html', context)


def Bill_pdf_view(request):
    data = Order.objects.filter(user=request.user).latest('id')
    u = data.user_id
    users = UserProfile.objects.get(user_id=u)
    list = data.item
    itemName = []
    itemprice = []
    for item in list:
        # print(item)
        menu = Menu.objects.get(id=item)
        # print(menu)
        # print(menu.item_name)
        itemName.append(menu.item_name)
        itemprice.append(menu.price)
    context = {'orders': data, 'users': users, 'menu': itemName, 'menus': itemprice}

    html_string = render_to_string('Bill_pdf.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target='Bill_pdf.pdf')

    fs = FileSystemStorage('')
    with fs.open('Bill_pdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attatchment; filename="Bill_pdf.pdf"'
        return response
    return response
    # return render(request,'Bill_pdf.html')

def change_password(request):
    if request.method == "POST":
        form = PasswordChange(data=request.POST or None, user=request.user)
        if form.is_valid():
            old_password = request.POST.get("old_password")
            new_password1 = request.POST.get("new_password1")
            new_password2 = request.POST.get("new_password2")
            if old_password == new_password1:
                messages.success(request, "new password must be diffrent form current password.")
                return redirect('change_password/')
            else:
                form.save()
                messages.success(request, "You have successfully changed your password.")
                return redirect('dashboard/')
    else:
        form = PasswordChange(user=request.user)
    context = {'form': form}
    return render(request, 'change_password.html', context)


