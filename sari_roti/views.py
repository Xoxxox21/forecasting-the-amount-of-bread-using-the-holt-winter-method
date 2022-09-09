import csv
import datetime
import io
from django.shortcuts import redirect, render
from matplotlib import pyplot as plt
import pandas as pd
from sari_roti.decorators import admin_only, allowed_users, unauthenticated_user
from .models import *
from .form import *
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from statsmodels.tsa.api import ExponentialSmoothing
from django.contrib.auth.models import Group, User
from sklearn.metrics import mean_absolute_percentage_error
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required(login_url="login")
def PasswordsChangeView(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('ganti-password')
        else:
            messages.error(request, 'Please correct the error below.')
    return render(request, 'registration/change_pass.html', {'form': form,})


@login_required(login_url="login")
@admin_only
def index(request):
    data_sales = datasales.objects.all()[:10]
    data_toko = datatoko.objects.all()[:10]
    data_jadwal = jadwal_kunjungan.objects.all()[:10]
    data_roti = dataroti.objects.all()[:10]
    total_sales = len(datasales.objects.all())
    total_toko = len(datatoko.objects.all())
    total_roti = len(dataroti.objects.all())
    konteks = {
        "data_sales": data_sales,
        "data_toko": data_toko,
        "data_jadwal": data_jadwal,
        "data_roti": data_roti,
        "total_sales": total_sales,
        "total_toko": total_toko,
        "total_roti": total_roti,
    }
    return render(request, "index.html", konteks)


@login_required(login_url="login")
@admin_only
def sales(request):
    data_sales = datasales.objects.all()
    konteks = {
        "data_sales": data_sales,
    }
    return render(request, "datasales.html", konteks)


@login_required(login_url="login")
@admin_only
def tambahsales(request):
    form = FormtambahSales()
    if request.POST:
        form = FormtambahSales(request.POST)
        if form.is_valid():
            form.save()

            # membuat user
            nik = form.cleaned_data["nik"]
            user = User.objects.create_user(
                username=form.cleaned_data["nik"],
                email=form.cleaned_data["Email"],
                first_name=form.cleaned_data["nama"],
                
            )
            user.set_password(nik)
            # print(user)
            user.save()
            # membuat group
            group = Group.objects.get(name="sales")
            user.groups.add(group)
            pesan = "Data berhasil ditambahkan"
        else:
            pesan = "Data yang dimasukkan tidak valid"
        form = FormtambahSales()
        konteks = {
            "form": form,
            "pesan": pesan,
        }
        return render(request, "tambahsales.html", konteks)
    else:
        konteks = {
            "form": form,
        }
        return render(request, "tambahsales.html", konteks)

@login_required(login_url="login")
@admin_only
def updatesales(request, nik_sales):
    Sales = datasales.objects.get(nik=nik_sales)
    template = "updatesales.html"
    if request.POST:
        form = FormtambahSales(request.POST, instance=Sales)
        if form.is_valid():
            form.save()
            messages.success(request, "Data berhasil diubah")
            return redirect("update-sales", nik_sales=nik_sales)
    else:
        form = FormtambahSales(instance=Sales)
        konteks = {
            "form": form,
            "sales": Sales,
        }
    return render(request, template, konteks)


@login_required(login_url="login")
@admin_only
def hapus_sales(request, nik_sales):
    Sales = datasales.objects.filter(nik=nik_sales)
    Sales.delete()
    user = User.objects.filter(username=nik_sales)
    user.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect("data-sales")


@login_required(login_url="login")
@admin_only
def toko(request):
    data_toko = datatoko.objects.all()
    konteks = {
        "data_toko": data_toko,
    }
    return render(request, "datatoko.html", konteks)


@login_required(login_url="login")
@admin_only
def tambahtoko(request):
    if request.POST:
        form = Formtoko(request.POST)
        if form.is_valid():
            form.save()
            pesan = "Data berhasil ditambahkan"
        else:
            pesan = "Data yang dimasukkan tidak valid"
        form = Formtoko()
        konteks = {
            "form": form,
            "pesan": pesan,
        }
        return render(request, "tambahtoko.html", konteks)
    else:
        form = Formtoko()
        konteks = {
            "form": form,
        }
        return render(request, "tambahtoko.html", konteks)

@login_required(login_url="login")
@admin_only
def updatetoko(request, kode):
    Toko = datatoko.objects.get(kode=kode)
    template = "updatetoko.html"
    if request.POST:
        form = Formtoko(request.POST, instance=Toko)
        if form.is_valid():
            form.save()
            messages.success(request, "Data berhasil diubah")
            return redirect("update-toko", kode=kode)
    else:
        form = Formtoko(instance=Toko)
        konteks = {
            "form": form,
            "toko": Toko,
        }
    return render(request, template, konteks)


@login_required(login_url="login")
@admin_only
def hapus_toko(request, kode):
    Toko = datatoko.objects.filter(kode=kode)
    Toko.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect("data-toko")


@login_required(login_url="login")
@admin_only
def distribusi(request):
    data_toko = datatoko.objects.all()
    data_roti = dataroti.objects.all()
    temp = []
    kosong = False
    konteks = {
        "data_toko": data_toko,
        "data_roti": data_roti,
        "temp": temp,
        "nama_toko": "Silahkan Pilih Toko",
        "kosong" : kosong
    }
    return render(request, "distribusi.html", konteks)


@login_required(login_url="login")
@admin_only
def isi_sisa(request, id_distribusi):
    distribusi = datadistribusi.objects.get(id=id_distribusi)
    template = "isi_sisa.html"
    if request.POST:
        form = formdistribusi(request.POST, instance=distribusi)
        if form.is_valid():
            jumlah = jumlahdistribusiperhari.objects.get(tanggal = distribusi.tanggal, toko_id = distribusi.toko_id)
            jumlah.jumlah_sisa = int(jumlah.jumlah_sisa) + int(form.cleaned_data["roti_sisa"])
            jumlah.save()
            form.save()
            messages.success(request, "Data berhasil diubah")
            return redirect("isi-sisa", id_distribusi=id_distribusi)
    else:
        form = formdistribusi(instance=distribusi)
        konteks = {
            "form": form,
            "distribusi": distribusi,
        }
    return render(request, template, konteks)


@login_required(login_url="login")
@admin_only
def DistribusiPerToko(request, kode):
    data_distribusi = datadistribusi.objects.filter(toko_id=kode)
    data_toko = datatoko.objects.all()
    data_roti = dataroti.objects.all()
    temp = []
    roti = []
    kosong = False
    hari = datetime.date.today()
    total = jumlahdistribusiperhari.objects.filter(toko_id=kode)
    
    #looping untuk mengambil data nama dari data toko
    for toko in data_toko:
        if toko.kode == kode:
            nama_toko = toko.nama
            kode_toko = toko.kode
    
    # looping untuk mengambil data tanggal dari datadistribusi yang dimasukkan kedalam kedalam temp agar ketika ditampilkan tidak sama
    if len(data_distribusi) == 0 or len(data_distribusi.filter(tanggal=hari)) != len(data_roti):
        kosong = True
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
    else:
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
        for date in range(len(temp)):
            if jumlahdistribusiperhari.objects.filter(tanggal=temp[date],toko_id=data_toko.get(kode=kode)).exists():
                continue
            else:        
                jumlah_drop = 0
                jumlah_sisa = 0
                for y in range(len(roti)):
                    hasil = data_distribusi.filter(tanggal = temp[date], roti_id = roti[y])
                    for has in hasil:
                        jumlah_drop += has.dropping
                        if has.roti_sisa is None:
                            jumlah_sisa += 0
                        else:
                            jumlah_sisa += has.roti_sisa
                jumlahdistribusiperhari.objects.create(tanggal = temp[date],toko_id=data_toko.get(kode=kode),jumlah_drop=jumlah_drop,jumlah_sisa=jumlah_sisa)
        
    konteks = {
        "data_distribusi": data_distribusi,
        "data_toko": data_toko,
        "kode_toko": kode_toko,
        "data_roti": roti,
        "nama_toko": "Toko " + nama_toko,
        "temp": temp,
        "kosong": kosong,
        "total": total
    }
    return render(request, "distribusi.html", konteks)

@login_required(login_url="login")
@admin_only
def droping(request):
    # toko = datatoko.objects.get(kode=kode)
    if request.POST:
        form = formdistribusi(request.POST)
        if form.is_valid():
            form.save()
            pesan = "Data berhasil ditambahkan"
        else:
            pesan = "Data yang dimasukkan tidak valid"
        form = formdistribusi()
        konteks = {
            "form": form,
            "pesan": pesan,
        }
        return render(request, "droping.html", konteks)
    else:
        form = formdistribusi()
        konteks = {
            "form": form,
        }
        return render(request, "droping.html", konteks)


@login_required(login_url="login")
@allowed_users(allowed_roles=["sales"])
def DistribusiUser(request):
    data_toko = datatoko.objects.all()
    konteks = {"data_toko": data_toko, "nama_toko": "Silahkan Pilih Toko"}
    return render(request, "distribusi_user.html", konteks)


@login_required(login_url="login")
@allowed_users(allowed_roles=["sales"])
def DistribusiUserToko(request, kode):
    data_distribusi = datadistribusi.objects.filter(toko_id=kode)
    data_toko = datatoko.objects.all()
    data_kunjungan = jadwal_kunjungan.objects.filter(toko_id=kode, sales_id=request.user.username)
    data_roti = dataroti.objects.all()
    data_dropping = {}
    tanggal = []
    droping = []
    temp = []
    roti = []
    hari = datetime.date.today()
    
    # looping untuk mengambil data nama dari data toko
    for toko in data_toko:
        if toko.kode == kode:
            nama_toko = toko.nama
            kode_toko = toko.kode
    ada = False
    for kunjungan in data_kunjungan:
        if kunjungan.hari == hari.strftime("%A"): #mengecek hari jadwal kunjungan yang sama dengan hari ini
            ada = True
            udah_masuk_data = False
            for data_ in data_distribusi:
                if data_.tanggal == hari:
                    udah_masuk_data = True
                IsMatch = False
                # ambil data roti sesuai dengan yang didata distribusi
                for i in range(len(roti)):
                    if roti[i] == data_.roti_id and temp[i] == data_.tanggal:
                        IsMatch = True
                if IsMatch:
                    continue
                else:
                    roti.append(data_.roti_id)
                    temp.append(data_.tanggal)
            if udah_masuk_data == True:
                data_distribusi = datadistribusi.objects.filter(toko_id=kode, tanggal=hari)
                break
            elif len(data_distribusi) >= len(data_roti):
                drop = 0
                periode = len(data_kunjungan)*4
                day = hari.day
                for i in range(periode):
                    for i in range(len(roti)):
                        ada_roti = 0
                        data_dropping[str(roti[i])] = {
                            "tanggal": [],
                            "dropping": [],
                        }
                        for data in data_distribusi:
                            if data.roti_id == roti[i]:
                                tanggal.append(data.tanggal)
                                droping.append(data.dropping)
                                ada_roti=+1
                        if ada_roti == 0:
                            hasil = 0
                            continue
                        else:
                            data_dropping[str(roti[i])]["tanggal"] = tanggal
                            data_dropping[str(roti[i])]["dropping"] = droping
                            tanggal = []
                            droping = []
                            df = pd.DataFrame(data_dropping[str(roti[i])])
                            df.set_index("tanggal", inplace=True)
                            df = df.fillna(method="ffill")
                            # model = ExponentialSmoothing(df["dropping"], trend = "add", seasonal = "add", seasonal_periods = periode).fit()
                            # df_train = df[:100]
                            df_test = df[140:]
                            # model_train = ExponentialSmoothing(df_train["dropping"], trend = "add", seasonal = "add", seasonal_periods = periode).fit()
                            model_test = ExponentialSmoothing(df_test["dropping"], trend = "add", seasonal = "add", seasonal_periods = periode).fit()
                            predik_test = model_test.forecast(steps = 1)
                            # mape = mean_absolute_percentage_error(df_test["dropping"], predik_test)
                            # print(roti[i])
                            # alpha = model.params['smoothing_level']
                            # beta = model.params['smoothing_trend']
                            # gamma = model.params['smoothing_seasonal']
                            # level = model.params['initial_level']
                            # trend = model.params['initial_trend']
                            # seasonal = model.params['initial_seasons']
                            # print("Alpha adalah "+str(alpha))
                            # print("beta adalah "+str(beta))
                            # print("gamma adalah "+str(gamma))
                            # print("initial level adalah "+str(level))
                            # print("initial trend adalah "+str(trend))
                            # print("initial seasonal adalah "+str(seasonal))
                            # print("mape adalah "+str(mape))
                            # predik = model.forecast(steps = 1)
                            hasil = round(predik_test)
                        if datadistribusi.objects.filter(toko_id=kode, roti_id=roti[i], tanggal=hari).exists():
                            continue
                        else:
                            drop = drop + int(hasil)
                            datadistribusi.objects.create(toko_id=data_toko.get(kode=kode), tanggal=hari, roti_id=roti[i], dropping=hasil)
                    jumlahdistribusiperhari.objects.create(tanggal = hari,toko_id=data_toko.get(kode=kode),jumlah_drop=drop,jumlah_sisa=0)
                    drop = 0
                    day = hari.day+3
                    hari = datetime.date(2022,8,day)
                hari = datetime.date.today()
                data_distribusi = datadistribusi.objects.filter(toko_id=kode, tanggal=hari)
                break
        else:
            continue
    konteks = {
        "data_distribusi": data_distribusi,
        "data_toko": data_toko,
        "data_roti": roti,
        "nama_toko": "Toko " + nama_toko,
        "kode_toko": kode_toko,
        "temp": temp,
        "ada": ada,
        "date": hari,
        "jumlah": jumlahdistribusiperhari.objects.filter(tanggal = hari,toko_id=data_toko.get(kode=kode)),
    }
    return render(request, "distribusi_user.html", konteks)


@login_required(login_url="login")
@admin_only
def jadwal(request):
    data_jadwal = jadwal_kunjungan.objects.all()
    konteks = {"data_jadwal": data_jadwal}
    return render(request, "jadwal.html", konteks)


@login_required(login_url="login")
@admin_only
def tambahjadwal(request):
    if request.POST:
        form = form_jadwal_kunjungan(request.POST)
        if form.is_valid():
            form.save()
            pesan = "Data berhasil ditambahkan"
        else:
            pesan = "Data yang dimasukkan tidak valid"
        form = form_jadwal_kunjungan()
        konteks = {
            "form": form,
            "pesan": pesan,
        }
        return render(request, "tambahjadwal.html", konteks)
    else:
        form = form_jadwal_kunjungan()
        konteks = {
            "form": form,
        }
        return render(request, "tambahjadwal.html", konteks)

@login_required(login_url="login")
@admin_only
def updatejadwal(request, id_jadwal):
    Jadwal = jadwal_kunjungan.objects.get(id=id_jadwal)
    template = "updatejadwal.html"
    if request.POST:
        form = form_jadwal_kunjungan(request.POST, instance=Jadwal)
        if form.is_valid():
            form.save()
            messages.success(request, "Data berhasil diubah")
            return redirect("update-jadwal", id_jadwal=id_jadwal)
    else:
        form = form_jadwal_kunjungan(instance=Jadwal)
        konteks = {
            "form": form,
            "jadwal": Jadwal,
        }
    return render(request, template, konteks)


@login_required(login_url="login")
@admin_only
def hapus_jadwal(request, id_jadwal):
    Jadwal = jadwal_kunjungan.objects.filter(id=id_jadwal)
    Jadwal.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect("data-jadwal-kunjungan")


@login_required(login_url="login")
@admin_only
def roti(request):
    data_roti = dataroti.objects.all()
    konteks = {"data_roti": data_roti}
    return render(request, "dataroti.html", konteks)


@login_required(login_url="login")
@admin_only
def tambahroti(request):
    if request.POST:
        form = form_roti(request.POST)
        if form.is_valid():
            form.save()
            pesan = "Data berhasil ditambahkan"
        else:
            pesan = "Data yang dimasukkan tidak valid"
        form = form_roti()
        konteks = {
            "form": form,
            "pesan": pesan,
        }
        return render(request, "tambahroti.html", konteks)
    else:
        form = form_roti()
        konteks = {
            "form": form,
        }
        return render(request, "tambahroti.html", konteks)


@login_required(login_url="login")
@admin_only
def updateroti(request, kode):
    roti = dataroti.objects.get(kode=kode)
    template = "updateroti.html"
    if request.POST:
        form = form_roti(request.POST, instance=roti)
        if form.is_valid():
            form.save()
            messages.success(request, "Data berhasil diubah")
            return redirect("update-roti", kode=kode)
    else:
        form = form_roti(instance=roti)
        konteks = {
            "form": form,
            "roti": roti,
        }
    return render(request, template, konteks)


@login_required(login_url="login")
@admin_only
def hapus_roti(request, kode):
    roti = dataroti.objects.filter(kode=kode)
    roti.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect("data-roti")


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "username atau password salah")
            return redirect("login")
    return render(request, "registration/login.html")


def Logout_page(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def pdf(request, kode, tanggal):
    data_distribusi = datadistribusi.objects.filter(toko_id=kode, tanggal=tanggal)
    template_path = 'pdfreport.html'
    context = {
        'data_distribusi': data_distribusi, 
        'tanggal': tanggal, 
        'kode': data_distribusi[0].toko_id.nama, 
        "jumlah": jumlahdistribusiperhari.objects.filter(
            tanggal = tanggal,
            toko_id=datatoko.objects.get(kode=kode))}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url="login")
@admin_only
def distribusi_upload(request):
    # declaring template
    template = "distribusi.html"
    data = datadistribusi.objects.all()
# prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, email, address,    phone, profile',
        'profiles': data    
    }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = datadistribusi.objects.update_or_create(
            tanggal = column[0],
            toko_id = datatoko.objects.get(kode=column[1]),
            roti_id = dataroti.objects.get(kode=column[2]),
            dropping = column[3],
            roti_sisa = column[4],
        )
    context = {}
    return redirect("data-distribusi")