
import sys

#				  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25
letters_upper = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
letters_lower = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def input_validator(alpha, beta): # Checks the alpha and beta values for correct bounds

	if alpha < 1:
		print "Alpha must be > 0"
		return False
	if beta < 0:
		print "Beta must be >= 0"
		return False

	return True

# Find the modular multiplicative inverse
def modulo_inverse(alpha):

	# We need to find the value of x to satisfy the following
	# equation -> (ax)mod26=1 so we will just brute force it.
	# If the process takes too many steps than we will return
	# an error code.

	for x in range(0, 1000000):

		if (alpha*x) % 26 == 1: # If this is true then x is the modular inverse
			return x

	return False # Return false if not found

# Decrypt affine ciphertext with provided alpha and beta
def affine_decrypt(ciphertext, alpha, beta):

	if input_validator(alpha,beta) == False:
		return False

	print "Decrypting with alpha = "+str(alpha)+" & beta = "+str(beta)+"."
	plaintext = ""
	
	inverse = modulo_inverse(alpha)
	if inverse == False:
		print "Could not calculate modulo multiplicative inverse."
		return False

	for letter in ciphertext: # Iterate through each letter in the plaintext
		
		if letter == '\n':
			plaintext += '\n'

		elif letter == " ": # If the letter is just a space
			plaintext += " " # Add space to ciphertext

		else: # If the letter is not a space

			is_letter = True

			if letter in letters_lower: # If the letter is lowercase
				letter_set 		= letters_lower

			elif letter in letters_upper: # If the letter is uppercase
				letter_set 		= letters_upper

			else: # The current is not a letter
				is_letter = False

			if is_letter: # If the current is either an uppercase or lowercase letter

				fx 	= letter_set.index(letter) # Get the index of the letter
				x 	= (fx-beta)*inverse
				x 	= x % 26 # Calculate the modulo
				
				plaintext += letter_set[x]
			
			else: # If the current was not on the regular letter line (probably a number)
				plaintext += letter

	return plaintext

# Encrypt plaintext with provided alpha and beta
def affine_encrypt(plaintext, alpha, beta):

	if input_validator(alpha,beta) == False:
		return False

	print "Encrypting with alpha = "+str(alpha)+" & beta = "+str(beta)+"."
	ciphertext = ""

	index = 0 # Track location in text
	endline = False # True if 
	for letter in plaintext: # Iterate through each letter in the plaintext

		if letter == '\n':
			ciphertext += '\n'
		
		elif letter == " ": # If the letter is just a space
			ciphertext += " " # Add space to ciphertext

		else: # If the letter is not a space

			is_letter = True

			if letter in letters_lower: # If the letter is lowercase
				letter_set 		= letters_lower

			elif letter in letters_upper: # If the letter is uppercase
				letter_set 		= letters_upper

			else: # The current is not a letter
				is_letter = False

			if is_letter: # If the current is either an uppercase or lowercase letter

				x 	= letter_set.index(letter) # Get the index of the letter
				fx 	= (alpha*x)+beta # Calculate the new location
				fx 	= fx % 26 # Calculate the modulo

				ciphertext += letter_set[fx]
			
			else: # If the current was not on the regular letter line (probably a number)
				ciphertext += letter

	return ciphertext

def main():

	if len(sys.argv) == 5:
		# The four arguments (after affine.py) should be [filename] [function] [alpha] [beta]
		print "Note: Argument order is as follows -> [filename] [-e or -d] [alpha] [beta]"
		
		filename 	= sys.argv[1]
		function 	= sys.argv[2]
		alpha 		= int(sys.argv[3])
		beta 		= int(sys.argv[4])

		# Reading the entire file into string 'data'
		with open(filename, 'r') as source:
			data = source.read()
			#data = source.read().replace('\n', '')

		if function == "-e" or function == "-E":
			new_data = affine_encrypt(data, alpha, beta)
		elif function == "-d" or function == "-D":
			new_data = affine_decrypt(data, alpha, beta)
		else:
			print "ERROR: The second argument should be either -e (encrypt) or -d (decrypt)."
			return

		if new_data == False: # Something went wrong with translation
			print "ERROR: Ensure that alpha > 0, beta >= 0, alpha and 26 are coprime."
			return

		new_file = open(filename, 'w')
		new_file.write(new_data)

		print "Process complete."
		return

	else:
		print "ERROR: Argument order is as follows -> [filename] [-e or -d] [alpha] [beta]"


if __name__ == '__main__':
	main()