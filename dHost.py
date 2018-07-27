"""
dHost - a node in the network.

Uses SHA256 as its cryptographic hash function. The Blockchain class has
the structure of the IBM Blockchain but with PoW instead of SE. PoW
algorithm adapted from Kansal, 2018.

For larger-scale implementations, please modify the confirm() function to
split transactions appropriately.
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

    def __init__(self, identifier, last, tx, timeAppended):
        self.identifier = identifier
        self.last = last # Hash of preceding block
        self.tx = tx # Transactions
        self.timeAppended = timeAppended
        self.nonce = nonce # For Proof of Work algorithm

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

    difficultyFactor = 1; # Adjusted as needed based on hash power

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

    def queueTx(self, tx):
        self.unconfirmed.append(tx)

    """
    Proof of Work (PoW): hard to produce data but easy to check - prevents
    creation of multiple 'valid' chains as well as defends against Denial
    of Service (DoS) attacks. Try random nonce until match on first
    character (with difficulty modifier) - adapted from Kansal, 2018.
    """
    def proveWork(self):
        block.nonce = 0
        while True:
            hash = block.doWork()
            if (hash.startswith('0' * Blockchain.difficultyFactor):
                return hash

    def verifyPoW(self, block, hash):
        return (pow.startswith('0' * Blockchain.difficultyFactor)
                and pow == block.doWork())

    """
    Checks if the previous hash matches and proof of work is valid. If they
    are, the block is appended to the Blockchain.

    MARKER TODO: print success/failure
    """
    def appendToChain(self, block, pow):
        if (block.preceding == self.preceding.hash
        and self.verifyPoW(block, pow)):
            block.hash = pow
            self.chain.append(block)
            return True
        else:
            return False

    """
    Confirm block by computing PoW. In larger-scale implementations,
    transactions to confirm should be split appropriately. Returns new
    identifier to keep track of the tail block.

    MARKER TODO print nothing to mine
    """
    def confirm(self):
        if self.unconfimed: # If there are transactions to confirm
            blockToAdd = Block( identifier = self.preceding.identifier + 1,
                                last = self.preceding.hash,
                                tx = self.unconfirmed
                                timeAppended = time.time())
            pow = self.proveWork(blockToAdd)
            self.appendToChain(blockToAdd, pow)
            self.unconfirmed = []
            return blockToAdd.index
        else:
            return False
