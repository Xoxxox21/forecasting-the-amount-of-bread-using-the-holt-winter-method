from unicodedata import name
from wsgiref.handlers import format_date_time
from django.db import models
            
class datatoko(models.Model):
    PnD= 'P&D'
    WARUNG_REorNOO = 'WARUNG RE/NOO'
    MTI_REorNOO = 'MTI RE/NOO'
    toko = [
        (PnD,'P&D'),
        (WARUNG_REorNOO,'WARUNG RE/NOO'),
        (MTI_REorNOO,'MTI RE/NOO'),
    ]
    kode = models.CharField(primary_key=True, max_length=5)
    nama = models.CharField(max_length=50)
    pemilik = models.CharField(max_length=50)
    no_hp = models.CharField(max_length=13)
    Email = models.CharField(max_length=50)
    alamat = models.TextField()
    Jenis_toko = models.CharField(max_length=13, choices=toko, default=PnD)
    bank_name = models.CharField(max_length=100)
    bank_akun_name = models.CharField(max_length=50)
    npwp_no = models.CharField(max_length=15)
    name_npwp = models.CharField(max_length=50)
    provinsi = models.CharField(max_length=50)
    kabupaten_kota = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longtitude = models.CharField(max_length=50)
    def __str__(self):
        return self.nama

class datasales (models.Model):
    LAKILAKI = 'laki-laki'
    perempuan = 'perempuan'
    MENIKAH='menikah'
    BELUMMENIKAH='belum menikah'
    ML = 'ML'
    MR = 'MR'
    jk = [
        (LAKILAKI,'laki-laki'),
        (perempuan,'perempuan'),
    ]
    pilih_status = [
        (MENIKAH,'menikah'),
        (BELUMMENIKAH,'belum menikah'),
    ]
    pilih_sales_type = [
        (ML,'MOBIL'),
        (MR,'MOTOR')    
    ]
    nik = models.CharField(primary_key=True, max_length=15)
    nama = models.CharField(max_length=50)
    alamat = models.TextField()
    no_hp = models.CharField(max_length=13)
    Email = models.CharField(max_length=50)
    jenis_kelamin = models.CharField(
        max_length=10,
        choices=jk,
        default=LAKILAKI
    )
    status = models.CharField(
        max_length=13,
        choices=pilih_status,
        default=MENIKAH
    )
    sales_type = models.CharField(
        max_length=10,
        choices=pilih_sales_type,
        default=ML
    )
    tanggal_mulai = models.DateField()
    tanggal_berakhir = models.DateField()
    def __str__(self):
        return self.nama
    

class dataroti (models.Model):
    kode = models.CharField(primary_key=True, max_length=100)
    nama = models.CharField(max_length=100)
    harga = models.CharField(max_length=100)
    def __str__(self):
        return self.kode

class datadistribusi (models.Model):
    tanggal = models.DateField()
    toko_id = models.ForeignKey(
        datatoko, 
        on_delete=models.CASCADE
    )
    roti_id = models.ForeignKey(
        dataroti,
        on_delete=models.CASCADE
    )
    dropping = models.IntegerField()
    roti_sisa = models.IntegerField(blank=True, null=True)

class jadwal_kunjungan(models.Model):
    sales_id = models.ForeignKey(
        datasales,
        on_delete=models.CASCADE
    )
    toko_id = models.ForeignKey(
        datatoko,
        on_delete=models.CASCADE
    )   
    hari = models.CharField(max_length=100)
    def __str__(self):
        return self.hari
