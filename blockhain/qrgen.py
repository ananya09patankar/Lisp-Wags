import  qrcode, ed25519
from binascii import hexlify, unhexlify                                                                 
from struct import Struct                                                                              
from utils import g, b58encode, b58decode
import argparse
import hashlib
# If one wants to covert to base58 these are the 3 functions but not used in this implementation
def count_leading_zeroes(s):                                                                            
    count = 0                                                                                           
    for c in s:                                                                                         
        if c == '\0':                                                                                   
            count += 1                                                                                  
        else:                                                                                           
            break
    return count

def base58_check_encode(prefix, payload, compressed=False):                                           
    s = prefix + payload                                                                                
    if compressed:                                                                                      
        s = prefix + payload + b'\x01'                                                              
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]                      
    result = s + checksum                                                                            
    return '1' * count_leading_zeroes(result) + b58encode(result).decode()                             
                                                                                      
def pub_key_to_addr(s):                                                                                 
    ripemd160 = hashlib.new('ripemd160')                                                               
    hash_sha256 = hashlib.new('SHA256')                                                             
    hash_sha256.update(bytes.fromhex(s))                                                     
    ripemd160.update(hash_sha256.digest())
    return base58_check_encode(b'\0', ripemd160.digest())
 
privKey, pubKey = ed25519.create_keypair()
privKey2 = privKey.to_ascii(encoding='hex').decode("utf-8")
pubKey2 = pubKey.to_ascii(encoding='hex').decode("utf-8")
print("Private key (32 bytes):", privKey2)
print("Public key (32 bytes): ", pubKey2)
img = qrcode.make(pubKey2)
img.save("{}.png".format(pubKey))

msg = b'Message for Ed25519 signing'
signature = privKey.sign(msg, encoding='hex')

print("Signature (64 bytes):", signature.decode())

try:
    pubKey.verify(signature, msg, encoding='hex')
    print("The signature is valid.")
except:
    print("Invalid signature!")
