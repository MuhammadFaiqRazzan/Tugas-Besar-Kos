import json
import os
import bcrypt

def load_admins(file_path='admins.json'):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return [json.loads(line) for line in f]
        except json.JSONDecodeError:
            return []
    return []

def save_admin(username, password, file_path='admins.json'):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_admin = {'username': username, 'password': hashed_password.decode()}

    try:
        with open(file_path, 'a') as f:
            json.dump(new_admin, f)
            f.write('\n')
        return True
    except Exception as e:
        return False, f"Gagal menyimpan admin: {e}"

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
    with open(file_path, 'w') as f :
        json.dump(data, f, indent=4)

def get_kos_by_id(data, kos_id) :
    return next((k for k in data['kos'] if ['id'] == kos_id), None)       
        
def tambah_pesanan(data, pesanan_data):
    if 'pemesanan' not in data:
        data['pemesanan'] = []
        data['pemesanan'].append(pesanan_data)
        return data