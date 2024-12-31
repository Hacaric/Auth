import hashlib as hlib
inp = input("Enter password >> ")
hashed_password = hlib.sha256(inp.encode("ascii")).hexdigest()
import urllib.request
page = urllib.request.urlopen('https://hacaric.github.io/Auth/')
print(page.read())
print(hashed_password)