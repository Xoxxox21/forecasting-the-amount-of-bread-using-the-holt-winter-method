import io
from django.shortcuts import redirect, render
from matplotlib import pyplot as plt
import pandas as pd
from sari_roti.decorators import admin_only, allowed_users, unauthenticated_user
from .models import *
from .form import *
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from statsmodels.tsa.api import ExponentialSmoothing
from django.contrib.auth.models import Group

@login_required(login_url='login')
def PasswordsChangeView(request):
    form = ChangePass(request.POST)
    if request.POST:
        form = ChangePass(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password berhasil diubah')
            return redirect('ganti-password')
    konteks = {
        'form': form,
    }
    return render(request, 'registration/change_pass.html', konteks)

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
def sales(request):
    data_sales = datasales.objects.all()
    konteks={
        'data_sales' : data_sales,
    }
    return render(request, 'datasales.html', konteks)

@login_required(login_url='login')
@admin_only
def tambahsales(request):
    if request.POST:
        form = FormtambahSales(request.POST)
        if form.is_valid():
            form.save()
            
            #membuat user
            user = User.objects.create_user(
                nik=form.cleaned_data['nik'],
                password='nama1234',
            )
            user.save()
            #membuat group
            group = Group.objects.get(name='sales')
            user.groups.add(group)
            pesan = "Data berhasil ditambahkan"
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

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
def hapus_sales(request, nik_sales):
    Sales = datasales.objects.filter(nik=nik_sales)
    Sales.delete()
    messages.success(request,"Data Berhasil Dihapus")
    return redirect('data-sales')

@login_required(login_url='login')
@admin_only
def toko(request):
    data_toko = datatoko.objects.all()
    konteks={
        'data_toko' : data_toko,
    }
    return render(request, 'datatoko.html', konteks)

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
def hapus_toko(request, kode):
    Toko = datatoko.objects.filter(kode=kode)
    Toko.delete()
    messages.success(request,"Data Berhasil Dihapus")
    return redirect('data-toko')

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
def DistribusiPerToko(request, kode):
    data_distribusi = datadistribusi.objects.filter(toko_id = kode)
    data_toko = datatoko.objects.all()
    temp = []
    roti=[]
    data_dropping = {}
    tanggal = []
    droping = []
    
    #looping untuk mengambil data tanggal dari datadistribusi yang dimasukkan kedalam kedalam temp agar ketika ditampilkan tidak sama
    for data_ in data_distribusi:
        IsMatch = False
        # ambil data tanggal
        for i in range(len(roti)):
            if roti[i] == data_.roti_id:
                IsMatch = True
        if IsMatch:
            continue
        else:
            roti.append(data_.roti_id)
        
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
    for i in range(len(roti)):
        data_dropping[str(roti[i])] = {
                'tanggal' : [],
                'dropping' : [],
        }
    # print(data_dropping)
        for data in data_distribusi:
            if data.roti_id == roti[i]:
                tanggal.append(str(data.tanggal))
                droping.append(data.dropping)
        data_dropping[str(roti[i])]['tanggal'] = tanggal
        data_dropping[str(roti[i])]['dropping'] = droping
        tanggal = []
        droping = []
        df = pd.DataFrame(data_dropping[str(roti[i])])
        df.set_index('tanggal', inplace=True)
        # df.plot(kind='line', title=str(roti[i]))
        # plt.show()
        df_train = df.iloc[:-72]
        df_test = df.iloc[-72:]
        # model = ExponentialSmoothing(df_train, trend='add',seasonal='mul',seasonal_periods=7).fit()
        # print(model.summary())
        # print(str(roti[i]))
        # predik = model.forecast(steps = 31)

    #looping untuk mengambil data nama dari data toko
    for toko in data_toko:
        if toko.kode == kode:
            nama_toko = toko.nama
    konteks={
        'data_distribusi' : data_distribusi,
        'data_toko' : data_toko,
        'data_roti' : roti,
        'nama_toko' :'Toko '+nama_toko,
        'temp'  : temp,
        'hasil' : data_dropping,
    }
    return render(request, 'distribusi.html', konteks)

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['sales'])
def DistribusiUser(request):
    data_toko = datatoko.objects.all()
    konteks={
        'data_toko' : data_toko,
        'nama_toko' : 'Silahkan Pilih Toko'
    }
    return render(request, 'distribusi_user.html', konteks)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['sales'])
def DistribusiUserToko(request, kode):
    data_distribusi = datadistribusi.objects.filter(toko_id = kode)
    data_toko = datatoko.objects.all()
    temp = []
    roti=[]
    data_dropping = {}
    tanggal = []
    droping = []
    
    #looping untuk mengambil data tanggal dari datadistribusi yang dimasukkan kedalam kedalam temp agar ketika ditampilkan tidak sama
    for data_ in data_distribusi:
        IsMatch = False
        # ambil data tanggal
        for i in range(len(roti)):
            if roti[i] == data_.roti_id:
                IsMatch = True
        if IsMatch:
            continue
        else:
            roti.append(data_.roti_id)
        
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

    #looping untuk mengambil data nama dari data toko
    for toko in data_toko:
        if toko.kode == kode:
            nama_toko = toko.nama
    konteks={
        'data_distribusi' : data_distribusi,
        'data_toko' : data_toko,
        'data_roti' : roti,
        'nama_toko' :'Toko '+nama_toko,
        'temp'  : temp,
        'hasil' : data_dropping,
    }
    return render(request, 'distribusi_user.html', konteks)

@login_required(login_url='login')
@admin_only
def jadwal(request):
    data_jadwal = jadwal_kunjungan.objects.all()
    konteks={
        'data_jadwal' : data_jadwal
    }
    return render(request, 'jadwal.html',konteks)

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
def hapus_jadwal(request, id_jadwal):
    Jadwal = jadwal_kunjungan.objects.filter(id=id_jadwal)
    Jadwal.delete()
    messages.success(request,"Data Berhasil Dihapus")
    return redirect('data-jadwal-kunjungan')

@login_required(login_url='login')
@admin_only
def roti(request):
    data_roti = dataroti.objects.all()
    konteks={
        'data_roti' : data_roti
    }
    return render(request, 'dataroti.html',konteks)

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@admin_only
def hapus_roti(request, kode):
    roti = dataroti.objects.filter(kode=kode)
    roti.delete()
    messages.success(request,"Data Berhasil Dihapus")
    return redirect('data-roti')

# @unauthenticated_user
# def register(request):
#     form = CreateUserForm()
#     if request.POST:
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             group = Group.objects.get(name='sales')
#             user.groups.add(group)
#             messages.success(request, 'akun '+username+' berhasil ditambahkan')
#             return redirect('login')
#     konteks = {
#         'form': form,
#     }
#     return render(request, 'registration/register.html', konteks)

@unauthenticated_user 
def login_page(request):
    if request.method == 'POST':
        nik = request.POST['nik']
        password = request.POST['password']
        user = authenticate(request, nik=nik, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'username atau password salah')
            return redirect('login')
    conteks = {}
    return render(request, 'registration/login.html', conteks)

def Logout_page(request):
    logout(request)
    return redirect('login')
