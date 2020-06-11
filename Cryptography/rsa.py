try:
    input = raw_input
except NameError:
    pass
try:
    chr = unichr
except NameError:
    pass
print("Welcome to RSA Wizard")
print("Lets Encrypt...")
p = int(input('Enter first prime number (bigger than 5): '))
q = int(input('Enter second prime number(different than one you entered): '))
print("Chosen prime numbers:\np=" + str(p) + ", q=" + str(q) + "\n")
n = p * q
print("n = p * q = " + str(n) + "\n")
phi = (p - 1) * (q - 1)
print("Euler's function (totient) [phi(n)]: " + str(phi) + "\n")


def gcd(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a


def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def coprimes(a):
    l = []
    for x in range(2, a):
        if gcd(a, x) == 1 and modinv(x, phi) is not None:
            l.append(x)
    for x in l:
        if x == modinv(x, phi):
            l.remove(x)
    return l


print("Choose one from this array:\n")
print(str(coprimes(phi)) + "\n")
e = int(input())
d = modinv(e, phi)
print("\nYour public key is a pair of numbers (e=" + str(e) + ", n=" + str(n) + ").\n")
print("Your private key is a pair of numbers (d=" + str(d) + ", n=" + str(n) + ").\n")


def encrypt_block(m):
    c = modinv(m ** e, n)
    if c is None: print('No modular multiplicative inverse for block ' + str(m) + '.')
    return c


def decrypt_block(c):
    m = modinv(c ** d, n)
    if m is None: print('No modular multiplicative inverse for block ' + str(c) + '.')
    return m


def encrypt_string(s):
    return ''.join([chr(encrypt_block(ord(x))) for x in list(s)])


def decrypt_string(s):
    return ''.join([chr(decrypt_block(ord(x))) for x in list(s)])


s = input("Enter a message to encrypt: ")
print("\nPlain message: " + s + "\n")
enc = encrypt_string(s)
print("Encrypted message: " + enc + "\n")
dec = decrypt_string(enc)
print("Decrypted message: " + dec + "\n")
