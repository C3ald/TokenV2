from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa
import string
import random
import os
class KEYS:
	def __init__(self):
		pass

	def password_gen(self,length=57):
		""" Generates a password from a length, default is 57 bytes """
		characters = list(string.ascii_letters + string.digits + "!@#$%^&*()") # characters
		random.shuffle(characters) # shuffle
		password = []
		for i in range(length):
			password.append(random.choice(characters))
		random.shuffle(password)
		return "".join(password)
	def key_gen(self,password:str):
		""" Generates keys """
		key = ECC.EccKey(seed=password.encode(), curve='Ed448')
		priv = key.export_key(format='DER').hex()
		public = key.public_key().export_key(format='DER').hex()
		return {"private key": priv, 'public key': public}
	
	
	def signature_gen(self, private_key:str, receiver_pub_key:str):
		""" Makes signatures, private key is what encrypts and the receiver public key is what is encrypted """
		message = receiver_pub_key.encode()
		key = ECC.import_key(bytes.fromhex(private_key))
		signer = eddsa.new(key,mode='rfc8032')
		signature = signer.sign(receiver_pub_key.encode())
		return signature.hex()


	def verify_signature(self,signature:str,public_key_of_signer:str,public_key_of_receiver_in_transaction:str):
		""" Verifies the signature returns True if the signature checks out and false if it is invalid"""
		message = public_key_of_receiver_in_transaction
		key = ECC.import_key(bytes.fromhex(public_key_of_signer))
		verifier = eddsa.new(key, mode='rfc8032')
		try:
			verifier.verify(message.encode(),bytes.fromhex(signature))
			return True
		except ValueError:
			return False

if __name__ == '__main__':
	key = KEYS()
	password = key.password_gen()
	keys = key.key_gen(password)
	print(password)
	print(keys)
	sign = key.signature_gen(keys['private key'], receiver_pub_key='joe')
	print(sign)
	verify = key.verify_signature(sign, keys['public key'], public_key_of_receiver_in_transaction='joe')
	print(verify)



