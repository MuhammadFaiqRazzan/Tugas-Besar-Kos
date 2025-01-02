import json
import bcrypt
from datetime import datetime
import os

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Validasi atribut "harga" di setiap kos
                for kos in data.get('kos', []):
                    if 'harga' not in kos or not str(kos['harga']).isdigit():
                        kos['harga'] = "0"  # Fallback nilai default jika tidak valid
                return data
        except json.JSONDecodeError:
            return {'kos': [], 'pemesanan': []}
    else:
        return {'kos': [], 'pemesanan': []}

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_kos_by_id(data, kos_id):
    return next((k for k in data['kos'] if k['id'] == kos_id), None)

def get_kos_by_kategori(data, kategori):
    return [k for k in data['kos'] if k.get('kategori') == kategori]

def tambah_pesanan(data, pesanan_baru):
    
    if 'pemesanan' not in data:
        data['pemesanan'] = []
    data['pemesanan'].append(pesanan_baru)
    return data

def tambah_kos(data, kos_data):
    data['kos'].append(kos_data)
    return data

def update_kos_status(data, kos_id, status):
    kos = get_kos_by_id(data, kos_id)
    if kos:
        kos['status'] = status
        return data, "Status kos berhasil diperbarui."
    return data, "Kos tidak ditemukan."

def get_kos_by_owner(data, owner):
    return [kos for kos in data['kos'] if kos.get('owner') == owner]

def get_user_data(data, username):
    """Mengambil data pengguna berdasarkan username."""
    if 'users' not in data:
        data['users'] = {}
    return data['users'].get(username, {'kos': [], 'data_diri': {}})

def update_user_data(data, username, updated_user_data):
    """Memperbarui data pengguna."""
    if 'users' not in data:
        data['users'] = {}
    data['users'][username] = updated_user_data
    return data

def simpan_pemesan(username, password):
    
        if not username or not password:
            return False, "Username dan password harus diisi!"

        try:
            # Periksa apakah username sudah ada
            if os.path.exists('pemesan.json'):
                with open('pemesan.json', 'r') as pemesan_file:
                    pemesans = [json.loads(line) for line in pemesan_file]
                    if any(pemesan['username'] == username for pemesan in pemesans):
                        return False, "Username sudah terdaftar!"

            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_pemesan = {
                'username': username,
                'password': hashed_password.decode(),
                'pemesanan': []  # Kosongkan pemesanan saat pertama kali register
            }
            with open('pemesan.json', 'a') as pemesan_file:
                json.dump(new_pemesan, pemesan_file)
                pemesan_file.write('\n')
            return True, "Pemesan berhasil didaftarkan!"
        except Exception as e:
            return False, f"Terjadi kesalahan: {e}"

def update_kamar_status(data):
    
    now = datetime.now()
    for kos in data.get('kos', []):
        for kamar in kos.get('kamar', []):
            for pesanan in data.get('pemesanan', []):
                if pesanan['kos_id'] == kos['id'] and pesanan['kamar_nomor'] == kamar['nomor']:
                    masa_berlaku = datetime.strptime(pesanan['masa_berlaku'], "%Y-%m-%d")
                    if now > masa_berlaku:
                        kamar['status'] = "Tersedia"
                        pesanan['status'] = "Selesai"
    return data