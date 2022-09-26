from array import array
from typing import List
import time   #for timestamp in header of each block
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
        # hash the value
        return hashlib.sha256(value.encode('utf8')).hexdigest()

    def __str__(self):
        return (str(self.hashValue))    # return the hash value


class MerkleTree:
    def __init__(self, array):
        self.buildTree(array)

    def buildTree(self, values):
        balance = []       # balance of the leafs
        account = []       # address of the leafs
        for line in values:     # split the values into address and balance
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
            account[i] + balance[i])) for i in range(len(account))]     # create leafs

        self.root = self._buildTree(Leafs)

    def _buildTree(self, Leafs):
        half = len(Leafs) // 2    # get half of the length of the Leafs
        # create new Leafs from pairs of Leafs
        if len(Leafs) == 2:
            # return the new Leafs
            return Leaf(Leafs[0], Leafs[1], None, None, Leaf.hash(Leafs[0].hashValue + Leafs[1].hashValue))
        elif len(Leafs) == 1:
            # return the new Leafs
            return Leaf(Leafs[0], None, (Leafs[0].address), (Leafs[0].balance), Leaf.hash(Leafs[0].hashValue))

        # recursive call
        left = self._buildTree(Leafs[:half])    # left child
        right = self._buildTree(Leafs[half:])   # right child
        address = None  # address of the new leaf
        balance = None  # balance of the new leaf
        if right:
            # hash the new Leafs
            hashValue = Leaf.hash(left.hashValue + right.hashValue)
        else:
            hashValue = Leaf.hash(left.hashValue)
        # return the new Leafs
        return Leaf(left, right, address, balance, hashValue)

    def getRootHash(self):      # returns the root hash
        return self.root.hashValue

    def printTree(self):           # prints the tree
        self._printTree(self.root)

    def _printTree(self, Leaf):
        if Leaf != None:
            if Leaf.left != None:
                print("Left: "+str(Leaf.left))      # prints left child
                print("Right: "+str(Leaf.right))    # prints right child
            else:
                print("Input")
            print("Hash Value: "+str(Leaf.hashValue))   # prints hash value
            print("Address: "+str(Leaf.address))    # prints address
            print("Balance: "+str(Leaf.balance))    # prints balance
            print("")
            self._printTree(Leaf.left)   # recursive call prints left child
            self._printTree(Leaf.right)  # recursive call prints right child

    # prints tree in order
    def printTreeInOrder(self):
        self._printTreeInOrder(self.root)

    def _printTreeInOrder(self, Leaf):
        if Leaf != None:
            # recursive call prints left child
            self._printTreeInOrder(Leaf.left)
            if Leaf.left != None:
                print("Left: "+str(Leaf.left))  # prints left child
                print("Right: "+str(Leaf.right))    # prints right child
            else:
                print("Input")
            print("Hash Value: "+str(Leaf.hashValue))   # prints hash value
            print("Address: "+str(Leaf.address))    # prints address
            print("Balance: "+str(Leaf.balance))    # prints balance
            print("")
            # recursive call prints right child
            self._printTreeInOrder(Leaf.right)

    # prints the tree graphically
    def printTreeGraphically(self):     # prints the tree graphically
        self._printTreeGraphically(self.root, 0)

    def _printTreeGraphically(self, node, level):
        if node is None:
            return
        # level increases indentation amount
        self._printTreeGraphically(node.right, level + 1)
        # print the node with indentation
        print(' ' * 4 * level + '->', node, end=" ")
        if node.left is None and node.right is None:
            print(f'\t[{node.address}, {node.balance}]')
        else:
            print()
        self._printTreeGraphically(node.left, level + 1)


def makeTree():
    try:
        # try - catch to try to open file
        file = open(sys.argv[1], "r")
    except:
        # if not a file, print this and exit program
        print("\nError: Please enter a valid text file.\n")
        sys.exit(0)    # exit program

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
    sys.exit(0)   # exit program
else:
    makeTree()  # make tree


#--------------------------Begin HW 4-------------------------------------

#• hash of the header of the previous block (zero for the initial genesis block)
#• hash of the root of the Merkle tree stored in the current block
#• a timestamp as an integer number of seconds since 1970-01-01 00:00:00 UTC (that is, Unix time)
#• difficulty target
#• nonce

class Block:
    def __init__(self, rootHash, timestamp, previous_hash, target, nonce):
        self.rootHash = rootHash   #to store index of block
        self.timestamp = time.time()
        self.previous_hash = previous_hash   #to store previous hash
        self.target = target   #for the difficulty target
        self.nonce = 0    

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        hash = hashlib.sha256()
        hash.update(
        str(self.rootHash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.target).encode('utf-8') +
        str(self.nonce).encode('utf-8')
        )
        return hash.hexdigest

    #You will need to find a nonce such that the nonce concatenated
    #with the root hash of the Merkle tree is hashed by SHA-256 to a value less than or equal to the specified
    #target. Please set your target such that the probability of success is 50%

class Blockchain:
    # setting the difficulty target 
    difficulty = 2 ** 256

    #initialize the blockchain
    def __init__(self):
        self.chain = []

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain.
        """
        genesis_block = Block(0, 0, [], 0, "0")  #create the genesis block
        genesis_block.hash = genesis_block.compute_hash() #hashing for the genesis block
        self.chain.append(genesis_block)  #adding the genesis block to the chain
    
    def printBlock():
        print("BEGIN BLOCK")
        print("BEGIN HEADER")
        print("END HEADER")
        print("s")

genesis_block = Block(0, 0, [], 0, "0")
print(genesis_block.previous_hash)