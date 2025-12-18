from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


def generate_assymetric_key():
    """
    Функия генерирует приватный и публичные ключи
    :return private_key, public_key: полученные ключи
    """
    keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048)

    private_key = keys
    public_key = keys.public_key()

    return private_key, public_key


def serialization_public_key(public_key, public_pem: str):
    """
    Записывает публичный в файл
    :param public_key: публичный ключ для записи
    :param public_pem: путь для записи
    """
    try:
        with open(public_pem, 'wb') as public_out:
            public_out.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo))
    except Exception as e:
        print(f"Error: {e}")


def serialization_private_key(private_key, private_pem: str):
    """
    Записывает приватный в файл
    :param private_key: приватный ключ для записи
    :param private_pem: путь для записи
    """
    try:
        with open(private_pem, 'wb') as private_out:
            private_out.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()))
    except Exception as e:
        print(f"Error: {e}")


def deserialization_public_key(public_pem: str):
    """
    Считывает публичный ключ с файла
    :param public_pem: путь для чтения
    :return d_public_key: значение ключа
    """
    try:
        with open(public_pem, 'rb') as pem_in:
            public_bytes = pem_in.read()
        d_public_key = load_pem_public_key(public_bytes)
    except Exception as e:
        print(f"Error: {e}")
        raise

    return d_public_key


def deserialization_private_key(private_pem: str):
    """
    Считывает приватный ключ с файла
    :param private_pem: путь для чтения
    :return d_private_key: значение ключа
    """
    try:
        with open(private_pem, 'rb') as pem_in:
            private_bytes = pem_in.read()
        d_private_key = load_pem_private_key(private_bytes, password=None)
    except Exception as e:
        print(f"Error: {e}")
        raise

    return d_private_key


def crypt_key_or_nonce(public_key, data):
    """
    шифрует ключ или параметр согласно публичному ключу
    :param public_key: ключ для шифрования
    :param data: шифруемый ключ или шифруемый параметр
    :return encrypted_key: зашифрованный ключ/параметр
    """
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data


def decrypt_key(private_key, data):
    """
    Расшифровывает ключ или параметр согласно приватному ключу
    :param private_key: ключ для расшифрования
    :param data: расшифруемый ключ или расшифруемый параметр
    :return decrypted_data: зашифрованный ключ/параметр
    """
    decrypted_data = private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data