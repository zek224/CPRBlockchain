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
    # we must be entering in a filename into MerkleTree() somewhere
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
                print("Error while building tree. Values at error point printed.") # no clue yet, its not an error with the inputs
                print("Line: ", line)
                print(line.split(" ", 1))
                sys.exit(-1)

        # create leafs from the values
        Leafs = [Leaf(None, None, account[i], balance[i], Leaf.hash(
            account[i] + balance[i])) for i in range(len(account))]     # create leafs

        self.root = self._buildTree(Leafs)  # build the tree

    def _buildTree(self, Leafs):
        half = len(Leafs) // 2    # get half of the length of the Leafs
        # create new Leafs from pairs of Leafs
        if len(Leafs) == 2:
            # return the new Leafs
            return Leaf(Leafs[0], Leafs[1], None, None, Leaf.hash(Leafs[0].hashValue + Leafs[1].hashValue)) # create new Leafs
        elif len(Leafs) == 1:
            # return the new Leafs
            return Leaf(Leafs[0], None, (Leafs[0].address), (Leafs[0].balance), Leaf.hash(Leafs[0].hashValue))  # create new Leafs

        # recursive call
        left = self._buildTree(Leafs[:half])    # left child
        right = self._buildTree(Leafs[half:])   # right child
        address = None  # address of the new leaf
        balance = None  # balance of the new leaf
        if right:
            # hash the new Leafs
            hashValue = Leaf.hash(left.hashValue + right.hashValue) # hash the new Leafs
        else:
            hashValue = Leaf.hash(left.hashValue)   # hash the new Leafs
        # return the new Leafs
        return Leaf(left, right, address, balance, hashValue)   # create new Leafs

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
            print(f'\t[{node.address}, {node.balance}]')    # prints address and balance
        else:
            print()
        self._printTreeGraphically(node.left, level + 1)    # recursive call

# ------------------------------Begin HW 4-------------------------------------

# • hash of the header of the previous block (zero for the initial genesis block)
# • hash of the root of the Merkle tree stored in the current block
# • a timestamp as an integer number of seconds since 1970-01-01 00:00:00 UTC (that is, Unix time)
# • difficulty target
# • nonce

class Block:

    def __init__(self, hash_prev, hash_root):
        self.hash_prev = hash_prev  # hash of previous block
        self.hash_root = hash_root  # hash of root of Merkle tree
        self.timestamp = dt.datetime.now()  # timestamp
        self.target = 2 ** 255  # for the difficulty target
        self.nonce = 0  # nonce
        self.nonce_max = 2 ** 32    # max nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        hashes = hashlib.sha256(((str(self.hash_prev) + str(self.hash_root) + str(
            self.timestamp) + str(self.target) + str(self.nonce)).encode('utf-8'))).hexdigest() # hash the block
        return hashes   # return the hash

    def set_nonce(self):
        testNonce = random.randint(0, 2**32)   # random target

        for n in range(self.nonce_max):
            if int(self.compute_hash(), 16) < self.target:
                self.nonce = testNonce   # set max nonce
                break   # break
            else:
                self.nonce = random.randint(0, 2**32)    # set nonce
        return self.nonce

class Blockchain ():
    def __init__(self):
        self.nonce_max = 2 ** 32    # max nonce
        self.target = 2 ** 255  # target

    def set_nonce(self, block):
        object1 = Block(block.hash_prev, block.hash_root)   # create a new block
        target = random.randint(0, 2**32)   # random target

        for n in range(self.nonce_max):
            if int(object1.compute_hash(), 16) < self.target:
                self.nonce_max = target   # set max nonce
                break   # break
            else:
                object1.nonce = random.randint(0, 2**32)    # set nonce

    def create_genesis_block(self):
        return Block("0", "0")  # create genesis block

# read in each rgument in argv adn append it to an array. then we have array of all filesname / paths to files.

