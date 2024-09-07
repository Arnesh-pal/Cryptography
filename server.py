import socket

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1, x2, y1 = 0, 1, 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        
        x2, x1 = x1, x
        d, y1 = y1, y
    
    if temp_phi == 1:
        return d + phi

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be the same")
    
    n = p * q
    phi = (p-1) * (q-1)
    
    e = 65537
    g = gcd(e, phi)
    
    while g != 1:
        e += 2
        g = gcd(e, phi)
    
    d = multiplicative_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher = [(ord(char) ** e) % n for char in plaintext]
    return cipher
    
def decrypt(private_key, ciphertext):
    d, n = private_key
    plain = [chr((char ** d) % n) for char in ciphertext]
    return ''.join(plain)

def server_program():
    p = 61
    q = 53
    public_key, private_key = generate_keypair(p, q)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    print(f"Connection from: {address}")
    
    conn.send(f"{public_key[0]},{public_key[1]}".encode())
    
    while True:
        data = conn.recv(1024)
        if not data:
            break
        cipher_text = list(map(int, data.decode().split(',')))
        
        print(f"Received encrypted message: {cipher_text}")
        print()
        decrypted_message = decrypt(private_key, cipher_text)
        print(f"Decrypted message: {decrypted_message}")
        print()
        
        response = input("Enter message to send: ")
        print()
        encrypted_response = encrypt(public_key, response)
        conn.send(','.join(map(str, encrypted_response)).encode())
    
    conn.close()

if __name__ == '__main__':
    server_program()
