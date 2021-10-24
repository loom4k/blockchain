import hashlib
import json

from time import time
from uuid import uuid4

from textwrap import dedent

from flask import Flask
from flask.json import jsonify

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Creates the new genesis block
        self.new_block(previous_hash = 1, proof = 100)

    def new_block(self):
        """
        Creates a new block in the blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (optionnal) <str> Hash of the previous block
        :return: <dict> New block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Resets the list of current transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self):
        """
        Creates a new transaction to go into the next mined block
        :param sender: <str> Address of the sender
        :param recipient: <str> Addess of the recipient
        :param amount: <int> Amount
        :return <int> The index of the block that will hold the transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # Returns the last block in the chain
        pass

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block
        :param block: <dict> Block
        :return <str>
        """

        # Make sure the dictionnary is ordered or there will be inconsistent hashes
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple proof of work application
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

# Create the flask Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_indentifier = str(uuid4()).replace('-', '')

# Instantiate the blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new block"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)