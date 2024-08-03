#pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util import Counter
import base64


key = bytes([45, 67, 89, 12, 34, 56, 78, 90, 123, 234, 45, 67, 89, 12, 34, 56])
def aes_ctr_decrypt(nonce, ciphertext,key=key):
    ctr = Counter.new(128, initial_value=int.from_bytes(nonce, byteorder='big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def decode__(b64_text):
    decoded_bytes = base64.b64decode(b64_text)
    ascii_byte_list = list(decoded_bytes)
    x_net_header = ascii_byte_list[0] + ascii_byte_list[5] + 4
    the_header = ascii_byte_list[:x_net_header]
    nonce = ascii_byte_list[x_net_header:x_net_header + 16]
    ciphertext = ascii_byte_list[(x_net_header + 16):]
    return the_header, nonce, aes_ctr_decrypt(bytes(nonce), bytes(ciphertext))


x_net_sync_term="xxxxxxxxx"
decode__(x_net_sync_term)
