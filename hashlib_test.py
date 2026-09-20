import hashlib
string="ni hao"
sha=hashlib.sha256(string.encode())
result_hex=sha.hexdigest()
sha2=hashlib.sha256()
sha2.update(b"ni ")
sha2.update(b"hao")
print(sha2.hexdigest(),"\n",result_hex)

