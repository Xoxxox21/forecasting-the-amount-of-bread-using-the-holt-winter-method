from django import forms
from django.forms import ModelForm
from .models import *
        
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