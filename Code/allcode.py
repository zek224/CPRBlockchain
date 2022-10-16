from __future__ import generator_stop
from array import array
from imp import is_builtin
from time import time
from typing import List
import datetime as dt  # for timestamp in header of each block
import hashlib
import sys
import os
import random
import numpy as np
import math

'''
Merkle Tree class
- Leaf and MerkleTree class
- MerkleTree class contains a list of Leaf objects
'''
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
                acct, bal = line.split(' ', 1)  # split line into two variables
                newBal=bal.replace("\n","")
                if (len(acct) != 40):        # check if address is 40 characters
                    print("Error: Invalid address at input line " +
                          str(values.index(line) + 1) + ".\n")
                    sys.exit(0)
                if (newBal.isdigit() == False):      # check if balance is a number
                    print("Error: Invalid balance at input line " +
                          str(values.index(line) + 1) + " " +newBal+ "\n")
                    # sys.exit(0)
                account.append(acct)    # add address to account array
                balance.append(newBal)     # add balance to balance array
            except:
                # no clue yet, its not an error with the inputs
                print("Error while building tree. Values at error point printed.")
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
            # create new Leafs
            return Leaf(Leafs[0], Leafs[1], None, None, Leaf.hash(Leafs[0].hashValue + Leafs[1].hashValue))
        elif len(Leafs) == 1:
            # return the new Leafs
            # create new Leafs
            return Leaf(Leafs[0], None, (Leafs[0].address), (Leafs[0].balance), Leaf.hash(Leafs[0].hashValue))

        # recursive call
        left = self._buildTree(Leafs[:half])    # left child
        right = self._buildTree(Leafs[half:])   # right child
        address = None  # address of the new leaf
        balance = None  # balance of the new leaf
        if right:
            # hash the new Leafs
            # hash the new Leafs
            hashValue = Leaf.hash(left.hashValue + right.hashValue)
        else:
            hashValue = Leaf.hash(left.hashValue)   # hash the new Leafs
        # return the new Leafs
        # create new Leafs
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
            # prints address and balance
            print(f'\t[{node.address}, {node.balance}]')
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
        self.timestamp = math.trunc(dt.datetime.now().timestamp())  # timestamp
        self.target = 2 ** 255  # for the difficulty target
        self.nonce = 0  # nonce
        self.nonce_max = 2 ** 32    # max nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        hashes = hashlib.sha256(((str(self.hash_prev) + str(self.hash_root) + str(
            self.timestamp) + str(self.target) + str(self.nonce)).encode('utf-8'))).hexdigest()  # hash the block
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

    def validate_block(self, inputs):   # inputs is an array of accounts and balances from the #.block.out file (lines 11 to 40)
        # see if self.hash_root is the same as MerkleTree(inputs).getRootHash()
        # print(self.hash_root)
        # print(MerkleTree(inputs).getRootHash())
        if self.hash_root == MerkleTree(inputs).getRootHash():
            return True
        else:
            return False


class Blockchain():
    def __init__(self):
        self.nonce_max = 2 ** 32    # max nonce
        self.target = 2 ** 255  # target
        self.blockList = []     # list of blocks

    # def set_nonce(self, block):
    #     # create a new block
    #     object1 = Block(block.hash_prev, block.hash_root)
    #     target = random.randint(0, 2**32)   # random target

    #     for n in range(self.nonce_max):
    #         if int(object1.compute_hash(), 16) < self.target:
    #             self.nonce_max = target   # set max nonce
    #             break   # break
    #         else:
    #             object1.nonce = random.randint(0, 2**32)    # set nonce

    def create_genesis_block(self):
        genesis_block = Block("0", "0")     # create genesis block
        self.blockList.append(genesis_block)  # create genesis block
        return genesis_block  # create genesis block


    # validate a block
    def validate_blockchain(self, block):
        # create a new block
        object1 = Block(block.hash_prev, block.hash_root)
        if int(object1.compute_hash(), 16) < self.target:
            return True     # return true
        else:
            return False    # return false


# read in each rgument in argv adn append it to an array. then we have array of all filesname / paths to files.

# reads in fileInputs, which is the list of paths to the different input files


blockchain = Blockchain()  # create a blockchain
blockchain.create_genesis_block()  # create genesis block

def makeTree(fileInputs):
    print("\nInputted files: ", fileInputs, "\n")   # print inputted files
    array = []  # array of all the transactions
    for files in fileInputs:
        array = []  # sets array to empty
        try:
            # try - catch to try to open file
            file = open(files, "r")
            #print('File opened')
        except:
            # if not a file, print this and exit program
            print("\nError: Please enter a valid text file.\n")
            sys.exit(0)    # exit program

        for line in file:
            array.append(line.strip())  # add each line to array

        tree = MerkleTree(array)        # make tree from input array ()
        # tree.printTreeGraphically()     # print tree graphically
        # print('\n\n\n')
        block = Block(blockchain.blockList[-1].compute_hash(), tree.getRootHash())  # is this reversed?
        blockchain.blockList.append(block)  # add block to blockchain
        #print("Root Hash: " + tree.getRootHash() + "\n")
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
        # fileNames = []      # array to make tree
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

