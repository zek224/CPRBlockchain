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

With each block, you will be able to see if it is valid or not. For a block to be valid, the hash_root with the Merkle root hash.  
If all blocks are valid, then we will have a valid BlockChain.

After that, you will be prompted to enter in a 40 character address and to search for that address and return its balance.
Next, an array is printed with the path from the leaf to the root to show proof of membership.