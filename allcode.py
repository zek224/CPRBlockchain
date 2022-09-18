from array import array
from typing import List
import hashlib
import sys
import os


class Leaf:
    def __init__(self, left, right, address: str, balance: int, hashValue: str, is_copied=False):  # is_copied is used to prevent infinite recursion    value = hash of content and content is the actual value
        self.left = left        # left child
        self.right = right      # right child
        self.address = address  # address of the leaf
        self.balance = balance  # balance of the leaf
        self.hashValue = hashValue # hash of the leaf
        self.is_copied = is_copied 

    @staticmethod
    def hash(value):
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def __str__(self):
        return (str(self.value))

    def copy(self):
        return Leaf(self.left, self.right, self.address, self.balance, self.hashValue, True)


class MerkleTree:
    def __init__(self, array):
        self.buildTree(array)

    def buildTree(self, values):

        # seperate elements in values by space into two variables
        # values = [address, balance]

        balance: int = []
        account: str = []

        for line in values:
            acct = ""
            bal = 0
            acct, bal = line.split(' ', 1) # split line into two variables
            account.append(acct)
            balance.append(bal)

        print(account)

        Leafs = [Leaf(None, None, account[i], balance[i], Leaf.hash(account[i] + balance[i])) for i in range(len(account))]

        # leaves = [Leaf(None, None, Leaf.hash(e), e) for e in values]            # makes leaves from all values in array
        if len(Leafs) % 2 == 1:
            # duplicate last elem if odd number of elements
            Leafs.append(Leafs[-1].copy())
        self.root = self.buildTreeRec(Leafs)           # builds tree from leaves

    def buildTreeRec(self, Leafs):
        if len(Leafs) % 2 == 1:
            # duplicate last elem if odd number of elements
            Leafs.append(Leafs[-1].copy())
        half = len(Leafs) // 2

        if len(Leafs) == 2:
            return Leaf(Leafs[0], Leafs[1], Leaf[0].address + " + " + Leaf[1].address, Leaf[0].balance + " + " + Leaf[1].balance, Leaf.hash(Leafs[0].hashValue + Leafs[1].hashValue))
            #return Leaf(Leafs[0], Leafs[1], Leaf.hash(Leafs[0].value + Leafs[1].value), Leafs[0].content+"+"+Leafs[1].content)

        left: Leaf = self.buildTreeRec(Leafs[:half])
        right: Leaf = self.buildTreeRec(Leafs[half:])
        address = left.address + " + " + right.address
        balance = left.balance + " + " + right.balance
        hashValue: str = Leaf.hash(left.hashValue + right.hashValue)
        #content: str = f'{left.content}+{right.content}'
        return Leaf(left, right, address, balance, hashValue)

    def getRootHash(self):
        return self.root.value

def makeTree():
    try:
        # try - catch to try to open file
        file = open(sys.argv[1], "r")
    except:
        # if not a file, print this and exit program
        print("\nError: Please enter a valid text file.\n")
        sys.exit(0)

    array = []


    # lines = file.readlines()
    # file.close()
    # split1 = lines[0].strip().split(" ")
    # split2 = lines[1].strip().split(" ") 
    # print(split1)
    # print(split2)
    for line in file:
        array.append(line.strip())  # add each line to array

    #print(array)
    #elements = file.read()          # read entire file to a string
    #array = elements.split()        # split into array based on space from string
    tree = MerkleTree(array)        # make tree from input array ()
    print("Root Hash: " + tree.getRootHash() + "\n")

# Help Message is argv[1] (path to input file) doesn't exist
if len(sys.argv) != 2:
    # Exits program if this statement is true
    print("\nUsage: 'python3 merkleTree.py <path/to/file.txt>\n")
    sys.exit(0)
else:
    makeTree()


# https://github.com/onuratakan/mixmerkletree
