# Immutable, Trustless Record-keeping and Sharing with Python

This repository contains code for a public blockchain and GUI allowing users to store and share information that can't be tampered with or repudiated.

The distributed ledger is based on the [IBM Blockchain](https://www.ibm.com/blockchain) structure, however Proof of Work (PoW) is used as a consensus algorithm instead of IBM SE. The PoW structure is adapted from Kansal (2018) with SHA256 as the cryptographic hash function.

[Flask](http://flask.pocoo.org/) is used for the front end and is needed to run the app.

For larger-scale implementations, please modify the confirm() function to
split transactions appropriately.
