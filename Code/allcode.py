import hashlib, sys, os, random, math, datetime as dt

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


global_addresses = []   # list of all addresses
global_balances = []    # list of all balances


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
                newBal = bal.replace("\n", "")
                if (len(acct) != 40):        # check if address is 40 characters
                    print("Error: Invalid address at input line " +
                          str(values.index(line) + 1) + ".\n")
                    sys.exit(0)
                if (newBal.isdigit() == False):      # check if balance is a number
                    print("Error: Invalid balance at input line " +
                          str(values.index(line) + 1) + " " + newBal + "\n")
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

        global_addresses.append(account)
        global_balances.append(balance)

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
        self._printTreeInOrder(self.root)   # prints tree in order

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

    # traverse the merkle tree and find a leaf with the given address
    def findLeaf(self, address, path):
        path = []
        return self._findLeaf(self.root, address, path)    # traverse the tree

    def _findLeaf(self, Leaf, address, path):
        if Leaf != None:
            if Leaf.left != None:
                # recursive call
                # add hash value to path for PoM
                path.append(Leaf.hashValue)
                return self._findLeaf(Leaf.left, address, path) or self._findLeaf(Leaf.right, address, path)    
            else:
                if Leaf.address == address:
                    path.append(Leaf.hashValue)    # add hash value to path for PoM
                    path = path[::-1]   # reverse the path
                    # print(path)    # print path for PoM
                    print("\nBalance at Address: " + Leaf.balance)  # print address
                    return path   # return balance
                else:
                    path.pop()                  # remove hash value from path if incorrect
                    return None              # return None if incorrect

    def get_balance(self, address, path=[]):
        '''
        we need to open every txt file
        we will use hashmap (every address(key) maps to a balance(value))
        double for loop (outer for files, inner for line) -> split line into key, value = line.split(' ', 1)
        place each key value into hashmap
        if address is in hashmap, return balance map['address'], if not return does not exist message
        '''

        return self.findLeaf(address, path)   # traverse the tree


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

    # inputs is an array of accounts and balances from the #.block.out file (lines 11 to 40)
    def validate_block(self, inputs):
        # see if self.hash_root is the same as MerkleTree(inputs).getRootHash()
        if self.hash_root == MerkleTree(inputs).getRootHash():
            return True    # return true if valid
        else:
            return False


class Blockchain():
    def __init__(self):
        self.nonce_max = 2 ** 32    # max nonce
        self.target = 2 ** 255  # target
        self.blockList = []     # list of blocks
        self.blockHashes = []    # list of block hashes
        self.blockPrevHashes = []    # list of previous block hashes

    def create_genesis_block(self):
        genesis_block = Block("0", "0")     # create genesis block
        self.blockList.append(genesis_block)  # create genesis block
        return genesis_block  # create genesis block

    def validate_blockchain(self, inputfiles, empty):
        for i in range(1, len(inputfiles) + 1):
            if (self.blockList[i].validate_block(empty[i - 1]) and blockchain.blockPrevHashes[i] == blockchain.blockHashes[i - 1]): # validate block
                print("Block " + str(i) + " validated - root hashes match.")  # print valid
            else:
                print("Block " + str(i) + " is invalid")
                print("Block hash prev: ", blockchain.blockPrevHashes[i])   # print invalid
                print("Block hash root: ", blockchain.blockHashes[i - 1])   # print invalid
                return False
        print("All block hashes link to eachother - Blockchain validated.")  # print valid
        return True # return true if valid

# read in each rgument in argv adn append it to an array. then we have array of all filesname / paths to files.

# reads in fileInputs, which is the list of paths to the different input files


blockchain = Blockchain()  # create a blockchain
blockchain.create_genesis_block()  # create genesis block
merkle_trees = []   # list of merkle trees


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
        merkle_trees.append(tree)       # add tree to list of trees
        tree.printTreeGraphically()     # print tree graphically
        print('\n\n\n')
        # is this reversed?
        block = Block(
            blockchain.blockList[-1].compute_hash(), tree.getRootHash())
        blockchain.blockList.append(block)  # add block to blockchain
        #print("Root Hash: " + tree.getRootHash() + "\n")
        file.close()    # close file
    return array        # return array


