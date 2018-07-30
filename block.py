import json
from hashlib import sha256

class Block:
    
    def __init__(self, block_id, timestamp, preceding_block_hash, block_tx):
        self.block_id = block_id
        self.timestamp = timestamp
        self.preceding_block_hash = preceding_block_hash
        self.block_tx = block_tx
        self.nonce = 0

    def hash_block_contents(self):
        return sha256(json.dumps(self.__dict__, sort_keys = True)
                      .encode()).hexdigest()