# reads in fileInputs, which is the list of paths to the different input files
def makeTree(fileInputs):
    print("\nInputted files: ", fileInputs, "\n")   # print inputted files
    array = []  # array of all the transactions
    for files in fileInputs:
        try:
            # try - catch to try to open file
            file = open(files, "r")
            print('File opened')
        except:
            # if not a file, print this and exit program
            print("\nError: Please enter a valid text file.\n")
            sys.exit(0)    # exit program

        for line in file:
            array.append(line.strip())  # add each line to array

        tree = MerkleTree(array)        # make tree from input array ()
        print("Root Hash: " + tree.getRootHash() + "\n")
        file.close()
        # tree.printTreeGraphically()
    return array


# if "python3 allcode.py" only, then prompt for file inputs where user input starts
size = 0
fileNames = []
if len(sys.argv) == 1:
    print("\nMake a selection \n1. Enter multiple file names \n2. Enter a folder (all files in folder will be entered) \n3. Exit\n")
    selectionInput = input("Selection: ")
    if (selectionInput == "1"):       # multiple file names
        print("Enter a single file name one at a time (enter 0 to exit): ")
        #fileNames = []      # array to make tree
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
        # remove empty strings from array
        fileNames = list(filter(None, fileNames))
        length = len(fileNames)
        makeTree(fileNames)
    elif (selectionInput == "2"):     # folder
        # prompt for folder name
        print("Enter the name of the folder (must be in same directory): ")
        folderName = input("Folder Name: ")    # get folder name
        dirList = os.listdir(folderName)    # get list of files in folder
        #size = len(dirList)
        # add folder name to each file name
        dirList = ["{}/{}".format(folderName, i) for i in dirList]
        length = len(dirList)
        fileNames = dirList
        makeTree(dirList)   # make tree from list of files
    else:
        print("Exiting...")    # exit program
        sys.exit(0)    # exit program

# Makes tree if more than 1 argv
if len(sys.argv) > 1:
    # make tree for every file by making an array of file inputs for the tree via argv (ignores argv[0] with is python3 and argv[1] which is program name, takes elements onwards)
    makeTree(sys.argv[1:])

object2 = Blockchain()  # create blockchain object
block = None    # block object
blocksList = []    # list of blocks

for n in range(length):
    if n == 0:
        block = object2.create_genesis_block()  # create genesis block
        object2.set_nonce(block)    # set nonce
    elif(selectionInput == "2"): 
        tree = makeTree(dirList)    # make tree
        merkletree = MerkleTree(tree)    # this should be array of contents of the file, not file names    
        block = Block(blocksList[-1].compute_hash(), merkletree.getRootHash())  # create block
    else:
        tree = makeTree(fileNames)  # make tree
        merkletree = MerkleTree(tree)    # this should be array of contents of the file, not file names    
        block = Block(blocksList[-1].compute_hash(), merkletree.getRootHash())
    blocksList.append(block)    # add block to list of blocks

#print files in given format
for i in range(len(blocksList)):
    print("Begin Block\n")          
    print("Begin Header\n") 
    print("Hash: "+blocksList[i].compute_hash() + "\n")
    print("Hash of root: " + blocksList[i].hash_prev + "\n")
    print("Timestamp: " + str(blocksList[i].timestamp) + "\n")
    print("Target: " + str(blocksList[i].target) + "\n")
    print("Nonce: " + str(blocksList[i].set_nonce()) + "\n")
    print("END HEADER\n")
    print("END BLOCK\n")
    print("------------------------\n")

os.mkdir("output")

for i in range(len(blocksList)):
    file_content = open(fileNames[i], 'r')
    tempFileName = os.path.basename(fileNames[i])
    tempFileName = tempFileName[:-4] 
    file = open('output/' + tempFileName + '.block.out', 'w')
    file.write("Begin Block\n")
    file.write("Begin Header\n")
    file.write("Hash: "+blocksList[i].compute_hash() + "\n")
    file.write("Hash of root: " + blocksList[i].hash_prev + "\n")
    file.write("Timestamp: " + str(blocksList[i].timestamp) + "\n")
    file.write("Target: " + str(blocksList[i].target) + "\n")
    file.write("Nonce: " + str(blocksList[i].set_nonce()) + "\n")
    file.write("END HEADER\n")
    file.write("END BLOCK\n")
    file.write("------------------------\n")
    file_content.close()
    file_content = open(fileNames[i], 'r')
    for line in file_content:
        file.write(line)
    file.close()