# if "python3 allcode.py" only, then prompt for file inputs where user input starts
size = 0
fileNames = []
if len(sys.argv) == 1:
    print("\nMake a selection \n1. Enter multiple file names \n2. Enter a folder (all files in folder will be entered) \n3. Exit\n")
    selectionInput = input("Selection: ")
    if (selectionInput == "1"):       # multiple file names
        print("Enter a single file name one at a time (enter 0 to exit): ")
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


def runChainValidation():
    testArray = []
    for i in range(len(fileNames)):
        testFileName = os.path.basename(fileNames[i])   # get file name
        testFileName = testFileName[:-4]    # remove .txt from file name
        # print(testFileName)
        with open('output/' + testFileName + '.block.out') as outputfile:
            # add lines 11 to 40 into testArray1
            for j, line in enumerate(outputfile):
                if j >= 10:    # start at line 11
                    testArray.append(line)  # add line to array

    # split array into chunks of 30 without numpy
    splits = [testArray[i:i + 30] for i in range(0, len(testArray), 30)]
    empty_list = []    # empty list
    for i in splits:
        empty_list.append(i)   # add each chunk to list
    blockchain.validate_blockchain(fileNames, empty_list)   # validate blockchain


# Makes tree if more than 1 argv
# if len(sys.argv) > 1:
#     if (sys.argv[1] == "--validate"):
#         print("run block validation")
#         runChainValidation()
#     else:
#         # make tree for every file by making an array of file inputs for the tree via argv (ignores argv[0] with is python3 and argv[1] which is program name, takes elements onwards)
#         makeTree(sys.argv[1:])


for i in range(len(blockchain.blockList)):
    blockchain.blockHashes.append(blockchain.blockList[i].compute_hash())   # add block hash to list of block hashes
    blockchain.blockPrevHashes.append(blockchain.blockList[i].hash_prev)    # add block prev hash to list of block prev hashes
    print("BEGIN BLOCK\n")
    print("BEGIN HEADER\n")
    print("Block Root Hash: " + blockchain.blockHashes[i] + "\n")
    print("Previous Block Root Hash: " + blockchain.blockPrevHashes[i] + "\n")
    print("Timestamp: " + str(blockchain.blockList[i].timestamp) + "\n")
    print("Target: " + str(blockchain.blockList[i].target) + "\n")
    print("Nonce: " + str(blockchain.blockList[i].set_nonce()) + "\n")
    print("END HEADER\n")
    print("END BLOCK\n")
    print("------------------------\n")

os.mkdir("output")


for i in range(len(blockchain.blockList) - 1):
    file_content = open(fileNames[i], 'r')  # open file
    tempFileName = os.path.basename(fileNames[i])   # get file name
    tempFileName = tempFileName[:-4]    # remove .txt from file name
    file = open('output/' + tempFileName +
                '.block.out', 'w')   # create new file
    file.write("BEGIN BLOCK\n")
    file.write("BEGIN HEADER\n")
    file.write("Hash of root: " + blockchain.blockHashes[i] + "\n")
    file.write("Hash of previous block: " +
               blockchain.blockPrevHashes[i] + "\n")
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

runChainValidation()    # run block validation


def checkAddressForBalance():
    while True:
        addressToCheck = input("\n\nProvide an address to check for a balance(40 characters long) \n")  # get address to check
        for i in range(len(merkle_trees)):
            path = merkle_trees[i].get_balance(addressToCheck)   # get balance of address
            if (path is not None):

                #print("\nBalance found in Block " + str(i) + ": " + str(balance))
                print("Proof of Membership (from account to root hash): ")
                for j in range(len(path)):
                    if(j == 0):
                        print("\t", path[j], "\t <- hash at address")
                    elif(j == (len(path) - 1)):
                        print("\t", path[j], "\t <- root hash of tree\n")
                    else:
                        print("\t", path[j])
                return
        print("Address not found")        

checkAddressForBalance()    # check address for balance