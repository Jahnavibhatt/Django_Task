from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms import ModelForm
from .models import UserProfile, Order


class SingUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}))

    # address = forms.CharField(label="", max_length=150, widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Enter your address'}))
    # phone_number = forms.CharField(label="", max_length=10, widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SingUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['username'].label = ""
        self.fields[
            'username'].help_text = '<span class="form text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password1'].label = ""
        self.fields[
            'password1'].help_text = '<ul class="from text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul></small></span>'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Enter the same password'
        self.fields['password2'].label = ""
        self.fields[
            'password2'].help_text = '<span class="form text text-muted"><small>Enter the same password as before, for verification.</small></span>'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your firstname'
        self.fields['first_name'].label = ""
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your lastname'
        self.fields['last_name'].label = ""

        # self.fields['address'].widget.attrs['class'] = 'form-control'
        # self.fields['address'].widget.attrs['placeholder'] = 'Enter your address'
        # self.fields['address'].label = ""
        #
        # self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        # self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your mobile number'
        # self.fields['phone_number'].label = ""


class UserProfileForm(forms.Form):
    address = forms.CharField(label="", max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your address'}))
    phone_number = forms.CharField(label="", max_length=10, min_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}))

    class Meta:
        models = UserProfile
        fields = ['address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter your address'
        self.fields['address'].label = ""

        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your mobile number'
        self.fields['phone_number'].label = ""


# class Order_Form(forms.Form):
#     class Meta:
#         model = Order_List
#         fields = ['user', 'item_name', 'total']


class PasswordChange(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChange, self).__init__(*args, **kwargs)

        self.fields['old_password'].help_text = ''
        self.fields['new_password1'].help_text = '<small id="emailHelp" class="form-text text-muted"><ul><li>Must be of eight characters length.</li><li>Alphanumeric and atleast one uppercase letter and symbol.</li></ul></small>'
        self.fields['new_password2'].help_text = ''

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'

        self.fields['old_password'].label = ''
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''

        self.fields['old_password'].widget.attrs['placeholder'] = 'Old Password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'
