import time,unit_generate,base64
def generate_dict(dict, ramdom_float_num, ua,frist_time,sessionID,apipath,webpath ):
    nowtime = int(time.time() * 1000)
    dict['d'] = nowtime
    dict['e'] = ua
    dict['s'] = sessionID
    dict['u'] = apipath
    dict['c'] = webpath
    dict['f']['i_e'] = frist_time
    dict['f']['ua'] = ua
    dict['b'] =int(ramdom_float_num*2147483647)
    # p=b+r+q+z+b+d+v
    textp=f"{dict['b']}{dict['r']}{dict['q']}{dict['z']}{dict['b']}{dict['d']}{dict['v']}"
    dict['p'] =generate_p(textp)
    return dict

def generate_p(text):# p=b+r+q+z+b+d+v
    x1 = 0
    for i in text:
        x1 = unit_generate.encodechat(i, x1)
    return unit_generate.right3(x1,0) 

def generate_nonce(d,b):   # d,b
    res=[]
    for i in range(4):
        str=f"0{d}{i}{b}"
        strbytes=str.encode('utf-8')
        res_num =unit_generate.fnv1a_32(strbytes)
        res=res+unit_generate.hex_to_byte_list(unit_generate.in32(res_num))
    return res

def generate_X_net_sync_term(dicts,SST):
    x_header = [2, 188, 0, 4] + list(base64.b64decode(SST))
    nonce = generate_nonce(dicts['d'], dicts['b'])
    ciphertext=list(unit_generate.aes_ctr_encrypt(unit_generate.encode_dict_to_byte(dicts),nonce))

    return base64.b64encode(bytes(x_header+nonce+ciphertext)).decode()



    