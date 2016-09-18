# Encryption
Various files for encrypting/decrypting data. User interface cleanly pulls all functionality together.

## Files

**main.py**: User interface file. Can implement any of the functionality of the individual cipher files below. The GUI is launched with the following command line call. <br/><br/> ```python main.py```<br/><br/>

**affine.py**: Script to encrypt or decrypt text files using the affine cipher. Affine cipher requires two keys *alpha* and *beta*, these along with the name of the file to be converted must be included in the command line call as follows. <br/><br/>```python affine.py [alice_in_wonderland.txt] [-e or -d] [alpha] [beta]```
<br/><br/>The -e command will tell the script to encrypt while -d will do the opposite. [More information about the Affine cipher](https://en.wikipedia.org/wiki/Affine_cipher)<br/><br/>

**shift.py**: Script to encrypt or decrypt text files using the shift (Caesar) cipher. Shift cipher only requires a single key *shift*. The command line call is as follows. <br/><br/>```python shift.py [alice_in_wonderland.txt] [-e or -d] [shift]```
<br/><br/>The -e command will tell the script to encrypt while -d will do the opposite. [More information about the shift cipher](https://en.wikipedia.org/wiki/Caesar_cipher)

## Screenshots

**User Interface**
[!Alt text](https://github.com/bfaure/Encryption/blob/master/archive/Untitled.png)
[!Alt text](https://github.com/bfaure/Encryption/blob/master/archive/encrypted.png)

## Dependencies
Python 2.7, PyQt4 for UI
