import gnupg
import sqlite3

# Crea una instancia de GPG
gpg = gnupg.GPG()

# Crea un archivo sqlite para cifrar
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')
conn.commit()
conn.close()

# Leer el archivo sqlite
with open('test.db', 'rb') as f:
    file_data = f.read()

# Cifrar los datos
encrypted_data = gpg.encrypt(file_data, 'your-email@example.com')

# Escribe los datos cifrados en un nuevo archivo
with open('encrypted.gpg', 'wb') as f:
    f.write(str(encrypted_data).encode('utf-8'))

# Descifra los datos
with open('encrypted.gpg', 'rb') as f:
    encrypted_file_data = f.read()
    decrypted_data = gpg.decrypt(encrypted_file_data)

# Escribe los datos descifrados en un nuevo archivo
with open('decrypted.db', 'wb') as f:
    f.write(str(decrypted_data).encode('utf-8'))

