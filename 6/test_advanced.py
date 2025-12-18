import pytest
from unittest.mock import Mock, patch, mock_open
from asym import *


@pytest.mark.parametrize("test_input", [
    "Печеньки".encode('utf-8'),
    b"One year later...",
    b"AX" * 50,
])
def test_encryption_parametrized(test_input):
    """
    Проверка целостности данных после шифрования с применением параметров
    
    :param test_input: Тестовые данные для шифрования
    """
    private_key, public_key = generate_assymetric_key()
    encrypted = crypt_key_or_nonce(public_key, test_input)
    decrypted = decrypt_key(private_key, encrypted)
    assert decrypted == test_input


def test_serialization_with_file_mocks():
    """
    Проверка записи публичного ключа в файл с использованием заглушек
    
    Тест заменяет вызовы open, write на mock объекты, что позволяет
    проверить корректность взаимодействия тестируемой функции с 
    файловыми объектами
    """
    mock_key = Mock()
    mock_key.public_bytes.return_value = b"MOCK_PEM_DATA"
    
    mock_file_handler = mock_open()
    
    with patch('builtins.open', mock_file_handler):
        serialization_public_key(mock_key, 'test_key.pem')
        
        mock_file_handler.assert_called_once_with('test_key.pem', 'wb')
        
        assert mock_file_handler().write.called
        
        write_call = mock_file_handler().write.call_args[0][0]
        assert write_call == b"MOCK_PEM_DATA"
        
        mock_key.public_bytes.assert_called_once_with(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

def test_with_fixtures():
    """
    Проверка  cохранения целостности данных после шифрования
    
    :param key_pair: Фикстура с парой ключей
    """
    private_key, public_key = generate_assymetric_key()
    
    test_data = "Тестовые данные для проверки".encode('utf-8')
    encrypted = crypt_key_or_nonce(public_key, test_data)

    assert encrypted != test_data

    decrypted = decrypt_key(private_key, encrypted)
    assert decrypted == test_data