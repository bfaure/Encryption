# Encryption
Various files for encrypting/decrypting data.

## Files

**affine.py**: Script to encrypt or decrypt text using the affine cipher. Affine cipher requires two keys *alpha* and *beta*, these along with the name of the file to be converted must be included in the command line call as follows: ```python affine.py [filename] [-e or -d] [alpha] [beta]```
-e will tell the script to encrypt while -d will do the opposite.
