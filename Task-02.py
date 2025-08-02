from PIL import Image
import numpy as np
import hashlib

#convert password to integer key
def generate_key_from_password(password: str) -> int:
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return int(hashed[:8], 16)  

def encrypt_image(input_path, output_path, password):
    key = generate_key_from_password(password) %256
    img = Image.open(input_path).convert('RGB')
    data = np.array(img)

    #swap
    swapped = data[..., [2, 1, 0]]  # B, G, R
    
    #xor
    encrypted_data = swapped ^ key

    encrypted_img = Image.fromarray(encrypted_data.astype('uint8'))
    encrypted_img.save(output_path)
    print("Image encrypted and saved as:", output_path)


def decrypt_image(input_path, output_path, password):
    key = generate_key_from_password(password) %256
    img = Image.open(input_path).convert('RGB')
    data = np.array(img)

    #reverse xor
    decrypted_xor = data ^ key

    #reverse swap
    unswapped = decrypted_xor[..., [2, 1, 0]]  # R, G, B

    decrypted_img = Image.fromarray(unswapped.astype('uint8'))
    decrypted_img.save(output_path)
    print("Image decrypted and saved as:", output_path)


if __name__ == "__main__":
    
    input_image = r"/home/kali/input.png"
    encrypted_image = r"/home/kali/encrypted.png"
    decrypted_image = r"/home/kali/decrypted.png"

    password = "mySecretPassword123"

    encrypt_image(input_image, encrypted_image, password)

    decrypt_image(encrypted_image, decrypted_image, password)
