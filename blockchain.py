import time as t
import hashlib
import requests as r
from tinydb import TinyDB



class Blockchain:
	""" blockchain class for all things related to the blockchain """
	def __init__(self):
		self.Blockchain_DB = TinyDB('Blockchain.json') # Blockchain database
		self.Node_DB = TinyDB('Nodes.json')

		self.verified_transactions = [] #Verified and valid transactions would go there
		self.Unverified_transactions = [] # Unverified transactions go there
		self.chain = [] #the chain
		self.nodes = [] # the nodes list
		if len(self.Blockchain_DB.all()) > 0:
			# Checks the blockchain file for any data
			self.chain = self.Blockchain_DB.all()
		else:
			self.chain.append(self.make_block(forger='network', previous_hash='0', proof=0))
		
		if len(self.Node_DB.all()) > 0:
			# Checks the nodes database for data
			self.nodes = self.Node_DB.all()
	
	def make_block(self, forger, previous_hash, proof:int):
		""" creates blocks and verifies transactions """
		block = {
			'index': len(self.chain),
			'timestamp': t.time(),
			'transactions': self.verified_transactions,
			'proof': proof,
			'previous hash': previous_hash
		}
		if self.chain < 1:
			block = {
				'index': 0,
				'timestamp':t.time(),
				'transactions':None,
				'proof': 0,
				'previous hash': None
			}
		#TODO make a way to verify transactions and validate them
		return block
	def announce_block(self, block):
		for node in self.nodes:
			r.post(f"http://{node}/new_block", json={'block':block})
