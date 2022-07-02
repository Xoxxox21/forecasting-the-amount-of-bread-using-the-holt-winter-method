from datetime import datetime
from django.shortcuts import redirect, render

from sari_roti import holtwinter
from .models import *
from .form import *
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
# from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User, BaseUserManager

def PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')
    return render(form_class,success_url)

# @login_required(login_url=settings.LOGIN_URL)
def index(request):
    data_sales = datasales.objects.all()
    data_toko = datatoko.objects.all()
    data_distribusi = datadistribusi.objects.all()
    data_jadwal = jadwal_kunjungan.objects.all()
    data_roti = dataroti.objects.all()
    total_sales = len(data_sales)
    total_toko = len(data_toko)
    total_roti = len(data_roti)
    konteks={
        'data_sales' : data_sales,
        'data_toko' : data_toko,
        'data_distribusi' : data_distribusi,
        'data_jadwal' : data_jadwal,
        'data_roti' : data_roti,
        'total_sales' : total_sales,
        'total_toko' : total_toko,
        'total_roti' : total_roti,
    }
    return render(request, 'index.html', konteks)

# @login_required(login_url=settings.LOGIN_URL)
def sales(request):
    data_sales = datasales.objects.all()
    konteks={
        'data_sales' : data_sales,
    }
    return render(request, 'datasales.html', konteks)

# @login_required(login_url=settings.LOGIN_URL)
def tambahsales(request):
    if request.POST:
        form = FormtambahSales(request.POST)
        if form.is_valid():
            form.save()
            
            #memasukkan data ke user
            # user = MyUserManager.create_user(request.post['Email'])
            
            
            pesan="Data berhasil ditambahkan"
        else:
            pesan="Data yang dimasukkan tidak valid"
        form=FormtambahSales()    
        konteks={
                'form': form,
                'pesan': pesan,
            }
        return render(request, 'tambahsales.html', konteks)
    else:
        form=FormtambahSales()
        konteks={
                'form': form,
        }
        return render(request, 'tambahsales.html', konteks)

# @login_required(login_url=settings.LOGIN_URL)
def updatesales(request, nik_sales):
    Sales = datasales.objects.get(nik=nik_sales)
    template = 'updatesales.html'
    if request.POST:
        form = FormtambahSales(request.POST, instance=Sales)
        if form.is_valid():
            form.save()
            messages.success(request,"Data berhasil diubah")
            return redirect('update-sales', nik_sales=nik_sales)             
    else:
        form = FormtambahSales(instance=Sales)
        konteks = {
            'form' : form,
            'sales' : Sales,
        }
    return render(request,template,konteks)

# @login_required(login_url=settings.LOGIN_URL)
def hapus_sales(request, nik_sales):
    Sales = datasales.objects.filter(nik=nik_sales)
    Sales.delete()
    messages.success(request,"Data Berhasil Dihapus")
    return redirect('data-sales')

# @login_required(login_url=settings.LOGIN_URL)
def toko(request):
    data_toko = datatoko.objects.all()
    konteks={
        'data_toko' : data_toko,
    }
    return render(request, 'datatoko.html', konteks)

# @login_required(login_url=settings.LOGIN_URL)
def tambahtoko(request):
    if request.POST:
        form = Formtoko(request.POST)
        if form.is_valid():
            form.save()
            pesan="Data berhasil ditambahkan"
        else:
            pesan="Data yang dimasukkan tidak valid"
        form=Formtoko()
        konteks={
                'form': form,
                'pesan': pesan,
            }
        return render(request, 'tambahtoko.html', konteks)
    else:
        form=Formtoko()
        konteks={
                'form': form,
        }
        return render(request, 'tambahtoko.html', konteks)

# @login_required(login_url=settings.LOGIN_URL)
def updatetoko(request, kode):
    Toko = datatoko.objects.get(kode=kode)
    template = 'updatetoko.html'
    if request.POST:
        form = Formtoko(request.POST, instance=Toko)
        if form.is_valid():
            form.save()
            messages.success(request,"Data berhasil diubah")
            return redirect('update-toko', kode=kode)             
    else:
        form = Formtoko(instance=Toko)
        konteks = {
            'form' : form,
            'toko' : Toko,
        }
    return render(request,template,konteks)

