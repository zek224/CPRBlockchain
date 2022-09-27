#!/bin/sh

# 10 test input files
file1='./Code/input/1.txt'
file2='./Code/input/2.txt'
file3='./Code/input/3.txt'
file4='./Code/input/4.txt'
file5='./Code/input/5.txt'
file6='./Code/input/6.txt'
file7='./Code/input/7.txt'
file8='./Code/input/8.txt'
file9='./Code/input/9.txt'
file10='./Code/input/10.txt'

# Run program
cd ./Code
python3 allcode.py $file1 $file2 $file3 $file4 $file5 $file6 $file7 $file8 $file9 $file10
