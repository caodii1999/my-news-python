from django import forms
from . import models
from django.core.validators import RegexValidator
from .models import UserProfileInfo, User

phone_validator = RegexValidator(
    r"((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))", "Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx!")


class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=150, label='Name', widget=forms.TextInput(attrs={
                           'placeholder': 'Enter your name', 'class': 'form-control fh5co_contact_text_box'}))
    phone_number = forms.CharField(max_length=20, label='Phone', validators=[phone_validator], widget=forms.TextInput(
        attrs={'placeholder': 'Phone number',
               'class': 'form-control fh5co_contact_text_box',
               'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
               'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'form-control fh5co_contact_text_box'}))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(
        attrs={'placeholder': 'Subject', 'class': 'form-control fh5co_contact_text_box'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Message', 'class': 'form-control fh5co_contacts_message'}))

    class Meta:
        model = models.Contact
        fields = '__all__'

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    confirm = forms.CharField(widget = forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    image = forms.ImageField(required= False)
    class Meta():
        model = UserProfileInfo
        exclude = ('user', )
