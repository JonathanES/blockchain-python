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

if __name__ == "__main__":
    transactionBuffer = [makeTransaction() for _ in range(100)]
    print(transactionBuffer)
