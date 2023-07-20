import hashlib
def get_hashf(file_path):
    """Obtiene el hash SHA256 de un archivo."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()