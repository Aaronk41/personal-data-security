def encrypt_caesar(plaintext, shift):
    encrypted = ""
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted += chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted += char
    return encrypted

def decrypt_caesar(ciphertext, shift):
    return encrypt_caesar(ciphertext, -shift)

if __name__ == "__main__":
    message = input("Enter a message to encrypt: ")
    shift = int(input("Enter shift value (1-25): "))

    encrypted = encrypt_caesar(message, shift)
    print("\nEncrypted:", encrypted)

    decrypted = decrypt_caesar(encrypted, shift)
    print("Decrypted:", decrypted)
