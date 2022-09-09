
from django import forms
from django.forms import ModelForm
from .models import *

from dataclasses import field
from re import U
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class ChangePass(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class FormtambahSales(ModelForm):
    class Meta:
        model = datasales
        fields = '__all__'

class Formtoko(ModelForm):
    class Meta:
        model = datatoko
        fields = '__all__'
        
class form_jadwal_kunjungan(ModelForm):
    class Meta:
        model = jadwal_kunjungan
        fields = '__all__'
        
class form_roti(ModelForm):
    class Meta:
        model = dataroti
        fields = '__all__'
        widget = {
            'kode' : forms.TextInput(),
            'nama' : forms.TextInput(),
            'harga' : forms.TextInput(),
        }
        
class formdistribusi(ModelForm):
    class Meta:
        model = datadistribusi
        fields = '__all__'