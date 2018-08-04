import time
import settings
from block import Block

class Blockchain:

    def __init__(self):
        self.blockchain = []
        self.pending_tx = []
        self.initialise_blockchain()

    def initialise_blockchain(self):
        first_block = Block(0, time.time(), '0', [])
        first_block.hash = first_block.hash_block_contents()
        self.blockchain.append(first_block)

    @property
    def preceding_block(self):
        return self.blockchain[-1]

    # Difficulty can be changed in settings.py
    def work_condition(self, hash):
        return hash.startswith('0' * settings.difficulty)

    # Append block after verifying hash and PoW
    def append_block(self, block, pow):

        if not (self.preceding_block.hash == block.preceding_block_hash
                and Blockchain.verify_pow(block, pow)):
            return False
        else:
            block.hash = pow
            self.blockchain.append(block)
            return True

    # PoW: brute force through possible nonces until match
    def proof_of_work(self, block):
        block.nonce = 0
        while True:
            hash = block.hash_block_contents()
            if self.work_condition(hash):
                return hash
            else:
                block.nonce += 1

    def submit_tx(self, tx):
        self.pending_tx.append(tx)

    @classmethod
    def verify_pow(cls, block, hash):
        return (cls.work_condition(cls, hash)
                and hash == block.hash_block_contents())

    # Recompute hashes and verify PoW through the entire blockchain
    @classmethod
    def verify_blockchain(cls, blockchain):
        preceding_block_hash = '0'
        for block in blockchain:
            hash = block.hash
            delattr(block, 'hash')
            if not (cls.verify_pow(block, hash)
                    and preceding_block_hash == block.preceding_block_hash):
                return False
            else:
                block.hash = preceding_block_hash = hash
        return True

    # PoW on pending tx, append to blockchain, announce to network and return ID
    def confirm_pending_tx(self):
        if self.pending_tx:
            preceding_block = self.preceding_block
            pending_block = Block(block_id = preceding_block.block_id + 1,
                                  timestamp = time.time(),
                                  preceding_block_hash = preceding_block.hash,
                                  block_tx = self.pending_tx)
            self.append_block(pending_block, self.proof_of_work(pending_block))
            self.pending_tx = []
            for node in settings.network:
                endpoint = 'http://{}/append_block'.format(node)
                requests.post(endpoint, data = json.dumps(block.__dict__,
                                                          sort_keys = True))
            return pending_block.block_id
        else:
            return False
