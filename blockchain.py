import time as t
import hashlib
import requests as r
from tinydb import TinyDB
import sys
from Utilities import *


class Blockchain:
    """ blockchain class for all things related to the blockchain """

    def __init__(self):
        self.Blockchain_DB = TinyDB('Blockchain.json')  # Blockchain database
        self.Node_DB = TinyDB('Nodes.json')

        self.verified_transactions = []  # Verified and valid transactions would go there
        self.Unverified_transactions = []  # Unverified transactions go there
        self.chain = []  # the chain
        self.nodes = []  # the nodes list
        if len(self.Blockchain_DB.all()) > 0:
            # Checks the blockchain file for any data
            self.chain = self.Blockchain_DB.all()
        else:
            self.chain.append(self.make_block(
                forger='network', previous_hash='0', proof=0))

        if len(self.Node_DB.all()) > 0:
            # Checks the nodes database for data
            self.nodes = self.Node_DB.all()

    def double_spend_check(self, transaction_id, signature):
        """ Checks for double spending, returns false if transaction is invalid and true if it is completely valid """
        valid_transaction = True
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['id'] == transaction_id or transaction['signature'] == signature:
                    return False
        return True

    def make_block(self, forger, previous_hash, proof: int):
        """ creates blocks and verifies transactions """
        for transaction in self.Unverified_transactions:
            keys = KEYS()
            sender = transaction['sender']
            receiver = transaction['receiver']
            signature = transaction['signature']
            transaction_id = transaction['id']
            # TODO double spend check
            valid_transaction_id = self.double_spend_check(
                transaction_id, signature)
            valid_keys = keys.verify_signature(signature, sender, receiver)
            if valid_keys == True and valid_transaction_id == True:
                self.verified_transactions.append(transaction)
            else:
                self.Unverified_transactions.remove(transaction)
        block = {
            'index': len(self.chain),
            'timestamp': t.time(),
            'transactions': self.verified_transactions,
            'proof': proof,
            'previous hash': previous_hash
        }
        if len(self.chain) < 1:
            block = {
                'index': 0,
                'timestamp': t.time(),
                'transactions': None,
                'proof': 0,
                'previous hash': 'Man I wish this was backed by something...'
            }
        # TODO make a way to verify transactions and validate them
        return block

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        work = "0"*5
        max_size = sys.maxsize
        print(f"current work: {work}")
        print(f"max integer: {max_size}")
        chain = self.chain
        while check_proof is False:
          if chain == self.chain: # proof of work algorithm: new_proof**2 - previous_proof**2
                 hash_op = hashlib.scrypt(str(new_proof**2 - previous_proof**2).encode(), n=1024, r=1, p=1, salt=f"{work}".encode()).hex()
                 if hash_op[:len(work)] == work:
                         check_proof = True
                         print(hash_op)
                 else:
                         new_proof += 1
          else:
                check_proof = False
                return new_proof

    def announce_block(self, block):
        for node in self.nodes:
                try:
                        r.post(f"http://{node}/new_block", json={'block': block})
                except Exception as e:
                        print(e) # debugging purposes
if __name__ == '__main__':
        blockchain = Blockchain()
        proof_test = blockchain.proof_of_work(previous_proof=0)
        print(proof_test)