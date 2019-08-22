# Python Blockchain: immutable decentralised data storage

A public blockchain and GUI allowing users to store and share information that can't be tampered with or repudiated.

The architecture is based on the [IBM Blockchain](https://www.ibm.com/blockchain), however Proof of Work (PoW) is used as a consensus algorithm instead of IBM SE. The PoW structure is adapted from Kansal (2018) with SHA256 as the cryptographic hash function.

## Requirements

- Python 3

## Install

```
pip3 install flask requests
```

## Run

Open two terminal windows and navigate to the project folder in both.

Start the node in one window:

```
python3 node.py
```

Run the GUI in the other window:

```
python3 gui.py
```

You can now view and interact with the blockchain at [http://localhost:5000](http://localhost:5000).

Blockchain difficulty can be adjusted in `settings.py` (a higher number means a more expensive computation). For larger-scale implementations, please modify the confirm() function to split transactions appropriately and security audit the code.
