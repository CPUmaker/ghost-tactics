from Crypto import Random
from Crypto.PublicKey import RSA


def generate_new_key():
    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)

    private_pem = rsa.exportKey()
    with open('master-private.pem', 'wb') as f:
        f.write(private_pem)

    public_pem = rsa.publickey().exportKey()
    with open('master-public.pem', 'wb') as f:
        f.write(public_pem)


generate_new_key()