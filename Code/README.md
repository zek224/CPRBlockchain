# CPRBlockchain
Blockchain Group Assignment for CSE242  
Daniel, Matt, Steven, and Zee  


## Usage: 
Run `bash run.sh`

OR

`cd ./Code`
Then, in folder do:
`python3 allcode.py`

You will be prompted to enter in a single file path or a folder
If you choose the first option, you will have to enter in the path of the file you are wishing to input,
and will continue to enter it until you press '0'.

Then, a list of blocks will be generated containing, `Block Root Hash`, `Previous Block Hash`, `Timestamp`,
`Difficulty Target`, and the `Nonce`.  You will also see an output folder generated containing all blocks.  

With each block, you will be able to see if it is valid or not. For a block to be valid, the hash_root has to equalthe Merkle root hash.  
If all blocks are valid, then we will have a valid BlockChain.

After that, you will be prompted to enter in a 40 character address and to search for that address and return its balance.
You will continue to be prompted to enter an address until successful.
You can take an address from the `output` file.  
Next, an array is printed with the path from the leaf to the root to show proof of membership,
as well as return the balance.


```Things We need```
1)  Change from root to hash of account, to account to root
2)  Check bad blocks better method
3)  What are we printing out? and how we outputting it

## Homework 5 Description:
## Validate Block
We took the contents of the output folder (output) and rebuild the tree with the 30 addresses and balances. If the merkle tree matches the output folder, then a validation is made. The merkle root contains a single hash that can validate every single transaction hash in the block, so if the block hash deviates from the merkle root while using the build_tree() method. If there is a single transaction in the output files which does not match from the input files, the merkle root created from that block will be different from the input files, so therefore it will be invalid. 

## Validate Blockchain
If the merkle root of each block is the same (we check this using the validate_block method), and the hash of the previous block is the equal to the previous element in block hashes list, then there is a validation. Else, we print that the block is invalid and we print the hash of the previous block and also the hash of the current block. 

## Generating/Testing for Bad Blocks
Our methodology for generating and testing bad blocks was by creating a bad blocks folder. This folder would contain one or more addresses which deviate from the specified length which map to a balance. 

## Balance Method
the get_balance method finds the balance of a transaction inside a block by traversing the tree of addresses. Once the address has been found using the find_leaf() method, we then print "\nBalance at Address: " + Leaf.balance and return the path where that address is found. Else, we return None since the address is not found. 

## Proof of Membership
We verified for proof of membership by making sure that each block in the blockchain fails if one block hash is modified in any way. Basically, by using the validation method discussed above, and validating the blockchain, every node can contribute to the blockchain. 

## Running Application for Homework 5

1. In the root folder, run with bash run.sh
2. Select either 1 or 2 to run either all txt files or a single txt file
3. Upon running, enter either a valid or invalid address (40 characters long)
4. CheckAddressForBalance will return if the address is found or not found.