#object2 = Blockchain()  # create blockchain object
#block = None    # block object
#blocksList = []    # list of blocks


# print files in given format
# for i in range(len(blockchain.blockList)):
#     print("BEGIN BLOCK\n")
#     print("BEGIN HEADER\n")
#     print("Block Root Hash: "+ blockchain.blockList[i].compute_hash() + "\n")
#     print("Previous Block Root Hash: " + blockchain.blockList[i].hash_prev + "\n")
#     print("Timestamp: " + str(blockchain.blockList[i].timestamp) + "\n")
#     print("Target: " + str(blockchain.blockList[i].target) + "\n")
#     print("Nonce: " + str(blockchain.blockList[i].set_nonce()) + "\n")
#     print("END HEADER\n")
#     print("END BLOCK\n")
#     print("------------------------\n")

os.mkdir("output")


for i in range(len(blockchain.blockList) - 1):
    file_content = open(fileNames[i], 'r')  # open file
    tempFileName = os.path.basename(fileNames[i])   # get file name
    tempFileName = tempFileName[:-4]    # remove .txt from file name
    file = open('output/' + tempFileName +
                '.block.out', 'w')   # create new file
    file.write("BEGIN BLOCK\n")
    file.write("BEGIN HEADER\n")
    file.write("Hash of root: "+ blockchain.blockList[i].compute_hash() + "\n")
    file.write("Hash of previous block: " + blockchain.blockList[i].hash_prev + "\n")
    file.write("Timestamp: " + str(blockchain.blockList[i].timestamp) + "\n")
    file.write("Target: " + str(blockchain.blockList[i].target) + "\n")
    file.write("Nonce: " + str(blockchain.blockList[i].set_nonce()) + "\n")
    file.write("END HEADER\n")
    file.write("END BLOCK\n")
    file.write("------------------------\n")
    file_content.close()    # close file
    file_content = open(fileNames[i], 'r')  # open file
    for line in file_content:
        file.write(line)    # write contents of file to new file
    file.close()    # close file


# rows, cols = (len(fileNames), 30)
# testArray = [[]*cols]*rows

# #inputs = [0] * len(fileNames)
# inputs=[[]*cols]*rows
#print("the Length of filesnames is " +str(len(fileNames)))

testArray = []
inputs = []
for i in range(len(fileNames)):
    testFileName = os.path.basename(fileNames[i])   # get file name
    testFileName = testFileName[:-4]    # remove .txt from file name
    #print(testFileName)
    with open('output/' + testFileName +'.block.out') as outputfile:
        # add lines 11 to 40 into testArray1
        for j, line in enumerate(outputfile):
            if j >= 10:
                testArray.append(line)
    # print(testArray[i])
    #print(i)
    #print("viewing output file" + str(outputfile))
    # #print(testArray)
    #testArray.clear()
#print(type(testArray))
# test = np.array(testArray)
# print(test)
splits = np.array_split(testArray, len(fileNames))
# print(len(splits))
empty_list = []
for i in splits:
    empty_list.append(i.tolist())
    
for j in range(1, len(fileNames)):
    print(blockchain.blockList[j].validate_block(empty_list[j - 1]))
    
    # for j in range(len(i)):
    #     #validate_block for each array produced by np.array_split
    #      blockchain.blockList[j].validate_block(i[int(j)])


    # blockchain.blockList[i].validate_block(list(i))
    # for j in range(len(list(i))):
    #     blockchain.blockList[i].validate_block(i)

    # if blockchain.blockList[i].validate_block(temp):
    #     print("Block " + str(i) + " is valid")
    # else:
    #     print("Block " + str(i) + " is invalid")
    # print(list(i))
    

# for i in sub_lists:
#     print("List ", count, ": ",list(i))
#     count+=1
# print(splits)

# valid_block for all inputs\
# for i in range(len(inputs)):
#     if blockchain.blockList[i].validate_block(inputs[i]):
#         print("Block " + str(i) + " is valid")
#     else:
#         print("Block " + str(i) + " is invalid")

#print(inputs)
# for i in range(0, len(inputs)):    
#     print(blockchain.blockList[i].validate_block(inputs[i]))

# print testArray out
# for i in range(len(testArray)):
#     print(testArray[i])
# print(inputs)

# print(inputs)