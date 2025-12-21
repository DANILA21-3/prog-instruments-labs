from asym import generate_assymetric_key, crypt_key_or_nonce, decrypt_key

def test_generate_assymetric_key():
    """
    Проверяет работоспобность вызова функции

    """
    private_key, public_key = generate_assymetric_key()
    assert private_key is not None
    assert public_key is not None

def test_crypt_key_or_nonce_basic():
    """
    Проверяет функцию на работоспосбность во время работы функции,
    возвращение не None и отличие исходных данных от результата

    """
    _ , public_key = generate_assymetric_key()
    test_data = b"Some word"
    encrypted_data = crypt_key_or_nonce(public_key, test_data)
    assert encrypted_data is not None
    assert encrypted_data != test_data

def test_decrypt_key_basic():
    """
    Проверяет являются ли зашифрованные и расшифрованные данные 
    исходными данными

    """
    private_key, public_key = generate_assymetric_key()
    original_data = b"Secret message"
    encrypted = crypt_key_or_nonce(public_key, original_data)
    decrypted = decrypt_key(private_key, encrypted)
    assert decrypted == original_data

def test_encrypt_decrypt_cycle():
    """
    Тестирует цикл шифрования/расшифрования для разных типов данных

    """
    private_key, public_key = generate_assymetric_key()
    test_messages = [b"Short", b"A" * 50, b"Test"]
    for message in test_messages:
        encrypted = crypt_key_or_nonce(public_key, message)
        decrypted = decrypt_key(private_key, encrypted)
        assert decrypted == message

def test_rsa_oaep_randomization():
    """
    Проверка недетерминированности шифрования
    
    """
    private_key, public_key = generate_assymetric_key()
    test_data = b"Two year later..."

    encrypted1 = crypt_key_or_nonce(public_key, test_data)
    encrypted2 = crypt_key_or_nonce(public_key, test_data)
    assert encrypted1 != encrypted2
    
    decrypted1 = decrypt_key(private_key, encrypted1)
    decrypted2 = decrypt_key(private_key, encrypted2)
    assert decrypted1 == test_data
    assert decrypted2 == test_data