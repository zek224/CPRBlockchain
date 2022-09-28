from array import array
from time import time
from typing import List
import datetime as dt  # for timestamp in header of each block
import hashlib
import sys
import os
import random


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
            try:
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
            except:
                print("Error while building tree. Values at error point printed.")
                print(line.split(" ", 1))
                print(values)
                sys.exit(-1)

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

# --------------------------Begin HW 4-------------------------------------

# • hash of the header of the previous block (zero for the initial genesis block)
# • hash of the root of the Merkle tree stored in the current block
# • a timestamp as an integer number of seconds since 1970-01-01 00:00:00 UTC (that is, Unix time)
# • difficulty target
# • nonce


class Block:
    next = None

    def __init__(self, hash_prev, hash_root, timestamp, target, nonce):
        self.hash_prev = hash_prev  # hash of previous block
        self.hash_root = hash_root  # hash of root of Merkle tree
        self.timestamp = dt.datetime.now()  # timestamp
        self.target = 2 ** (256-50)  # for the difficulty target
        self.nonce = 0  # nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        hashes = hashlib.sha256(((str(self.hash_prev) + str(self.hash_root) + str(
            self.timestamp) + str(self.target) + str(self.nonce)).encode('utf-8'))).hexdigest()
        return hashes

    @staticmethod
    def create_genesis_block():
        """
        A function to manually create a genesis block.
        The previous hash is set to 0, the root of the hash is set to 0,
        the timestamp is set to the current time, and the nonce and target
        are set to 0.
        """

        return Block("0", "0", dt.datetime.now(), 0, 0)

    # def make_nounce(self):
        # """
        # A function that returns a nonce that is less than the target.
        # """
        # nonce = 0
        # while True:
        #     if int(self.compute_hash(), 16) <= self.target:
        #         break
        #     else:
        #         nonce += 1
        # return nonce
        # curr_nonce = random.randint(0, 2**64)
        # tries = 0
        # while True:
        #     tries += 1
        #     if int(hashlib.sha256((hex(curr_nonce) + self.hash_root.MerkleTree.getRootHash()).encode('utf-8')).hexdigest(), 16) < self.target:
        #         self.nonce = curr_nonce
        #         break
        #     else:
        #         curr_nonce = random.randint(0, 2**64)

# def mine(self, block):
#         for n in range(self.maxNonce):
#             if int(block.hash(), 16) <= self.target:
#                 self.add(block)
#                 print(block)
#                 break
#             else:
#                 block.nonce += 1
    # You will need to find a nonce such that the nonce concatenated
    # with the root hash of the Merkle tree is hashed by SHA-256 to a value less than or equal to the specified
    # target. Please set your target such that the probability of success is 50%


class Blockchain:
    max_nonce = 2**64
    geneis_block = Block.create_genesis_block()
    head = geneis_block

    def add_block(self, block):
        # next should be the next input file
        block.hash_prev = self.block.compute_hash()
        self.block.next = block
        self.block = self.block.next

    def set_nonce(self, block):
        for n in range(self.max_nonce):
            if int(block.compute_hash(), 16) < self.target:
                self.add_block(block)
                break
            else:
                block.nonce += 1

    def print_blockchain(self):
        genesis_block = [Block.create_genesis_block()]
        print("Begin Block\n")
        print("Begin Header\n")
        print("Genesis Block\n")
        print("Hash: "+genesis_block[0].compute_hash() + "\n")
        print("Hash of root: " + genesis_block[0].hash_prev + "\n")
        print("Timestamp: " + str(genesis_block[0].timestamp) + "\n")
        print("Target: " + str(genesis_block[0].target) + "\n")
        print("Nonce: " + str(genesis_block[0].make_nounce()) + "\n")
        print("End Header\n")
        print("End Block\n")
        print("------------------------\n")

    # # initialize the blockchain
    # def __init__(self):
    #     self.chain = list()
    #     genesis_block = self.createblocks("0", "0", dt.datetime.now(), 0, 0)
    #     self.chain.append(genesis_block)

    # def createblocks(self, hash_prev, hash_root, timestamp, target, nonce):
    #     self.hash_prev = hash_prev
    #     self.hash_roor = hash_root
    #     self.timestamp = dt.dataTime.now()
    #     self.target = target
    #     self.nonce = nonce


#         # genesis_block = Block("Genesis")
#         # timestamp = datetime.datetime.now()
#         # hash_prev = 0
#         # return (Block(genesis_block, hash_prev, 0, timestamp, 0, 0))

#         # genesis_block = Block("Genesis")
#         # # genesis_block = Block(0, 0, [], 0, "0")  # create the genesis block
#         # # genesis_block.hash = genesis_block.compute_hash()  # hashing for the genesis block
#         # # # adding the genesis block to the chain
#         # # self.chain.append(genesis_block)

# read in each argument in argv adn append it to an array. then we have array of all filesname / paths to files.


# reads in fileInputs, which is the list of paths to the different input files
def makeTree(fileInputs):
    print("\nInputted files: ", fileInputs, "\n")
    for files in fileInputs:
        try:
            # try - catch to try to open file
            file = open(files, "r")
            print('File opened')
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


# if "python3 allcode.py" only, then prompt for file inputs where user input starts
size=0
if len(sys.argv) == 1:
    print("\nMake a selection \n1. Enter multiple file names \n2. Enter a folder (all files in folder will be entered) \n3. Exit\n")
    selectionInput = input("Selection: ")
    if (selectionInput == "1"):       # multiple file names
        print("Enter a single file name one at a time (enter 0 to exit): ")
        fileNames = []      # array to make tree
        fileName = ""       # file location var
        loop = True         # infinite loop unless 0 is entered
        while (loop):
            if (fileName == "0"):        # ends loop
                loop = False
            else:                       # enter values to be added to array. 0 will still be entered at the end, but is removed below
                fileName = input("\nEnter the path to a file (0 to exit): ")
                fileNames.append(fileName)
        # remove last element from array (which would be 0 to exit loop but also got appended to array)
        fileNames.pop()
        makeTree(fileNames)
    elif (selectionInput == "2"):     # folder
        # prompt for folder name
        print("Enter the name of the folder (must be in same directory): ")
        folderName = input("Folder Name: ")    # get folder name
        dirList = os.listdir(folderName)    # get list of files in folder
        size=len(dirList)
        # add folder name to each file name
        dirList = ["{}/{}".format(folderName, i) for i in dirList]
        makeTree(dirList)   # make tree from list of files
    else:
        print("Exiting...")    # exit program
        sys.exit(0)    # exit program

# Makes tree if more than 1 argv
if len(sys.argv) > 1:
    # make tree for every file by making an array of file inputs for the tree via argv (ignores argv[0] with is python3 and argv[1] which is program name, takes elements onwards)
    size=len(sys.argv)-2
    makeTree(sys.argv[1:])

#def __init__(self, hash_prev, hash_root, timestamp, target, nonce):

blockchain = Blockchain()
for n in range(size):
    blockchain.set_nonce(Block)

while blockchain.head != None:
    print(blockchain.head)
    blockchain.head = blockchain.head.next
