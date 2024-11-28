import json
import os

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f :
            return json.load(f)
    else:
        return{
            'kos' : [],
            'pemesanan' : []
        }
        
def save_data(file_path, data):
    with open(file_path, 'w') as f :
        json.dump(data, f, indent=4)