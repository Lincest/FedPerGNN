from crypto import random
from tqdm import tqdm
import base64
from crypto.publickey import rsa 
from crypto.signature import pkcs1_v1_5 as pkcs1_signature
from crypto.cipher import pkcs1_v1_5 as pkcs1_cipher
from crypto.cipher import pkcs1_oaep
from crypto.hash import sha256


def generate_key():
    random_generator = random.new().read
    rsa = rsa.generate(2048, random_generator)
    public_key = rsa.publickey().exportkey()
    private_key = rsa.exportkey()
    
    with open('rsa_private_key.pem', 'wb')as f:
        f.write(private_key)
        
    with open('rsa_public_key.pem', 'wb')as f:
        f.write(public_key)
    

def get_key(key_file):
    with open(key_file) as f:
        data = f.read()
        key = rsa.importkey(data)
    return key    

def sign(msg):
    private_key = get_key('rsa_private_key.pem')
    signer = pkcs1_signature.new(private_key)
    digest = sha256.new()
    digest.update(bytes(msg.encode("utf8")))
    return signer.sign(digest)

def verify(msg, signature):
    #use signature because the rsa encryption lib adds salt defaultly
    pub_key = get_key('rsa_public_key.pem')
    signer = pkcs1_signature.new(pub_key)
    digest = sha256.new()
    digest.update(bytes(msg.encode("utf8")))
    return signer.verify(digest, signature)
    
def encrypt_data(msg): 
    pub_key = get_key('rsa_public_key.pem')
    cipher =encryptor = pkcs1_oaep.new(pub_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    return encrypt_text.decode('utf-8')

def decrypt_data(encrypt_msg): 
    private_key = get_key('rsa_private_key.pem')
    cipher = pkcs1_oaep.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_msg))
    return back_text.decode('utf-8')