# @login_required(login_url=settings.LOGIN_URL)
def hapus_toko(request, kode):
    Toko = datatoko.objects.filter(kode=kode)
    Toko.delete()
    messages.success(request,"Data Berhasil Dihapus")
    return redirect('data-toko')

# @login_required(login_url=settings.LOGIN_URL)
def distribusi(request):
    data_toko = datatoko.objects.all()
    data_roti = dataroti.objects.all()
    temp = []
    konteks={
        'data_toko' : data_toko,
        'data_roti' : data_roti,
        'temp'  : temp,
        'nama_toko' : 'Silahkan Pilih Toko'
    }
    return render(request, 'distribusi.html', konteks)

# @login_required(login_url=settings.LOGIN_URL)
def isi_sisa(request, id_distribusi):
    distribusi = datadistribusi.objects.get(id=id_distribusi)
    template = 'isi_sisa.html'
    if request.POST:
        form = formdistribusi(request.POST, instance=distribusi)
        if form.is_valid():
            form.save()
            messages.success(request,"Data berhasil diubah")
            return redirect('isi-sisa', id_distribusi=id_distribusi)             
    else:
        form = formdistribusi(instance=distribusi)
        konteks = {
            'form' : form,
            'distribusi' : distribusi,
        }
    return render(request,template,konteks)

# @login_required(login_url=settings.LOGIN_URL)
def DistribusiPerToko(request, kode):
    data_distribusi = datadistribusi.objects.filter(toko_id = kode)
    data_toko = datatoko.objects.all()
    data_roti = dataroti.objects.all()
    temp = []
    roti=[]
    data_dropping = {}
    
    #looping untuk mengambil data tanggal dari datadistribusi yang dimasukkan kedalam kedalam temp agar ketika ditampilkan tidak sama
    for r in data_roti:
        roti.append(r.kode)
        
    for data in data_distribusi:
        IsMatch = False
        # ambil data tanggal
        for i in range(len(temp)):
            if temp[i] == data.tanggal:
                IsMatch = True
        if IsMatch:
            continue
        else:
            temp.append(data.tanggal)
        #metode HWES    
    for id in data_distribusi:
        for id_roti in roti:
                for id_tanggal in temp:
                    if id.tanggal == id_tanggal and id.roti_id == id_roti:
                        data_dropping[id_tanggal] = id_roti
        print(data_dropping.keys())
            
    
    #looping untuk mengambil data nama dari data toko
    for toko in data_toko:
        if toko.kode == kode:
            nama_toko = toko.nama
    konteks={
        'data_distribusi' : data_distribusi,
        'data_toko' : data_toko,
        'data_roti' : data_roti,
        'nama_toko' :'Toko '+nama_toko,
        'temp'  : temp,
        'hasil' : data_dropping,
    }
    return render(request, 'distribusi.html', konteks)

# @login_required(login_url=settings.LOGIN_URL)
def droping(request):
    if request.POST:
        form = formdistribusi(request.POST)
        if form.is_valid():
            form.save()
            pesan="Data berhasil ditambahkan"
        else:
            pesan="Data yang dimasukkan tidak valid"
        form=formdistribusi()    
        konteks={
                'form': form,
                'pesan': pesan,
            }
        return render(request, 'droping.html', konteks)
    else:
        form=formdistribusi()
        konteks={
                'form': form,
        }
        return render(request, 'droping.html', konteks)

def DistribusiUser(request, kode):
    data_distribusi = datadistribusi.objects.filter(toko_id = kode)
    data_toko = datatoko.objects.all()
    data_tampil = {}
    for data in data_distribusi:
        if data.tanggal == datetime.date.today():
            print(data.tanggal)
    for toko in data_toko:
        if toko.kode == kode:
            nama_toko = toko.nama
    konteks={
        'data_distribusi' : data_distribusi,
        'data_toko' : data_toko,
        'nama_toko' :'Toko '+nama_toko,
    }
    return render(request, 'distribusi_user.html', konteks)
    

