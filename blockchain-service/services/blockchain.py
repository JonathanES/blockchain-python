import hashlib
import json
import sys
import random
random.seed(2) # Sets a fixed seed so results are predictable every time we run the code

# Defining a helper function that wraps our hashing algorithm
def hashMe(msg=""):
    if type(msg) != str:
        msg = json.dumps(msg, sort_keys=True)

    return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()
 
def makeTransaction(maxValue = 1000):
    sign = int(random.getrandbits(1)) * 2 - 1 # Randomly choose between -1 or 1 (whether Jonathan pays Philippe or Philippe pays Jonathan)
    amount = random.randint(1, maxValue)
    jonathanAmount = sign * amount
    philippeAmount = -1 * jonathanAmount

    return {u'Jonathan': jonathanAmount, u'Philippe': philippeAmount}

def updateState(transaction, state):
    """
    Inputs:
        transaction: a dictionary with keys Jonathan and Philippe, and values the amount of money that they are sending to each other.
        state: a dictionary with keys Jonathan and Philippe, and values their current balance

    Outputs:
        state: a dictionary with keys Jonathan and Philippe, and values their new balance
        ** Additional users will be added to state if they are not already present
    """
    state = state.copy()

    for key in transaction.keys():
        state[key] = state.get(key, 0) + transaction[key]
    return state

def isValidTransaction(transaction, state):
    """
    Inputs:
        transaction: a dictionary with keys Jonathan and Philippe or anyone else, and values the amount of money they are sending to each other
        state: a dictionary with keys Jonathan and Philippe or anyone else, and values their current balance

    Output:
        True if the transaction is valid, False otherwise
    """

    if sum(transaction.values()) != 0:
        return False
    for key in transaction.keys():
        account_balance = state.get(key, 0)
        if account_balance + transaction[key] < 0:
            return False
    
    return True

def initBlockChain(state):
    genesisBlockTransactions = [state]
    genesisBlockContents = {
            'blockNumber': 0,
            'parentHash': None,
            'transactionCount': 1,
            'transactions': genesisBlockTransactions
    }
    genesisHash = hashMe(genesisBlockContents)
    genesisBlock = {'hash': genesisHash, 'contents': genesisBlockContents}
    return [genesisBlock]


def makeBlock(transactions, chain):
    """
    Inputs:
        transactions: a list of transactions to include in the block
        chain: the current blockchain (a list of existing blocks)
    Outputs:
        block: a dictionary representing the new block, including it's hash and its content
    """
    parentBlock = chain[-1]
    parentHash = parentBlock["hash"]
    blockNumber = parentBlock["contents"]["blockNumber"] + 1
    transactionCount = len(transactions)

    blockContents = {
        "blockNumber": blockNumber,
        "parentHash": parentHash,
        "transactionCount": transactionCount,
        "transactions": transactions
    }
    
    blockHash = hashMe(blockContents)

    block = {"hash": blockHash, "contents": blockContents}
    return block

def checkBlockHash(block):
    expectedHash = hashMe(block["contents"])
    if expectedHash != block["hash"]:
        raise Exception(f"Hash does not match for block {block["contents"]["blockNumber"]}. Expected {expectedHash}, got {block["hash"]}")
    return

def checkBlockValidity(block, parent, state):
    parentNumber = parent["contents"]["blockNumber"]
    parentHash = parent["hash"]
    blockNumber = block["contents"]["blockNumber"]

    for transaction in block["contents"]["transactions"]:
        if isValidTransaction(transaction, state):
            state = updateState(transaction, state)
        else:
            raise Exception(f"Transaction {transaction} in block {blockNumber}")
    checkBlockHash(block)

    if blockNumber != parentNumber + 1:
        raise Exception(f"Block {blockNumber} is not the next block after {parentNumber}")
    
    if block["contents"]["parentHash"] != parentHash:
        raise Exception(f"Block {blockNumber} does not have the correct parent hash. Expected {parentHash}, got {block["contents"]["parentHash"]}")
    
    return state

def checkChain(chain):
    if type(chain) == str:
        try:
            chain = json.loads(chain)
            assert type(chain) == list
        except:
            return False
    elif type(chain) != list:
        return False
    
    state = {}

    for transaction in chain[0]["contents"]["transactions"]:
        state = updateState(transaction, state)
    
    checkBlockHash(chain[0])
    parent = chain[0]

    for block in chain[1:]:
        state = checkBlockValidity(block, parent, state)
        parent = block
    return state
if __name__ == "__main__":
    state = {'Jonathan': 1000, 'Philippe': 1000}  # Initial balances
    chain = initBlockChain(state)
    print(f"Initial State: {state}")
    transactionBuffer = [makeTransaction() for _ in range(100)]

    blockSizeLimit = 10 # maximum number of transactions allowed in a block
    while len(transactionBuffer):
        transactionList = []
        while len(transactionList) < blockSizeLimit:
            if not transactionBuffer:
                break
            transaction = transactionBuffer.pop()

            if isValidTransaction(transaction, state):
                transactionList.append(transaction)
                state = updateState(transaction, state)
            else:
                print(f"Transaction {transaction} is invalid")
                continue
        newBlock = makeBlock(transactionList, chain)
        chain.append(newBlock)
        print(f"Block {newBlock['contents']['blockNumber']} created with {len(transactionList)} transactions")
    print(chain)
    state = checkChain(chain)
    print(state)