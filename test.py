from werkzeug.security import generate_password_hash

print(generate_password_hash('saad',method='sha256'))
from hashlib import sha256
hs = sha256(('saad').encode('utf-8')).hexdigest()
print(hs)
