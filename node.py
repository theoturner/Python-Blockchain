import json
import time
import requests
import settings
from block import Block
from blockchain import Blockchain
from flask import Flask, request

settings.launch_network()

blockchain = Blockchain()
app = Flask(__name__)

# Check if submitted transaction has all required inputs before submitting
@app.route('/submit_tx', methods = ['POST'])
def submit_tx():
    tx = request.get_json()
    if (tx.get('user') and tx.get('data')):
        tx['timestamp'] = time.time()
        blockchain.submit_tx(tx)
        return 'Transaction submitted.', 201
    else:
        return 'Transaction rejected: incomplete data.', 404

# Return length and contents of network-agreed blockchain
@app.route('/blockchain', methods = ['GET'])
def get_blockchain():
    get_longest_blockchain()
    blocks = []
    for block in blockchain.blockchain:
        blocks.append(block.__dict__)
    return json.dumps({'length': len(blocks), 'chain': blocks})

# Endpoint for running confirm_pending_tx
@app.route('/confirm_pending_transactions', methods = ['GET'])
def confirm_tx():
    result = blockchain.confirm_pending_tx()
    if result:
        return 'Block #{}\'s transactions have been confirmed.'.format(result)
    else:
        return 'Nothing to confirm: no pending transactions.'

# Add nodes to network
@app.route('/add_nodes', methods = ['POST'])
def add_nodes():
    nodes = request.get_json()
    if nodes:
        for node in nodes:
            settings.network.add(node)
        return 'The nodes have been added to the network.', 201
    else:
        return 'Nothing to add: no nodes were recognised.', 400

# Verify block added by a different node before appending it to the blockchain
@app.route('/append_block', methods = ['POST'])
def add_remote_block():
    pending_block = request.get_json()
    block = Block(pending_block['block_id'],
                  pending_block['timestamp'],
                  pending_block['preceding_block_hash'],
                  pending_block['block_tx'])
    if blockchain.append_block(block, pending_block['hash']):
        return 'Block added to blockchain.', 201
    else:
        return 'Error: invalid block.', 400

# View unconfirmed transactions
@app.route('/pending_tx')
def get_pending_tx():
    pending_tx = json.dumps(blockchain.pending_tx)
    if pending_tx == '[]':
        return 'No pending transactions.'
    else:
        return pending_tx

# Check a longer chain exists, if so verify it before replacing the node's copy
def get_longest_blockchain():
    global blockchain
    longest_blockchain = None
    maximum_length = len(blockchain.blockchain)
    for node in settings.network:
        node_data = requests.get('http://{}/blockchain'.format(node))
        this_length = node_data.json()['length']
        this_blockchain = node_data.json()['chain']
        if (this_length > maximum_length
            and blockchain.verify_blockchain(this_blockchain)):
            maximum_length = this_length
            longest_blockchain = this_blockchain
    if longest_blockchain:
        blockchain = longest_blockchain
        return True
    return False

app.run(debug = True, port = 8000)
