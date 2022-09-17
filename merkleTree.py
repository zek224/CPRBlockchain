from typing import List
import hashlib, sys, os


class Leaf:
    def __init__(self, left, right, value: str, content, is_copied=False):
        self.left: Leaf = left
        self.right: Leaf = right
        self.value = value
        self.content = content
        self.is_copied = is_copied

    @staticmethod
    def hash(val: str):
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __str__(self):
        return (str(self.value))

    def copy(self):
        """
        class copy function
        """
        return Leaf(self.left, self.right, self.value, self.content, True)


class MerkleTree:
    def __init__(self, values: List[str]):
        self.buildTree(values)

    def buildTree(self, values: List[str]):

        leaves: List[Leaf] = [Leaf(None, None, Leaf.hash(e), e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1].copy())  # duplicate last elem if odd number of elements
        self.root: Leaf = self.buildTreeRec(leaves)

    def buildTreeRec(self, Leafs: List[Leaf]) -> Leaf:
        if len(Leafs) % 2 == 1:
            Leafs.append(Leafs[-1].copy())  # duplicate last elem if odd number of elements
        half: int = len(Leafs) // 2

        if len(Leafs) == 2:
            return Leaf(Leafs[0], Leafs[1], Leaf.hash(Leafs[0].value + Leafs[1].value), Leafs[0].content+"+"+Leafs[1].content)

        left: Leaf = self.buildTreeRec(Leafs[:half])
        right: Leaf = self.buildTreeRec(Leafs[half:])
        value: str = Leaf.hash(left.value + right.value)
        content: str = f'{left.content}+{right.content}'
        return Leaf(left, right, value, content)

    def printTree(self):
        self.printTreeRec(self.root)

    def printTreeRec(self, Leaf: Leaf):
        if Leaf != None:
            if Leaf.left != None:
                print("Left: "+str(Leaf.left))
                print("Right: "+str(Leaf.right))
            else:
                print("Input")
                
            if Leaf.is_copied:
                print('(Padding)')
            print("Value: "+str(Leaf.value))
            print("Content: "+str(Leaf.content))
            print("")
            self.printTreeRec(Leaf.left)
            self.printTreeRec(Leaf.right)

    def getRootHash(self):
        return self.root.value


def makeTree():
    try:
        file = open(sys.argv[1])                # try - catch to try to open file
    except:
        print("\nError: Please enter a valid text file.\n")         # if not a file, print this and exit program
        sys.exit(0)
    elements = file.read()          # read entire file to a string 
    array = elements.split()        # split into array based on space from string
    print("Input: ", array)
    tree = MerkleTree(array)        # make tree from input array ()
    print("Root Hash: " + tree.getRootHash() + "\n")
    tree.printTree()

if len(sys.argv) != 2:                                                # Help Message is argv[1] (path to input file) doesn't exist
    print("\nUsage: 'python3 merkleTree.py <path/to/file.txt>\n")     # Exits program if this statement is true
    sys.exit(0)
else:
    makeTree()  


# https://github.com/onuratakan/mixmerkletree
# string (address), single space, integer (balance?)


# def mixmerkletree():
#     elems = ["Copy", "Paste", "Repeat", "From", "Daniel U", "Matt N", "Steven N", "Zee K"]
#     print("Inputs: ")
#     print(*elems, sep=" | ")
#     print("")
#     mtree = MerkleTree(elems)
#     print("Root Hash: "+mtree.getRootHash()+"\n")
#     mtree.printTree()
