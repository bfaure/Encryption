
import sys

#				  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25
letters_upper = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
letters_lower = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

# Ensure that the input is above zero
def input_validator(shift):

	if shift < 0:
		return False

	return True


def shifter(plaintext, shift, function="encrypt"):

	if input_validator(shift) == False:
		return False

	print "Encrypting with shift = "+str(shift) if function=="encrypt" else "Decrypting with shift = "+str(shift)
	ciphertext = ""

	for letter in plaintext:

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

			if is_letter:

				x 	= letter_set.index(letter)
				fx 	= x+shift if function=="encrypt" else x-shift
				fx 	= fx % 26
				ciphertext += letter_set[fx]

			else:
				ciphertext += letter
	return ciphertext

def main():

	if len(sys.argv) == 4:
		# The four arguments (after affine.py) should be [filename] [function] [alpha] [beta]
		print "Note: Argument order is as follows -> [filename] [-e or -d] [shift]"
		
		filename 	= sys.argv[1]
		function 	= sys.argv[2]
		shift 		= int(sys.argv[3])

		# Reading the entire file into string 'data'
		with open(filename, 'r') as source:
			data = source.read()

		if function == "-e" or function == "-E":
			new_data = shifter(data, shift)
		elif function == "-d" or function == "-D":
			new_data = shifter(data, shift, "decrypt")
		else:
			print "ERROR: The second argument should be either -e (encrypt) or -d (decrypt)."
			return

		if new_data == False: # Something went wrong with translation
			print "ERROR: Ensure that shift >= 0."
			return

		new_file = open(filename, 'w')
		new_file.write(new_data)

		print "Process complete."
		return

	else:
		print "ERROR: Argument order is as follows -> [filename] [-e or -d] [shift]"


if __name__ == '__main__':
	main()