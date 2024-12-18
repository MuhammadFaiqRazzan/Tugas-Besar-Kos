import bcrypt
import json
import os

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
    data['kos'].append(kos_data)
    return data

def buat_pesanan(data, data_pesanan):
    kos = next((k for k in data['kos'] if k['id'] == data_pesanan['kos_id']), None)
    if kos and kos['status'] == 'Tersedia':
        kos['status'] = 'Tidak Tersedia'
        data['pemesanan'].append(data_pesanan)
        return data, "Pesanan Berhasil"
    else:
        return data, "Kos tidak Tersedia!"
    
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
