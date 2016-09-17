
import sys

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


# Decrypt affine ciphertext with provided alpha and beta
def affine_decrypt(ciphertext, alpha, beta):

	if input_validator(alpha,beta) == False:
		return ""

	print "Decrypting with alpha = "+str(alpha)+" & beta = "+str(beta)+"."
	plaintext = ""

	for letter in ciphertext: # Iterate through each letter in the plaintext
		
		if letter == " ": # If the letter is just a space
			plaintext += " " # Add space to ciphertext

		else: # If the letter is not a space

			is_letter = True

			if letter in letters_lower: # If the letter is lowercase
				letter_set 		= letters_lower

			elif letter in letters_upper: # If the letter is uppercase
				letter_set = letters_upper

			else: # The current is not a letter
				is_letter = False

			if is_letter: # If the current is either an uppercase or lowercase letter

				fx = letter_set.index(letter) # Get the index of the letter
				x = (fx-beta)/alpha # Calculate the new location

				if x < 26: # If the new location does not need modulus
					plaintext += letter_set[x] # Add the new encrypted letter
				else: # If the new location does need modulus

					found = False
					while(found==False):
						x = x - 26 # Subtract 26
						if x < 26:
							plaintext 	+= letter_set[x] # Add the new encrypted letter
							found 		= True # We can stop modulus operation now
			
			else: # If the current was not on the regular letter line (probably a number)
				plaintext += letter

	return plaintext

# Encrypt plaintext with provided alpha and beta
def affine_encrypt(plaintext, alpha, beta):

	if input_validator(alpha,beta) == False:
		return ""

	print "Encrypting with alpha = "+str(alpha)+" & beta = "+str(beta)+"."
	ciphertext = ""

	for letter in plaintext: # Iterate through each letter in the plaintext
		
		if letter == " ": # If the letter is just a space
			ciphertext += " " # Add space to ciphertext

		else: # If the letter is not a space

			is_letter = True

			if letter in letters_lower: # If the letter is lowercase
				letter_set 		= letters_lower

			elif letter in letters_upper: # If the letter is uppercase
				letter_set = letters_upper

			else: # The current is not a letter
				is_letter = False

			if is_letter: # If the current is either an uppercase or lowercase letter

				x = letter_set.index(letter) # Get the index of the letter
				fx = (alpha*x)+beta # Calculate the new location

				if fx < 26: # If the new location does not need modulus
					ciphertext += letter_set[fx] # Add the new encrypted letter
				else: # If the new location does need modulus

					found = False
					while(found==False):
						fx = fx - 26 # Subtract 26
						if fx < 26:
							ciphertext 	+= letter_set[fx] # Add the new encrypted letter
							found 		= True # We can stop modulus operation now
			
			else: # If the current was not on the regular letter line (probably a number)
				ciphertext += letter

	return ciphertext






def main():

	plaintext 	= "Brian D. Faure"
	alpha 		= 2
	beta 		= 10

	print"Plaintext: "+plaintext

	# Inputs to the affine cipher are the plaintext, alpha, and beta
	ciphertext = affine_encrypt(plaintext, alpha, beta)

	print "Ciphertext: "+ciphertext

	print "Re-converted plaintext: "+affine_decrypt(ciphertext, alpha, beta)






if __name__ == '__main__':
	main()