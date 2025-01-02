import bcrypt
import json
import os
from datetime import datetime, timedelta
import calendar

def validasi_login(username, password):
    try:
        with open('admins.json', 'r') as admin_file:
            admins = [json.loads(line) for line in admin_file]
            for admin in admins:
                if admin['username'] == username and bcrypt.checkpw(password.encode(), admin['password'].encode()):
                    return True, "Login berhasil!"
        return False, "Username atau password salah!"
    except FileNotFoundError:
        return False, "Belum ada akun yang terdaftar!"

def simpan_admin(username, password):
    if not username or not password:
        return False, "Username dan password harus diisi!"

    try:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with open('admins.json', 'a') as admin_file:
            json.dump({'username': username, 'password': hashed_password.decode()}, admin_file)
            admin_file.write('\n')
        return True, "Admin berhasil didaftarkan!"
    except Exception as e:
        return False, f"Terjadi kesalahan: {e}"

def validasi_input(data):
    if not all(data.values()):
        return False, "Harap isi semua data!"

    if 'harga' not in data or not str(data['harga']).isdigit() or int(data['harga']) <= 0:
        return False, "Harga harus berupa angka positif!"

    if 'rekening' not in data or not data['rekening'].isdigit() or len(data['rekening']) < 10:
        return False, "Nomor rekening harus berupa angka dengan minimal 10 digit!"

    # Validasi gambar menggunakan fungsi validasi_gambar
    if 'gambar' in data:
        is_valid, message = validasi_gambar(data['gambar'])
        if not is_valid:
            return False, message

    return True, "Data valid"

def tambah_kos(data, kos_data):
    # Periksa apakah nama kos sudah ada
    existing_kos = next((k for k in data['kos'] if k['nama_kos'] == kos_data['nama_kos']), None)
    if existing_kos:
        # Tambahkan kamar ke kos yang ada
        existing_kos['kamar'].extend(kos_data['kamar'])
    else:
        # Tambahkan kos baru jika belum ada
        data['kos'].append(kos_data)
    return data

def buat_pesanan(data, data_pesanan):
    
    kos = next((k for k in data['kos'] if k['id'] == data_pesanan['kos_id']), None)
    if kos:
        kamar = next((k for k in kos['kamar'] if k['nomor'] == data_pesanan['kamar_nomor']), None)
        if kamar and kamar['status'] == 'Tersedia':
            durasi_bulan = data_pesanan.get('durasi', 1)
            now = datetime.now()

            # Hitung bulan awal dan akhir
            bulan_awal = now.month
            tahun_awal = now.year
            bulan_akhir = (bulan_awal + durasi_bulan - 1) % 12 or 12
            tahun_akhir = tahun_awal + (bulan_awal + durasi_bulan - 1) // 12

            # Format status dengan nama bulan
            nama_bulan_awal = calendar.month_name[bulan_awal]
            nama_bulan_akhir = calendar.month_name[bulan_akhir]
            masa_berlaku = datetime(tahun_akhir, bulan_akhir, 1)
            data_pesanan['masa_berlaku'] = masa_berlaku.strftime("%Y-%m-%d")
            data_pesanan['status'] = 'Aktif'

            kamar['status'] = f"Disewa {nama_bulan_awal} - {nama_bulan_akhir} {tahun_akhir}"

            # Tambahkan pesanan ke data
            if 'pemesanan' not in data:
                data['pemesanan'] = []
            data['pemesanan'].append(data_pesanan)
            return data, "Pesanan berhasil dibuat."
        else:
            return data, "Kamar tidak tersedia."
    return data, "Kos tidak ditemukan."

def validasi_pembayaran(nominal, rekening_input, kos_data):
    try:
        nominal = int(nominal)
    except ValueError:
        return False, "Nominal harus berupa angka!"
    
    if rekening_input != kos_data['rekening']:
        return False, "Rekening tujuan tidak sesuai!"
    
    total_harga = int(kos_data['harga'])
    if nominal < total_harga:
        return False, f"Nominal pembayaran kurang! Harus sebesar {total_harga}."
    
    return True, 

def validasi_gambar(path_gambar):
    if not os.path.isfile(path_gambar):
        return False, "Gambar tidak ditemukan di sistem!"
    if not path_gambar.lower().endswith(('.png', '.jpg', '.jpeg')):
        return False, "Format gambar harus PNG, JPG, atau JPEG!"
    return True, "Gambar valid"

def validasi_input(data):
    
    if not all(data.values()):  # Memastikan semua kolom terisi
        return False, "Harap isi semua data!"

    try:
        harga = int(data.get('harga', 0))
        if harga <= 0:  # Harga tidak boleh nol atau negatif
            return False, "Harga harus lebih besar dari 0!"
    except ValueError:
        return False, "Harga harus berupa angka!"
    
    # Validasi nomor rekening
    if not data.get('rekening', '').isdigit() or len(data['rekening']) < 10:
        return False, "Nomor rekening harus berupa angka dengan minimal 10 digit!"
    
    # Validasi gambar
    if 'gambar' in data:
        is_valid, message = validasi_gambar(data['gambar'])
        if not is_valid:
            return False, message
    
    return True, "Data valid"

def validasi_login_pemesan(username, password):
    try:
        with open('pemesan.json', 'r') as pemesan_file:
            pemesans = [json.loads(line) for line in pemesan_file]
            for pemesan in pemesans:
                if pemesan['username'] == username and bcrypt.checkpw(password.encode(), pemesan['password'].encode()):
                    return True, pemesan  # Return data pemesan jika login berhasil
        return False, "Username atau password salah!"
    except FileNotFoundError:
        return False, "Belum ada akun pemesan yang terdaftar!"
    
def simpan_admin(username, password):
    if not username or not password:
        return False, "Username dan password harus diisi!"

    try:
        # Periksa apakah username sudah ada
        if os.path.exists('admins.json'):
            with open('admins.json', 'r') as admin_file:
                admins = [json.loads(line) for line in admin_file]
                if any(admin['username'] == username for admin in admins):
                    return False, "Username sudah terdaftar!"

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with open('admins.json', 'a') as admin_file:
            json.dump({'username': username, 'password': hashed_password.decode()}, admin_file)
            admin_file.write('\n')
        return True, "Admin berhasil didaftarkan!"
    except Exception as e:
        return False, f"Terjadi kesalahan: {e}"

def validasi_durasi(durasi):
    
    try:
        durasi = int(durasi)
        if durasi <= 0:
            return False, "Durasi pemesanan harus berupa angka positif!"
        return True, ""
    except ValueError:
        return False, "Durasi pemesanan harus berupa angka!"
    
def validasi_nominal(jumlah_uang, total_harga):
   
    try:
        jumlah_uang = int(jumlah_uang)
        if jumlah_uang < total_harga:
            return False, f"Jumlah uang yang dibayarkan kurang! Minimal: Rp {total_harga:,}"
        return True, ""
    except ValueError:
        return False, "Jumlah uang harus berupa angka!"

def validasi_bukti_transfer(file_path):
  
    if not os.path.isfile(file_path):
        return False, "Bukti transfer tidak ditemukan!"
    if not file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        return False, "Bukti transfer harus berupa file gambar (JPG, JPEG, PNG)!"
    return True, ""

