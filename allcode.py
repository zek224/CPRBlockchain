from typing import List
import hashlib
import sys
import os


class Leaf:
    def __init__(self, left, address: str, balance: int, right, hashValue: str, is_copied=False):  # is_copied is used to prevent infinite recursion    value = hash of content and content is the actual value
        self.left = left        # left child
        self.right = right      # right child
        self.address = address  # address of the leaf
        self.balance = balance  # balance of the leaf
        self.hashValue = hashValue # hash of the leaf
        self.is_copied = is_copied 

    @staticmethod
    def hash(val):
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __str__(self):
        return (str(self.value))

    def copy(self):
        return Leaf(self.left, self.right, self.value, self.content, True)


class MerkleTree:
    def __init__(self, values):
        self.buildTree(values)

    def buildTree(self, values):

        leaves = [Leaf(None, None, Leaf.hash(e), e) for e in values]            # makes leaves from all values in array
        if len(leaves) % 2 == 1:
            # duplicate last elem if odd number of elements
            leaves.append(leaves[-1].copy())
        self.root = self.buildTreeRec(leaves)           # builds tree from leaves

    def buildTreeRec(self, Leafs):
        if len(Leafs) % 2 == 1:
            # duplicate last elem if odd number of elements
            Leafs.append(Leafs[-1].copy())
        half = len(Leafs) // 2

        if len(Leafs) == 2:
            return Leaf(Leafs[0], Leafs[1], Leaf.hash(Leafs[0].value + Leafs[1].value), Leafs[0].content+"+"+Leafs[1].content)

        left: Leaf = self.buildTreeRec(Leafs[:half])
        right: Leaf = self.buildTreeRec(Leafs[half:])
        value: str = Leaf.hash(left.value + right.value)
        content: str = f'{left.content}+{right.content}'
        return Leaf(left, right, value, content)

    def getRootHash(self):
        return self.root.value

def makeTree():
    try:
        # try - catch to try to open file
        file = open(sys.argv[1])
    except:
        # if not a file, print this and exit program
        print("\nError: Please enter a valid text file.\n")
        sys.exit(0)
    elements = file.read()          # read entire file to a string
    array = elements.split()        # split into array based on space from string
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