# @login_required(login_url=settings.LOGIN_URL)
def jadwal(request):
    data_jadwal = jadwal_kunjungan.objects.all()
    konteks={
        'data_jadwal' : data_jadwal
    }
    return render(request, 'jadwal.html',konteks)

# @login_required(login_url=settings.LOGIN_URL)
def tambahjadwal(request):
    if request.POST:
        form = form_jadwal_kunjungan(request.POST)
        if form.is_valid():
            form.save()
            pesan="Data berhasil ditambahkan"
        else:
            pesan="Data yang dimasukkan tidak valid"
        form=form_jadwal_kunjungan()    
        konteks={
                'form': form,
                'pesan': pesan,
            }
        return render(request, 'tambahjadwal.html', konteks)
    else:
        form=form_jadwal_kunjungan()
        konteks={
                'form': form,
        }
        return render(request, 'tambahjadwal.html', konteks)

# @login_required(login_url=settings.LOGIN_URL)
def updatejadwal(request, id_jadwal):
    Jadwal = jadwal_kunjungan.objects.get(id=id_jadwal)
    template = 'updatejadwal.html'
    if request.POST:
        form = form_jadwal_kunjungan(request.POST, instance=Jadwal)
        if form.is_valid():
            form.save()
            messages.success(request,"Data berhasil diubah")
            return redirect('update-jadwal', id_jadwal=id_jadwal)             
    else:
        form = form_jadwal_kunjungan(instance=Jadwal)
        konteks = {
            'form' : form,
            'jadwal' : Jadwal,
        }
    return render(request,template,konteks)

# @login_required(login_url=settings.LOGIN_URL)
def hapus_jadwal(request, id_jadwal):
    Jadwal = jadwal_kunjungan.objects.filter(id=id_jadwal)
    Jadwal.delete()
    messages.success(request,"Data Berhasil Dihapus")
    return redirect('data-jadwal-kunjungan')

# @login_required(login_url=settings.LOGIN_URL)
def roti(request):
    data_roti = dataroti.objects.all()
    konteks={
        'data_roti' : data_roti
    }
    return render(request, 'dataroti.html',konteks)

# @login_required(login_url=settings.LOGIN_URL)
def tambahroti(request):
    if request.POST:
        form = form_roti(request.POST)
        if form.is_valid():
            form.save()
            pesan="Data berhasil ditambahkan"
        else:
            pesan="Data yang dimasukkan tidak valid"
        form=form_roti()    
        konteks={
                'form': form,
                'pesan': pesan,
            }
        return render(request, 'tambahroti.html', konteks)
    else:
        form=form_roti()
        konteks={
                'form': form,
        }
        return render(request, 'tambahroti.html', konteks)

# @login_required(login_url=settings.LOGIN_URL)
def updateroti(request, kode):
    roti = dataroti.objects.get(kode=kode)
    template = 'updateroti.html'
    if request.POST:
        form = form_roti(request.POST, instance=roti)
        if form.is_valid():
            form.save()
            messages.success(request,"Data berhasil diubah")
            return redirect('update-roti', kode=kode)             
    else:
        form = form_roti(instance=roti)
        konteks = {
            'form' : form,
            'roti' : roti,
        }
    return render(request,template,konteks)

# @login_required(login_url=settings.LOGIN_URL)
def hapus_roti(request, kode):
    roti = dataroti.objects.filter(kode=kode)
    roti.delete()
    messages.success(request,"Data Berhasil Dihapus")
    return redirect('data-roti')

# def login_view(request):
#     form = LoginForm(request.POST or None)
#     msg = None
#     if request.method == 'POST':
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None and user.is_admin:
#                 login(request, user)
#                 return redirect('adminpage')
#             elif user is not None and user.is_sales:
#                 login(request, user)
#                 return redirect('sales')
#             else:
#                 msg= 'invalid credentials'
#         else:
#             msg = 'error validating form'
#     return render(request, 'registrations/login.html', {'form': form, 'msg': msg})
