# Encryption
Various files for encrypting/decrypting data.

## Files

**affine.py**: Script to encrypt or decrypt text files using the affine cipher. Affine cipher requires two keys *alpha* and *beta*, these along with the name of the file to be converted must be included in the command line call as follows. <br/><br/>```python affine.py [alice_in_wonderland.txt] [-e or -d] [alpha] [beta]```
<br/><br/>The -e command will tell the script to encrypt while -d will do the opposite. [More information about the Affine cipher](https://en.wikipedia.org/wiki/Affine_cipher)<br/><br/>

**shift.py**: Script to encrypt or decrypt text files using the shift (Caesar) cipher. Shift cipher only requires a single key *shift*. The command line call is as follows. <br/><br/>'''python shift.py [alice_in_wonderland.txt] [-e or -d] [shift]'''
<br/><br/>The -e command will tell the script to encrypt while -d will do the opposite. [More information about the shift cipher](https://en.wikipedia.org/wiki/Caesar_cipher)

## Dependencies
Python 2.7
