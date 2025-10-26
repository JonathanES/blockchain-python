import hashlib
import json
import sys

# Defining a helper function that wraps our hashing algorithm
def hashMe(msg=""):
    if type(msg) != str:
        msg = json.dumps(msg, sort_keys=True)

    return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

if __name__ == "__main__":
    transaction = {'Jonathan': 174, 'Philippe': -174}
    print(hashMe(transaction))
