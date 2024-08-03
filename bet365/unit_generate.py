import operator
from Crypto.Cipher import AES
from Crypto.Util import Counter
import base64

key = bytes([45, 67, 89, 12, 34, 56, 78, 90, 123, 234, 45, 67, 89, 12, 34, 56])

def aes_ctr_encrypt(plaintext,nonce,key=key):
    ctr = Counter.new(128, initial_value=int.from_bytes(nonce, byteorder='big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext


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


def decode_byte_to_dict(bytestext):
    def parse_data(data):
        pos = 0
        result = {}
        while pos < len(data):
            if pos + 1 > len(data):
                break
            key_length = data[pos]
            pos += 1
            if pos + key_length > len(data):
                break
            key = data[pos:pos + key_length].decode('utf-8')
            pos += key_length
            if pos + 2 > len(data):
                break
            value_length_part1 = data[pos]
            value_length_part2 = data[pos + 1]
            value_length = value_length_part1 + value_length_part2 * 256
            pos += 2
            if pos + value_length > len(data):
                break
            value = data[pos:pos + value_length]
            pos += value_length
            if   ("i_c" not in result.keys() and key in ["d", "b", "p", "r", "q", "v", "w"]) or (key.startswith("i_") ):
                value = int.from_bytes(value, byteorder='little')
            else:
                try:
                    value = value.decode('utf-8')
                except:
                    pass
            result[key] = value
        return result

    dicts = parse_data(bytestext)
    if 'f' in dicts:
        dicts['f'] = parse_data(dicts['f'])
    return dicts


def jisuan(a1, a2, func):
    # 将值限制在 32 位范围内
    a1 = a1 & 0xFFFFFFFF
    a2 = a2 & 0xFFFFFFFF
    # 执行指定的位操作
    result = func(a1, a2) & 0xFFFFFFFF
    # 如果结果的最高位是 1，则这是一个负数
    if result & 0x80000000:
        result -= 0x100000000
    return result
def right3(value, shift):
    # js中value>>>shift
    if value < 0:
        value += 2 ** 32
    # 进行右移操作
    return (value >> shift) & (2 ** 32 - 1)


num1 = 1101195530
num2 = 1849170683
num3 = 1011462487
num4 = 1870552039
num5 = 2116561607
num6 = 1297822139
num7 = 495394314
num8 = 684556403
num9 = 1902634096
num10 = 37428903
num11 = 787769321
def encodechat(char, key):
    f1 = jisuan(key,  ord(char), operator.xor)

    a2 = jisuan(f1, 1, operator.lshift)
    a3 = right3(f1, 31)
    a4 = jisuan(a2, a3, operator.or_)
    f1 = jisuan(a4, num1, operator.xor)
    f1 = forfunc(f1, num1)
    f1 = forfunc(f1, num2)
    f1 = forfunc(f1, num3)
    f1 = forfunc(f1, num4)
    f1 = forfunc(f1, num5)
    f1 = forfunc(f1, num6)
    f1 = forfunc(f1, num7)
    f1 = forfunc(f1, num8)

    a2 = jisuan(f1, 1, operator.lshift)
    a3 = right3(f1, 31)
    a4 = jisuan(a2, a3, operator.or_)
    f1 = jisuan(a4, num2, operator.xor)
    f1 = forfunc(f1, num2)
    f1 = forfunc(f1, num3)
    f1 = forfunc(f1, num4)
    f1 = forfunc(f1, num5)
    f1 = forfunc(f1, num6)
    f1 = forfunc(f1, num7)
    f1 = forfunc(f1, num8)
    f1 = forfunc(f1, num9)

    a2 = jisuan(f1, 1, operator.lshift)
    a3 = right3(f1, 31)
    a4 = jisuan(a2, a3, operator.or_)
    f1 = jisuan(a4, num3, operator.xor)
    f1 = forfunc(f1, num3)
    f1 = forfunc(f1, num4)
    f1 = forfunc(f1, num5)
    f1 = forfunc(f1, num6)
    f1 = forfunc(f1, num7)
    f1 = forfunc(f1, num8)
    f1 = forfunc(f1, num9)
    f1 = forfunc(f1, num10)

    a2 = jisuan(f1, 1, operator.lshift)
    a3 = right3(f1, 31)
    a4 = jisuan(a2, a3, operator.or_)
    f1 = jisuan(a4, num4, operator.xor)
    f1 = forfunc(f1, num4)
    f1 = forfunc(f1, num5)
    f1 = forfunc(f1, num6)
    f1 = forfunc(f1, num7)
    f1 = forfunc(f1, num8)
    f1 = forfunc(f1, num9)
    f1 = forfunc(f1, num10)
    f1 = forfunc(f1, num11)

    return f1


def forfunc(a5, keys):
    a6 = jisuan(a5, 65535, operator.and_)
    a7 = jisuan(a5, keys, operator.xor)
    a8 = jisuan(a7, 65535, operator.and_)
    a9 = jisuan(a6, a8, operator.mul)
    a10 = jisuan(a9, 65535, operator.and_)
    a11 = right3(a5, 16)
    a12 = jisuan(a11, 65535, operator.and_)
    a13 = jisuan(a5, keys, operator.xor)
    a14 = right3(a13, 16)
    a15 = jisuan(a12, a14, operator.mul)
    a16 = jisuan(a15, 65535, operator.and_)
    a17 = jisuan(a10, 16, operator.lshift)
    a18 = a5 + a17
    a19 = a18 + a16
    a20 = right3(a19, 0)
    a21 = jisuan(a20, 15, operator.and_)
    a22 = a21 + 1
    a23 = right3(a20, a22)
    a24 = jisuan(a20, a23, operator.xor)
    return a24

def to_signed_32bit(value):
    # 将整数限制在 32 位范围内
    value = value & 0xFFFFFFFF
    # 如果最高位是1，将其解释为负数
    if value & 0x80000000:
        return value - 0x100000000
    else:
        return value

def hex_to_byte_list(hex_num):
    # 确保输入为整数
    if not isinstance(hex_num, int):
        raise ValueError("Input must be an integer")
    byte_list = [
        (hex_num >> 24) & 0xFF,  # 提取最高字节
        (hex_num >> 16) & 0xFF,  # 提取次高字节
        (hex_num >> 8) & 0xFF,  # 提取次低字节
        hex_num & 0xFF  # 提取最低字节
    ]
    return byte_list
def fnv1a_32(data):
    FNV_prime = 16777619
    offset_basis = 2166136261
    hash_value = offset_basis
    for byte in data:
        hash_value ^= byte
        hash_value *= FNV_prime
        # 确保哈希值保持在 32 位范围内
        hash_value &= 0xFFFFFFFF
    return hash_value

def in32(hash_value):
    if hash_value>2147483647:
        return to_signed_32bit(hash_value)*-1
    else:
        return hash_value


def extendbytes(keystr, key):
    return len(str(keystr)).to_bytes(1, byteorder='little') + keystr.encode() + len(key).to_bytes(2,
                                                                                                  byteorder='little')  + key
def encode_dict_to_byte(dictcontent):
    bts = bytearray()
    d = dictcontent['d'].to_bytes(8, byteorder='little')
    a = dictcontent['a'].encode()
    b = dictcontent['b'].to_bytes(4, byteorder='little')
    c = dictcontent['c'].encode()
    e = dictcontent['e'].encode()
    p = dictcontent['p'].to_bytes(8, byteorder='little')
    g = dictcontent['g'].encode()
    h = dictcontent['h'].encode()
    n = dictcontent['n'].encode()
    o = dictcontent['o'].encode()
    q = dictcontent['q'].to_bytes(1, byteorder='little')
    r = dictcontent['r'].to_bytes(1, byteorder='little')
    s = dictcontent['s'].encode()
    t = dictcontent['t'].encode()
    u = dictcontent['u'].encode()
    v = dictcontent['v'].to_bytes(1, byteorder='little')
    x = dictcontent['x'].encode()
    z = dictcontent['z'].encode()
    f_i_c = dictcontent['f']['i_c'].to_bytes(1, byteorder='little')
    f_i_e = dictcontent['f']['i_e'].to_bytes(8, byteorder='little')
    f_i_n = dictcontent['f']['i_n'].to_bytes(1, byteorder='little')
    f_i_u = dictcontent['f']['i_u'].to_bytes(1, byteorder='little')
    f_i_r = dictcontent['f']['i_r'].to_bytes(1, byteorder='little')
    f_i_cl = dictcontent['f']['i_cl'].to_bytes(1, byteorder='little')
    f_i_ev = dictcontent['f']['i_ev'].to_bytes(8, byteorder='little')
    f_i_ps = dictcontent['f']['i_ps'].to_bytes(4, byteorder='little')
    f_uqid = dictcontent['f']['uqid'].encode()  # \x00
    f_fw = dictcontent['f']['fw'].encode()
    f_ua = dictcontent['f']['ua'].encode()
    f_rf = dictcontent['f']['rf'].encode()
    f_i_l = dictcontent['f']['i_l'].to_bytes(1, byteorder='little')
    f_z = dictcontent['f']['z'].encode()
    f_x = dictcontent['f']['x'].encode()
    f_i_z = dictcontent['f']['i_z'].to_bytes(1, byteorder='little')
    f_pi = dictcontent['f']['pi'].encode()
    f = bytearray()
    f.extend(extendbytes("i_c", f_i_c))
    f.extend(extendbytes("i_e", f_i_e))
    f.extend(extendbytes("i_n", f_i_n))
    f.extend(extendbytes("i_u", f_i_u))
    f.extend(extendbytes("i_r", f_i_r))
    f.extend(extendbytes("i_cl", f_i_cl))
    f.extend(extendbytes("i_ev", f_i_ev))
    f.extend(extendbytes("i_ps", f_i_ps))
    f.extend(extendbytes("uqid", f_uqid))
    f.extend(extendbytes("fw", f_fw))
    f.extend(extendbytes("ua", f_ua))
    f.extend(extendbytes("rf", f_rf))
    f.extend(extendbytes("i_l", f_i_l))
    f.extend(extendbytes("z", f_z))
    f.extend(extendbytes("x", f_x))
    f.extend(extendbytes("i_z", f_i_z))
    f.extend(extendbytes("pi", f_pi))

    bts.extend(extendbytes("d", d))
    bts.extend(extendbytes("a", a))
    bts.extend(extendbytes("b", b))
    bts.extend(extendbytes("c", c))
    bts.extend(extendbytes("e", e))
    bts.extend(extendbytes("p", p))
    bts.extend(extendbytes("g", g))
    bts.extend(extendbytes("h", h))
    bts.extend(extendbytes("n", n))
    bts.extend(extendbytes("o", o))
    bts.extend(extendbytes("q", q))
    bts.extend(extendbytes("r", r))
    bts.extend(extendbytes("s", s))
    bts.extend(extendbytes("t", t))
    bts.extend(extendbytes("u", u))
    bts.extend(extendbytes("v", v))
    bts.extend(extendbytes("x", x))
    bts.extend(extendbytes("z", z))
    bts.extend(len(str('f')).to_bytes(1, byteorder='little') +  "f".encode() + len(f).to_bytes(2,byteorder='little')  + f)
    return bts
