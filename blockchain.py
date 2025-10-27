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

    return {u'Jonathan': jonathanAmount, u'philippeAmount': philippeAmount}

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

if __name__ == "__main__":
    state = {'Jonathan': 1000, 'Philippe': 1000}  # Initial balances
    print(f"Initial State: {state}")

    # Test different transactions
    transaction1 = {'Jonathan': -800, 'Philippe': 800}
    transaction2 = {'Jonathan': 1500, 'Philippe': -1500}
    transaction3 = {'Jonathan': -400, 'Philippe': 600}
    transaction4 = {'Jonathan': -500, 'Philippe': 250, 'Kung': 250}
    # Check if transactions are valid
    print(f"Transaction: {transaction1}, Valid: {isValidTransaction(transaction1, state)}")
    print(f"Transaction: {transaction2}, Valid: {isValidTransaction(transaction2, state)}")
    print(f"Transaction: {transaction3}, Valid: {isValidTransaction(transaction3, state)}")
    print(f"Transaction: {transaction4}, Valid: {isValidTransaction(transaction4, state)}")

    if isValidTransaction(transaction4, state):
        state = updateState(transaction4, state)
    print(f"updated state: {state}")
