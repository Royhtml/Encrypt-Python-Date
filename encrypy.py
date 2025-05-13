from cryptography.fernet import Fernet
import subprocess
import os
import sys

# 1. Generate encryption key
key = Fernet.generate_key()
cipher = Fernet(key)

# 2. Encrypt the target Python file
target_script = "mainpp.py"  # Ganti dengan file Python Anda

# Baca file dengan encoding UTF-8
with open(target_script, 'rb') as f:
    file_content = f.read()

# Jika file mengandung BOM (Byte Order Mark), kita bisa menghapusnya
if file_content.startswith(b'\xef\xbb\xbf'):
    file_content = file_content[3:]

encrypted_data = cipher.encrypt(file_content)

# 3. Create loader script
loader_script = f'''
from cryptography.fernet import Fernet
import sys
import os
import tempfile

key = {key!r}
cipher = Fernet(key)

encrypted_data = {encrypted_data!r}

# Decrypt in memory
try:
    decrypted_code = cipher.decrypt(encrypted_data).decode('utf-8')
    # Execute decrypted code
    exec(decrypted_code)
except Exception as e:
    print(f"Error: {{e}}")
    input("Press Enter to exit...")
'''

# 4. Save loader script
with open('contoh_loader.py', 'w', encoding='utf-8') as f:
    f.write(loader_script)

# 5. Compile to binary
print("Compiling to binary...")
try:
    subprocess.run([
        'pyinstaller',
        '--onefile',
        '--windowed',
        'mainpp.py'
    ], check=True)
    
    print(f"Binary created in dist/protected_loader.exe")
    print("Don't forget to delete the profesional mainpp.py after compilation!")
except subprocess.CalledProcessError as e:
    print(f"Compilation failed: {e}")