from array import array
from typing import List
import hashlib
import sys
import os


class Leaf:
    # is_copied is used to prevent infinite recursion
    def __init__(self, left, right, address, balance, hashValue, is_copied=False):
        self.left = left        # left child
        self.right = right      # right child
        self.address = address  # address of the leaf
        self.balance = balance  # balance of the leaf
        self.hashValue = hashValue  # hash of the leaf
        self.is_copied = is_copied

    @staticmethod
    def hash(value):
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def __str__(self):
        return (str(self.hashValue))

    # copys a leaf and returns the copy
    def copy(self):
        return Leaf(self.left, self.right, self.address, self.balance, self.hashValue, True)


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
            account.append(acct)    # add address to account array
            balance.append(bal)     # add balance to balance array

        # create leafs from the values
        Leafs = [Leaf(None, None, account[i], balance[i], Leaf.hash(
            account[i] + balance[i])) for i in range(len(account))]    # make leafs from input array

        if len(Leafs) % 2 == 1:
            # duplicate last elem if odd number of elements
            Leafs.append(Leafs[-1].copy())  # copy last element
        # builds tree from leaves
        self.root = self._buildTree(Leafs)

    def _buildTree(self, Leafs):
        if len(Leafs) % 2 == 1:
            # duplicate last elem if odd number of elements
            Leafs.append(Leafs[-1].copy())  # copy last element
        half = len(Leafs) // 2  # half of the length of Leafs

        # create new Leafs from pairs of Leafs
        if len(Leafs) == 2:
            # return root
            return Leaf(Leafs[0], Leafs[1], (Leafs[0].address + " + " + Leafs[1].address), (Leafs[0].balance + " + " + Leafs[1].balance), Leaf.hash(Leafs[0].hashValue + Leafs[1].hashValue))

        left = self.buildTreeRec(Leafs[:half])   # left child
        right = self.buildTreeRec(Leafs[half:])     # right child
        address = left.address + " + " + right.address  # address of the node
        balance = left.balance + " + " + right.balance  # balance of the node
        hashValue = Leaf.hash(
            left.hashValue + right.hashValue)  # hash of the node
        return Leaf(left, right, address, balance, hashValue)  # return node

    def getRootHash(self):
        return self.root.hashValue  # return root hash

    def printTree(self):
        self._printTree(self.root)
    
    def _printTree(self, Leaf: Leaf):
        if Leaf != None:
            if Leaf.left != None:
                print("Left: "+str(Leaf.left))
                print("Right: "+str(Leaf.right))
            else:
                print("Input")
            if Leaf.is_copied:
                print('(Padding)')
            print("Hash Value: "+str(Leaf.hashValue))
            print("Address: "+str(Leaf.address))
            print("Balance: "+str(Leaf.balance))
            print("")
            self._printTree(Leaf.left)
            self._printTree(Leaf.right)
        


def makeTree():
    try:
        # try - catch to try to open file
        file = open(sys.argv[1], "r")
    except:
        # if not a file, print this and exit program
        print("\nError: Please enter a valid text file.\n")
        sys.exit(0)  # exit program

    array = []

    for line in file:
        array.append(line.strip())  # add each line to array

    tree = MerkleTree(array)        # make tree from input array ()
    print("Root Hash: " + tree.getRootHash() + "\n")
    tree.printTree()


# Help Message is argv[1] (path to input file) doesn't exist
if len(sys.argv) != 2:
    # Exits program if this statement is true
    print("\nUsage: 'python3 merkleTree.py <path/to/file.txt>\n")
    sys.exit(0)  # exit program
else:
    makeTree()  # make tree from input file


# https://github.com/onuratakan/mixmerkletree
