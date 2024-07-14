import hashlib
import base58

def private_key_to_wif(priv_key_hex):
    # Шаг 1: Добавляем префикс 0x80 к приватному ключу
    extended_key = '80' + priv_key_hex
    
    # Шаг 2: Двойное SHA-256 хеширование
    first_sha256 = hashlib.sha256(bytes.fromhex(extended_key)).hexdigest()
    second_sha256 = hashlib.sha256(bytes.fromhex(first_sha256)).hexdigest()
    
    # Шаг 3: Добавляем контрольную сумму (первые 4 байта второго хеша)
    checksum = second_sha256[:8]
    final_key = extended_key + checksum
    
    # Шаг 4: Конвертируем в base58
    wif = base58.b58encode(bytes.fromhex(final_key)).decode('utf-8')
    return wif

# Пример использования
priv_key_hex = '000'
wif_key = private_key_to_wif(priv_key_hex)
print(wif_key)
