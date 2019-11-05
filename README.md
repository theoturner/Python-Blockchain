# Python Blockchain: immutable decentralised data storage

A public blockchain and GUI allowing users to store and share information that can't be tampered with or repudiated.

The architecture is based on the [IBM Blockchain](https://www.ibm.com/blockchain), however Proof of Work (PoW) is used as a consensus algorithm instead of IBM SE. The PoW structure is adapted from Kansal (2018) with SHA256 as the cryptographic hash function.

This software is licensed under the MIT software license (see LICENSE file). Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

The author of this software makes no representation or guarantee that this software (including any third-party libraries) will perform as intended or will be free of errors, bugs or faulty code. The software may fail which could completely or partially limit functionality or compromise computer systems. If you use or implement the software, you do so at your own risk. In no event will the author of this software be liable to any party for any damages whatsoever, even if it had been advised of the possibility of damage.

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
