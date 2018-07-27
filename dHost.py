'''
dHost - a node in the network.

Uses SHA256 as its cryptographic hash function. The Blockchain class has
the structure of the IBM Blockchain but with PoW instead of SE. PoW
algorithm adapted from Kansal, 2018.

For larger-scale implementations, please modify the confirm() function to
split transactions appropriately.
'''

import requests
import time
import json
from hashlib import sha256
from flask import Flask, request


app = Flask(__name__)
nodes = set()


'''
===========================================================================
Block
===========================================================================
A group of records added to the blockchain in each appending operation. For
record-keeping, merkle trees are unnecessary.
===========================================================================
'''
class Block:

    def __init__(self, identifier, last, tx, timeAppended):
        self.identifier = identifier
        self.last = last # Hash of preceding block
        self.tx = tx # Transactions
        self.timeAppended = timeAppended
        self.nonce = nonce # For Proof of Work algorithm

    '''
    Calculate hash on block data itself.
    '''
    def doWork(self):
        hash = sha256(json.dumps(self.__dict__, sort_keys = True).encode())
        return hash.hexdigest()

'''
===========================================================================
End of Block class
===========================================================================
'''


'''
===========================================================================
Blockchain
===========================================================================
Essentially a singly linked list of blocks but referring to the previous
block with a hash, rather than a pointer. Uses same structure as the IBM
Blockchain but uses Proof of Work over their own consensus mechanism.
===========================================================================
'''
class Blockchain:

    difficultyFactor = 1; # Adjusted as needed based on hash power

    def __init__(self):
        self.chain = [] # The actual blockchain
        self.unconfirmed = [] # Transactions not yet hashed and appended
        self.intialiseChain()

    '''
    Point to preceding block - note this requires the first block to have
    been created already. Uses readonly property shorthand.
    '''
    @property
    def preceding(self):
        return self.chain[-1] # Conveniently can use -1 in Python

    '''
    Creates the first block in the blockchain as this is distinct from
    other blocks in that it has no preceding block to point to.
    '''
    def initialiseChain():
        firstBlock = Block(0, '0', [], time.time()) # MARKER check '' vs ''
        firstBlock.hash = originBlock.doWork() # Hash added as new item
        self.chain.append(firstBlock)

    def queueTx(self, tx):
        self.unconfirmed.append(tx)

    '''
    Proof of Work (PoW): hard to produce data but easy to check - prevents
    creation of multiple 'valid' chains as well as defends against Denial
    of Service (DoS) attacks. Try random nonce until match on first
    character (with difficulty modifier) - adapted from Kansal, 2018.
    '''
    def proveWork(self):
        block.nonce = 0
        while True:
            hash = block.doWork()
            if (hash.startswith('0' * Blockchain.difficultyFactor):
                return hash

    def verifyPoW(self, block, hash):
        return (pow.startswith('0' * Blockchain.difficultyFactor)
                and pow == block.doWork())

    '''
    Checks if the previous hash matches and proof of work is valid. If they
    are, the block is appended to the Blockchain.

    MARKER TODO: print success/failure
    '''
    def appendToChain(self, block, pow):
        if (block.preceding == self.preceding.hash
        and self.verifyPoW(block, pow)):
            block.hash = pow
            self.chain.append(block)
            return True
        else:
            return False

    '''
    Confirm block by computing PoW. In larger-scale implementations,
    transactions to confirm should be split appropriately. Also broadcasts
    confirmations to the network.
    '''
    def confirm(self):
        if self.unconfirmed: # If there are transactions to confirm
            blockToAdd = Block( identifier = self.preceding.identifier + 1,
                                last = self.preceding.hash,
                                tx = self.unconfirmed
                                timeAppended = time.time())
            pow = self.proveWork(blockToAdd)
            self.appendToChain(blockToAdd, pow)
            self.unconfirmed = []
            for node in nodes:
                requests.post('http://{}/addblocks'.format(node),
                data = json.dumps(blockToAdd.__dict__, sort_keys = True))
            return True
        else:
            return False

    @classmethod
    def isValidChain(cls, chain):
        result = True
        last = "0"

        # MARKER CHANGE THIS
        for block in chain:
            hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not (block_hash.startswith('0' * Blockchain.difficulty)
                    or hash == block.doWork())
                    or last == block.last:
                result = False
                break

            block.hash, last = hash, hash

        return result

'''
===========================================================================
End of Blockchain class
===========================================================================
'''


'''
===========================================================================
Consensus Mechanism
===========================================================================
If a longer chain exists, check it is valid and if so replace current chain
with it. If this is the longest chain, returns False.
===========================================================================
'''
def consensus():
    global blockchain
    longest = None
    length = len(blockchain)
    for node in nodes:
        response = requests.get('http://{}/blockchain'.format(node))
        length = response.json()['length']
        thisChain = response.json()['chain']
        if thisLength > length and blockchain.isValidChain(thisChain):
            length = thisLength
            longest = thisChain
    if longest:
        blockchain = longest
        return True
    else:
        return False



'''
===========================================================================
End of Consensus Mechanism
===========================================================================
'''



'''
===========================================================================
Endpoints
===========================================================================
Six endpoints - adapted from IBM Blockchain developerWorks documentation.
1. Query the node's copy of the blockchain (GET)
2. Submit a transaction from the app (POST)
3. Request confirmation of transactions (GET)
4. Query unconfirmed transactions
5. Add nodes to network (POST)
6. Check and add block confirmed by another node to chain (POST)
===========================================================================
'''

nodeChainCopy = Blockchain()

'''
Query the node's copy of the blockchain (GET)
'''
@app.route('/blockchain', methods=['GET']) # MARKER no camelcase http?
def getBlockchain():
    contents = []
    for block in nodeChainCopy.chain:
        contents.append(block.__dict__)
    return json.dumps({"length": len(contents), "chain": contents})

'''
Submit a transaction from the app (POST)
'''
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json();
    data.timeAppended = time.time()
    dataItems = ['author', 'content']
    for items in dataItems:
        if not data.get(field):
            return 'Transaction rejected: all fields required.', 404
    nodeChainCopy.appendToChain(data)
    return 'Transaction accepted.', 201

'''
Request confirmation of transactions (GET)
'''
@app.route('/confirm', methods=['GET']) # MARKER no camelcase http?
def requestConfirmation():
    if nodeChainCopy.confirm():
        return 'Block confirmed.'
    else:
        return 'No pending transactions.'

'''
Query unconfirmed transactions
'''
@app.route('/unconfirmed')
def getUnconfirmed():
    return json.dumps(nodeChainCopy.unconfirmed)

'''
Add nodes to network (POST)
'''
@app.route('/addnodes', methods=['POST'])
def addNodes():
    visibleNodes = request.get_json()
    if not visibleNodes:
        return 'Bad request.', 400
    for node in visibleNodes:
        nodes.add(node)
    return 'Nodes added to network.', 201

'''
Check and add block confirmed by another node to this node's chain (POST)
'''
@app.route('/addblocks', methods=['POST'])
def addBlocks():
    data = request.get_json()
    # MARKER Conflict with previous variables with same names?
    pow = data['hash']
    blockToAdd = Block( data['identifier'],
                        data['last'],
                        data['tx'],
                        data['timeAppended'])
    if nodeChainCopy.appendToChain(blockToAdd, pow):
        return 'Block added to chain.', 201
    else:
        return 'Invalid block: discarded by node.', 400

'''
===========================================================================
End of endpoints
===========================================================================
'''



app.run(debug = True, port = 8000)
