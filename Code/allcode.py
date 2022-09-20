from array import array
from typing import List
import hashlib
import sys
import os


class Leaf:
    def __init__(self, left, right, address, balance, hashValue):
        self.left = left        # left child
        self.right = right      # right child
        self.address = address  # address of the leaf
        self.balance = balance  # balance of the leaf
        self.hashValue = hashValue  # hash of the leaf

    @staticmethod
    def hash(value):
        return hashlib.sha256(value.encode('utf8')).hexdigest() # hash the value

    def __str__(self):
        return (str(self.hashValue))


class MerkleTree:
    def __init__(self, array):
        self.buildTree(array)

    def buildTree(self, values):
        balance = []       # balance of the leafs
        account = []       # address of the leafs
        for line in values:     # sploit the values into address and balance
            acct = ""
            bal = 0
            acct, bal = line.split(' ', 1)  # split line into two variables
            if (len(acct) != 40):        # check if address is 40 characters
                print("\nError: Invalid address at input line " +
                      str(values.index(line) + 1) + ".\n")
                # sys.exit(0)
            if (not bal.isdigit()):      # check if balance is a number
                print("\nError: Invalid balance at input line " +
                      str(values.index(line) + 1) + ".\n")
                # sys.exit(0)
            account.append(acct)    # add address to account array
            balance.append(bal)     # add balance to balance array

        # create leafs from the values
        Leafs = [Leaf(None, None, account[i], balance[i], Leaf.hash(
            account[i] + balance[i])) for i in range(len(account))]

        self.root = self._buildTree(Leafs)  # build tree from leafs

    def _buildTree(self, Leafs):
        half = len(Leafs) // 2  # get half of the length of the Leafs array
        # create new Leafs from pairs of Leafs
        if len(Leafs) == 2:
            # return new Leafs
            return Leaf(Leafs[0], Leafs[1], None, None, Leaf.hash(Leafs[0].hashValue + Leafs[1].hashValue))
        elif len(Leafs) == 1:
            # return new Leafs
            return Leaf(Leafs[0], None, (Leafs[0].address), (Leafs[0].balance), Leaf.hash(Leafs[0].hashValue))

        # recursive call
        left = self._buildTree(Leafs[:half])    # left child
        right = self._buildTree(Leafs[half:])   # right child
        address = None  # address of the new leaf
        balance = None  # balance of the new leaf
        if right:
            # hash of the new leaf
            hashValue = Leaf.hash(left.hashValue + right.hashValue)
        else:
            hashValue = Leaf.hash(left.hashValue)
        # return new Leafs
        return Leaf(left, right, address, balance, hashValue)

    def getRootHash(self):
        return self.root.hashValue


def makeTree():
    try:
        # try - catch to try to open file
        file = open(sys.argv[1], "r")
    except:
        # if not a file, print this and exit program
        print("\nError: Please enter a valid text file.\n")
        sys.exit(0)

    array = []

    for line in file:
        array.append(line.strip())  # add each line to array

    tree = MerkleTree(array)        # make tree from input array ()
    print("Root Hash: " + tree.getRootHash() + "\n")
    # tree.printTreeGraphically()


# Help Message is argv[1] (path to input file) doesn't exist
if len(sys.argv) != 2:
    # Exits program if this statement is true
    print("\nUsage: 'python3 merkleTree.py <path/to/file.txt>\n")
    sys.exit(0)     # exit program
else:
    makeTree()  # make tree from input file
