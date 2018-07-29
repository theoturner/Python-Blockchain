# Python Blockchain: immutable decentralised data storage

A public blockchain + GUI allowing users to store and share information that can't be tampered with or repudiated.

The architecture his based on the [IBM Blockchain](https://www.ibm.com/blockchain), however Proof of Work (PoW) is used as a consensus algorithm instead of IBM SE. The PoW structure is adapted from Kansal (2018) with SHA256 as the cryptographic hash function.

[Flask](http://flask.pocoo.org/) is used for the front end and is needed to run the app. Flask allows for RESTful interaction with nodes.


## How to use the Python Blockchain

Install [Python 3](https://www.python.org/downloads/), version 3.4 or later.

Open a terminal window, then use pip3 to install Flask and requests:

```sh
>>> pip3 install flask
>>> pip3 install requests
```

Open two terminal windows and navigate to your project folder in both.

Start the node in one window:

```sh
>>> python3 node.py
```

Run the GUI in the other window:

```sh
>>> python3 gui.py
```

You can now view and interact with the blockchain at [http://localhost:5000](http://localhost:5000).

For larger-scale implementations, please modify the confirm() function to
split transactions appropriately and security audit the code.
