"""
dHost - a node in the network.
Uses SHA256 as its cryptographic hash function. The Blockchain class has
the structure of the IBM Blockchain but with PoW instead of SE.
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
block with a hash, rather than a pointer. Uses same structure as the IBM
Blockchain but uses Proof of Work over their own consensus mechanism.
"""
class Blockchain:

    def __init__(self):
        self.chain = [] # The actual blockchain
        self.unconfirmed = [] # Transactions not yet hashed and appended
        self.intialiseChain()

    """
    Point to preceding block - note this requires the first block to have
    been created already. Uses readonly property shorthand.
    """
    @property
    def preceding(self):
        return self.chain[-1] # Conveniently can use -1 in Python

    """
    Creates the first block in the blockchain as this is distinct from
    other blocks in that it has no preceding block to point to.
    """
    def initialiseChain():
        firstBlock = Block(0, '0', [], time.time()) # MARKER check '' vs ""
        firstBlock.hash = originBlock.doWork() # Hash added as new item
        self.chain.append(firstBlock)
