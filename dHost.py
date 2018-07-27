# dHost - a node in the network

# We use SHA256 as our cryptographic hash fucntion
from hashlib import sha256

# Block
# A group of records added to the blockchain in each
# appending operation
class Block:
    def __init__(self, identifier, last, tx, timestamp):
        self.identifier = identifier
        self.last = last # Hash of preceding block
        self.tx = tx # Transactions
        self.timestamp = timestamp

# Blockchain
# Essentially a singly linked list of blocks but referring to
# the previous block with a hash, rather than a pointer
class Blockchain:
