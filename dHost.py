"""
dHost - a node in the network.
Uses SHA256 as its cryptographic hash function.
"""

from hashlib import sha256
import json

"""
Block
A group of records added to the blockchain in each
appending operation. For record-keeping, merkle trees are
unnecessary.
"""
class Block:

    def __init__(self, identifier, last, tx, timestamp):
        self.identifier = identifier
        self.last = last # Hash of preceding block
        self.tx = tx # Transactions
        self.timestamp = timestamp

    """
    Calculate hash on block.
    """
    def proveWork(self):

"""
Blockchain
Essentially a singly linked list of blocks but referring to
the previous block with a hash, rather than a pointer.
"""
class Blockchain:
