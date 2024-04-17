import json
import hashlib
import os
import time

# Define constants
TARGET_DIFFICULTY = "0000ffff00000000000000000000000000000000000000000000000000000000"
# Function to validate transaction
def validate_transaction(transaction):
    # Placeholder for transaction validation logic
    # You need to implement this based on Bitcoin transaction validation rules

    # Check if transaction has required fields
    if "txid" not in transaction or "inputs" not in transaction or "outputs" not in transaction:
        return False

    # Validate inputs
    for input in transaction["inputs"]:
        if "txid" not in input or "index" not in input or "signature" not in input:
            return False
        # Additional validation checks, such as verifying if the input is unspent

    # Validate outputs
    for output in transaction["outputs"]:
        if "index" not in output or "amount" not in output or "address" not in output:
            return False
    return True

# Function to calculate merkle root
def calculate_merkle_root(transactions):
    txids = [transaction["txid"] for transaction in transactions]
    while len(txids) > 1:
        if len(txids) % 2 != 0:
            txids.append(txids[-1])  # Duplicate the last transaction ID if odd number of transactions
        temp = []
        for i in range(0, len(txids), 2):
            concat = txids[i] + txids[i+1]
            concat_hash = hashlib.sha256(concat.encode()).hexdigest()
            temp.append(concat_hash)
        txids = temp

    return txids[0]


# Function to mine block
def mine_block(transactions):
    # Create block header
    block_header = {
        "version": 1,
        "prev_block_hash": "0000000000000000000000000000000000000000000000000000000000000000",  # Placeholder for previous block hash
        "merkle_root": calculate_merkle_root(transactions),
        "timestamp": int(time.time()),
        "difficulty_target": TARGET_DIFFICULTY,
        "nonce": 0
    }

    # Create coinbase transaction
    coinbase_transaction = {
        "txid": "coinbase_txid",  # Placeholder for coinbase transaction ID
        "inputs": [],
        "outputs": [
            {"index": 0, "amount": 50, "address": "miner_address"}  # Placeholder for coinbase output
        ]
    }

    # Include coinbase transaction in list of transactions
    block_transactions = [coinbase_transaction]

    # Iterate through transactions and include valid ones in the block
    for transaction in transactions:
        if validate_transaction(transaction):
            block_transactions.append(transaction)

    # Mine block
    block_header = mine_block_header(block_header)

    # Return block header and list of transaction IDs
    return block_header, block_transactions

# Function to mine block header
def mine_block_header(block_header):
    while True:
        # Serialize block header
        block_header_string = json.dumps(block_header, sort_keys=True)

        # Calculate block hash
        block_hash = hashlib.sha256(block_header_string.encode()).hexdigest()

        # Check if block hash meets target difficulty
        if block_hash < TARGET_DIFFICULTY:
            block_header["hash"] = block_hash
            break
        else:
            # Increment nonce and try again
            block_header["nonce"] += 1

    return block_header

# Function to write output to file
def write_output(block_header, transactions):
    with open("output.txt", "w") as f:
        f.write(json.dumps(block_header) + "\n")
        f.write(json.dumps(transactions[0]) + "\n")  # Serialize coinbase transaction
        for transaction in transactions[1:]:
            f.write(transaction["txid"] + "\n")  # Write transaction ID

# Main function
def main():
    mempool_path = "./mempool"
    transactions = []

    # Load transactions from mempool
    for filename in os.listdir(mempool_path):
        with open(os.path.join(mempool_path, filename), "r") as file:
            transaction = json.load(file)
            transactions.append(transaction)

    # Mine block
    block_header, block_transactions = mine_block(transactions)

    # Write output to file
    write_output(block_header, block_transactions)

if __name__ == "__main__":
    main()
