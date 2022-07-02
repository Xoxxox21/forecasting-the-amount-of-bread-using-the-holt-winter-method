from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView,LogoutView, PasswordChangeView, PasswordChangeDoneView
from sari_roti.views import *
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    
    path('data-sales/', sales, name='data-sales'),
    path('tambah-sales/', tambahsales, name='tambah-sales'),
    path('data-sales/ubah/<str:nik_sales>', updatesales, name='update-sales'),
    path('data-sales/hapus/<str:nik_sales>', hapus_sales, name='hapus-sales'),
    
    path('data-toko/', toko, name='data-toko'),
    path('tambah-toko/', tambahtoko, name='tambah-toko'),
    path('data-toko/ubah/<str:kode>', updatetoko, name='update-toko'),
    path('data-toko/hapus/<str:kode>', hapus_toko, name='hapus-toko'),
    
    path('data-distribusi/', distribusi, name='data-distribusi'),
    path('droping/', droping, name='droping'),
    path('data-distribusi/tambah/<int:id_distribusi>', isi_sisa, name='isi-sisa'),
    path('data-distribusi/<str:kode>/', DistribusiPerToko, name='distribusi-toko'),
    path('data-distribusi-user/', DistribusiUser, name='distribusi-user'),
    
    path('data-roti/', roti, name='data-roti'),
    path('tambah-roti/', tambahroti, name='tambah-roti'),
    path('data-roti/ubah/<str:kode>', updateroti, name='update-roti'),
    path('data-roti/hapus/<str:kode>', hapus_roti, name='hapus-roti'),
    
    path('data-jadwal/', jadwal, name='data-jadwal-kunjungan'),
    path('tambah-jadwal/', tambahjadwal, name='tambah-jadwal'),
    path('data-jadwal/ubah/<int:id_jadwal>', updatejadwal, name='update-jadwal'),
    path('data-jadwal/hapus/<int:id_jadwal>', hapus_jadwal, name='hapus-jadwal'),
    
    # path('login/', login_view, name='login_view'),    
    # path('keluar/', LogoutView.as_view(next_page='masuk'), name='keluar'),
    path('ganti-password/', PasswordChangeView.as_view(template_name='change_pass.html'), name='ganti-password'),
    path('ganti-password/done/', PasswordChangeDoneView.as_view(template_name='change_pass_done.html'),name='password_change_done'),
    
]
