import socket

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher = [(ord(char) ** e) % n for char in plaintext]
    return cipher

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65432))
    
    public_key_data = client_socket.recv(1024).decode()
    public_key = tuple(map(int, public_key_data.split(',')))
    
    while True:
        message = input("Enter message to send: ")
        encrypted_message = encrypt(public_key, message)
        client_socket.send(','.join(map(str, encrypted_message)).encode())
        
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received encrypted message: {data.decode()}")
        print()
    
    client_socket.close()

if __name__ == '__main__':
    client_program()
