import json
import datetime
import requests
from app import app
from flask import request, render_template, redirect

host = 'http://127.0.0.1:8000'
ordered_tx = []

# Load full blockchain by tx and sort by time (adapted from from Kansal 2018)
def get_full_blockchain():
    blockchain_source = requests.get('{}/blockchain'.format(host))
    if blockchain_source.status_code == 200:
        global ordered_tx
        all_tx = []
        blockchain = json.loads(blockchain_source.content)
        for block in blockchain['chain']:
            for tx in block['block_tx']:
                tx['block_id'] = block['block_id']
                tx['hash'] = block['preceding_block_hash']
                all_tx.append(tx)
        ordered_tx = sorted(all_tx, key = lambda k: k['timestamp'],
                            reverse = True)

def readable_time(time):
    return datetime.datetime.fromtimestamp(time).strftime('%H:%M on %d %b %Y')

@app.route('/')
def index():
    get_full_blockchain()
    return render_template('index.html',
                           title = 'Python Blockchain: immutable '
                                   'decentralised data storage',
                           ordered_tx = ordered_tx,
                           host = host,
                           time = readable_time)

# Compose tx using form
@app.route('/submit', methods = ['POST'])
def compose_tx():
    requests.post('{}/submit_tx'.format(host),
                  json = {'user': request.form['user'],
                          'data': request.form['data']},
                  headers = {'Content-type': 'application/json'})
    return redirect('/')
