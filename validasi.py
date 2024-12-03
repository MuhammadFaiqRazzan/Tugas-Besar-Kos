import bcrypt
import json

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

    if not data['harga'].isdigit() or int(data['harga']) <= 0:
        return False, "Harga harus berupa angka positif!"

    if not data['rekening'].isdigit() or len(data['rekening']) < 10:
        return False, "Nomor rekening harus berupa angka dengan minimal 10 digit!"

    if not data['gambar'].lower().endswith(('.png', '.jpg', '.jpeg')):
        return False, "Format gambar harus PNG, JPG, atau JPEG!"

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