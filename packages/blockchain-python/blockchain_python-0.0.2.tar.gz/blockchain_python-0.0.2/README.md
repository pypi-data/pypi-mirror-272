# Blockchain-Python

Blockchain-Python is a Python library for creating a basic blockchain structure.

## Installation

You can install Blockchain-Python using pip:

```bash
pip install blockchain-python
```


```python
import blockchain_python as bcp

# Initialize Blockchain
blockchain = bcp.Blockchain()

# Add a block with transaction data
blockchain.add_block('transaction 1')

# Read the first block
blockchain.read_block(0)

# Show all blocks
blockchain.show_all_blocks()
```

## Example

```python
import blockchain_python as bcp

# Initialize Blockchain
blockchain = bcp.Blockchain()

# Add multiple blocks
blockchain.add_block('transaction 1')
blockchain.add_block('transaction 2')
blockchain.add_block('transaction 3')

# Read the second block
blockchain.read_block(1)

# Show all blocks
blockchain.show_all_blocks()
```

