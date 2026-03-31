import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa as rsa_keygen

def generate_rsa_keypair(key_size=2048):
    private_key = rsa_keygen.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    pn = private_key.private_numbers()
    return pn.public_numbers.e, pn.d, pn.public_numbers.n

def aes_ctr_encrypt(key: bytes, nonce: bytes, plaintext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def aes_ctr_decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

def rsa_based_encrypt(plaintext: bytes, e: int, n: int):
    ell = 32 
    n_byte_len = (n.bit_length() + 7) // 8

    r = int.from_bytes(os.urandom(n_byte_len), 'big') % n

    c0 = pow(r, e, n)

    r_bytes = r.to_bytes(n_byte_len, 'big')

    cipher_blocks = []
    num_blocks = (len(plaintext) + ell - 1) // ell

    for block_index in range(num_blocks):
        start = block_index * ell
        block = plaintext[start: start + ell]
        if len(block) < ell:
            block = block + b'\x00' * (ell - len(block))

        h_i = hashlib.sha256(block_index.to_bytes(4, 'big') + r_bytes).digest()

        c_i = bytes(a ^ b for a, b in zip(block, h_i))
        cipher_blocks.append(c_i)

    return c0, b"".join(cipher_blocks), len(plaintext)


def rsa_based_decrypt(c0: int, cipher_data: bytes, original_len: int, d: int, n: int) -> bytes:
    ell = 32
    n_byte_len = (n.bit_length() + 7) // 8

    r = pow(c0, d, n)
    r_bytes = r.to_bytes(n_byte_len, 'big')

    plain_blocks = []
    num_blocks = len(cipher_data) // ell

    for block_index in range(num_blocks):
        start = block_index * ell
        c_i = cipher_data[start: start + ell]

        h_i = hashlib.sha256(block_index.to_bytes(4, 'big') + r_bytes).digest()

        p_i = bytes(a ^ b for a, b in zip(c_i, h_i))
        plain_blocks.append(p_i)

    return b"".join(plain_blocks)[:original_len]


def sha256_hash(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()
