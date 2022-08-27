from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa
import string
import random
import os
def bytes_to_int(bytes):
	result = 0
	for b in bytes:
		result = result * 256 + int(b)
	return result

def int_to_bytes(value, length):
	result = []
	for i in range(0, length):
		result.append(value >> (i * 8) & 0xff)
	result.reverse()
	return result

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
		priv = key.export_key(format='DER')
		public = key.public_key().export_key(format='DER')
		view_key = public * 2
		receiver_address = self.receiver_address(public, view_key)
		return {"private key": priv.hex(), 'public key': public.hex(), 'view key':view_key.hex(), 'receiver address': receiver_address.hex()}
	
	
	def receiver_address(self,public_spend_key:bytes, view_key:bytes):
		""" Generates the receiver address for wallets """
		new_key = public_spend_key + view_key * -2
		return new_key



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



