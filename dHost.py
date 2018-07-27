"""
dHost - a node in the network.
Uses SHA256 as its cryptographic hash function.
"""

from hashlib import sha256
import time
import json

"""
Block
A group of records added to the blockchain in each appending operation. For
record-keeping, merkle trees are unnecessary.
"""
class Block:

    def __init__(self, identifier, last, tx, timestamp):
        self.identifier = identifier
        self.last = last # Hash of preceding block
        self.tx = tx # Transactions
        self.timestamp = timestamp

    """
    Calculate hash on block data itself.
    """
    def doWork(self):
        hash = sha256(json.dumps(self.__dict__, sort_keys = True).encode())
        return hash.hexdigest()


"""
Blockchain
Essentially a singly linked list of blocks but referring to the previous
block with a hash, rather than a pointer.
"""
class Blockchain:

    def __init__(self):
        self.chain = []
        self.unconfirmed = [] # Transactions not yet hashed and appended
        self.intialiseChain()

    """
    Creates the first block in the blockchain as this is distinct from
    other blocks in that it has no preceding block to point to.
    """
    def initialiseChain():
        originBlock = Block(0, '0', [], time.time()) # MARKER check '' vs ""
