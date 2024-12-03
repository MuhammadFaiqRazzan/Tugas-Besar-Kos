import json
import os
import bcrypt

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {'kos': [], 'pemesanan': []}
    else:
        return {'kos': [], 'pemesanan': []}

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_kos_by_id(data, kos_id):
    """Mencari kos berdasarkan ID."""
    return next((k for k in data['kos'] if k['id'] == kos_id), None)

def tambah_pesanan(data, pesanan_data):
    if 'pemesanan' not in data:
        data['pemesanan'] = []
    data['pemesanan'].append(pesanan_data)
    return data

def tambah_kos(data, kos_data):
    """Menambahkan data kos baru."""
    data['kos'].append(kos_data)
    return data
