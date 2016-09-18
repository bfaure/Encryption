import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"/algo")
from affine import *
from shift import * 

from PyQt4 import QtGui
from PyQt4 import QtGui
from PyQt4.QtCore import QThread, QRect
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class window(QtGui.QWidget):
	# Window to allow the user to set up the encryption/decryption settings,
	# select their source file, choose whether or not to create a copy, etc.

	# Window constructor
	def __init__(self, parent=None):
		super(window, self).__init__()
		#self.initThread()
		
		# Begin the user interface constructor
		self.initUI()

	def initUI(self):

		# Class resources
		self.title_font = QtGui.QFont("Lucida", 20)
		self.encryption_types = ["Affine", "Caesar (shift)"]
		self.transform_direction = "encryption"
		self.transform_type = "affine"
		self.have_text = False
		self.alpha_validator = QtGui.QIntValidator(1, 1000000, self)
		self.beta_validator = QtGui.QIntValidator(0, 1000000, self)
		self.shift_validator = QtGui.QIntValidator(0, 1000000, self)

		# Initializing window
		self.resize(775,400)
		self.setWindowTitle("Encrpytion Suite")

		# Layouts
		self.main_vertical = QtGui.QVBoxLayout(self) # Outer layout
		self.main_horizontal = QtGui.QHBoxLayout() # Under self.logo in the self.main_vertical
		self.left_vertical = QtGui.QVBoxLayout() # First column on the self.main_horizontal
		self.right_vertical = QtGui.QVBoxLayout() # Second column on the self.main_horizontal
		self.right_upper_horizontal = QtGui.QHBoxLayout() # First row of self.right_vertical
		self.right_lower_horizontal = QtGui.QHBoxLayout() # Last for of self.right_vertical
		self.form_layout = QtGui.QStackedWidget() # List of layouts for the different encryption types 
		self.affine_layout = QtGui.QHBoxLayout() # Holds the alpha and beta inputs for affine
		self.shift_layout = QtGui.QHBoxLayout() # Holds the shift input for shift cipher
		self.shift_widget = QtGui.QWidget() # Parent for shift layout
		self.affine_widget = QtGui.QWidget() # Parent for affine layout

		# Widgets
		self.logo = QtGui.QLabel("Encryption Suite", self)
		self.logo.setFont(self.title_font)
		self.logo.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.main_vertical.addWidget(self.logo)
		self.main_vertical.addSpacing(25)

		self.pastebox_logo = QtGui.QLabel("Paste text below.", self)
		self.pastebox_logo.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.left_vertical.addWidget(self.pastebox_logo)

		self.pastebox = QtGui.QTextEdit("", self)
		self.pastebox.textChanged.connect(self.text_changed)
		self.left_vertical.addWidget(self.pastebox)
		self.main_horizontal.addLayout(self.left_vertical, 1) # Add stretching priority to paste box
		self.main_vertical.addLayout(self.main_horizontal, 1) # Add stretching priority to horizontal layout
		self.main_vertical.addStretch()

		self.type_selector_label = QtGui.QLabel("Choose transformation type: ", self)
		self.right_upper_horizontal.addWidget(self.type_selector_label)
		self.right_vertical.addLayout(self.right_upper_horizontal)

		self.type_selector = QComboBox(self)
		self.type_selector.addItems(self.encryption_types)
		self.type_selector.currentIndexChanged.connect(self.encryption_type_selected)
		self.right_upper_horizontal.addWidget(self.type_selector)

		self.divider = QtGui.QFrame(self)
		self.divider.setFrameShape(QFrame.HLine)
		self.right_vertical.addWidget(self.divider)
		self.right_vertical.addSpacing(25)
		self.right_vertical.addStretch()
		self.right_vertical.addWidget(self.form_layout) # QStackedLayout holding both the shift and affine widgets
		self.main_horizontal.addLayout(self.right_vertical)

		self.alpha_input = QtGui.QLineEdit("", self)
		self.alpha_input.setPlaceholderText("alpha")
		self.alpha_input.textEdited.connect(self.param_changed)
		self.alpha_input.setValidator(self.alpha_validator)
		self.affine_layout.addWidget(self.alpha_input)

		self.beta_input = QtGui.QLineEdit("", self)
		self.beta_input.setPlaceholderText("beta")
		self.beta_input.textEdited.connect(self.param_changed)
		self.beta_input.setValidator(self.beta_validator)
		self.affine_layout.addWidget(self.beta_input)

		self.affine_widget.setLayout(self.affine_layout)
		self.form_layout.addWidget(self.affine_widget)

		self.shift_input = QtGui.QLineEdit("", self)
		self.shift_input.setPlaceholderText("shift")
		self.shift_input.textEdited.connect(self.param_changed)
		self.shift_input.setValidator(self.shift_validator)
		self.shift_layout.addWidget(self.shift_input)
		self.shift_widget.setLayout(self.shift_layout)
		self.form_layout.addWidget(self.shift_widget)
		self.form_layout.setCurrentIndex(0)

		self.encrypt_row = QtGui.QHBoxLayout()
		self.decrypt_row = QtGui.QHBoxLayout()

		self.encrypt_label = QtGui.QLabel("Encryption", self)
		self.decrypt_label = QtGui.QLabel("Decryption", self)

		self.encrypt_button = QtGui.QRadioButton(self)
		self.encrypt_button.toggled.connect(self.radio_changed)
		self.decrypt_button = QtGui.QRadioButton(self)
		self.decrypt_button.toggled.connect(self.radio_changed)

		self.encrypt_row.addStretch()
		self.encrypt_row.addWidget(self.encrypt_label)
		self.encrypt_row.addSpacing(45)
		self.encrypt_row.addWidget(self.encrypt_button)
		self.encrypt_row.addStretch()

		self.decrypt_row.addStretch()
		self.decrypt_row.addWidget(self.decrypt_label)
		self.decrypt_row.addSpacing(45)
		self.decrypt_row.addWidget(self.decrypt_button)
		self.decrypt_row.addStretch()

		self.right_vertical.addLayout(self.encrypt_row)
		self.right_vertical.addLayout(self.decrypt_row)
		self.right_vertical.addSpacing(25)

		self.divider_low = QtGui.QFrame(self)
		self.divider_low.setFrameShape(QFrame.HLine)
		self.right_vertical.addWidget(self.divider_low)

		self.action_button = QtGui.QPushButton("Encrypt", self)
		self.action_button.clicked.connect(self.action)
		self.right_lower_horizontal.addWidget(self.action_button)
		self.right_vertical.addLayout(self.right_lower_horizontal)
		self.right_vertical.addStretch(1)

		self.clear_button = QtGui.QPushButton("Clear", self)
		self.clear_button.clicked.connect(self.clear)
		self.right_lower_horizontal.addWidget(self.clear_button)

		# Showing the window
		self.show()
		self.encryption_type_selected()

	def param_changed(self):
		self.check_config()

	def check_config(self):
		# Checks all launch configurations to see if ready to start
		if self.have_text == False:
			self.action_button.setEnabled(False)
			return

		if self.transform_type == "affine":
			if self.alpha_input.text() == "":
				self.action_button.setEnabled(False)
				return

			if self.beta_input.text() == "":
				self.action_button.setEnabled(False)
				return

		if self.transform_type == "shift":
			if self.shift_input.text() == "":
				self.action_button.setEnabled(False)
				return

		self.action_button.setEnabled(True)

	def text_changed(self):
		text = self.pastebox.toPlainText()
		if text != "":
			self.have_text = True
		self.check_config()

	def radio_changed(self):
		if self.encrypt_button.isChecked():
			# The user wants to encrypt
			self.transform_direction = "encryption"
			self.action_button.setText("Encrypt")
		if self.decrypt_button.isChecked():
			# The user wants to decrypt
			self.transform_direction = "decryption"
			self.action_button.setText("Decrypt")

	def encryption_type_selected(self):
		cur = self.type_selector.currentText()
		self.action_button.setEnabled(False)
		self.encrypt_button.setChecked(True)

		if cur == "Affine":
			self.transform_type = "affine"
			self.form_layout.setCurrentIndex(0)

		elif cur == "Caesar (shift)":
			self.transform_type = "shift"
			self.form_layout.setCurrentIndex(1)
		

	def action(self):
		self.cur_text = self.pastebox.toPlainText()

		if self.transform_type == "affine":
			alpha = int(self.alpha_input.text())
			beta = int(self.beta_input.text())

			if self.transform_direction == "encryption":
				new_text = affine_encrypt(self.cur_text, alpha, beta)
				self.pastebox.setText(new_text)
				return

			else:
				new_text = affine_decrypt(self.cur_text, alpha, beta)
				self.pastebox.setText(new_text)
				return

		if self.transform_type == "shift":
			shift = int(self.shift_input.text())
			new_text = shifter(self.cur_text, shift, "encrypt" if self.transform_direction=="encryption" else "decrypt")
			self.pastebox.setText(new_text)
			return


	def clear(self):
		self.pastebox.clear() # Clear the pastebox
		self.have_text = False
		self.check_config()



def main():
	# First check if the user is wanting to perform a straight file encryption
	# using the command line interface.
	if len(sys.argv) > 1:
		# The logic for this region can be ported over from the main functions
		# of the affine.py and shift.py files.
		print "Handle the direct encryption and decryption stuff here (WIP)."

	else:
		# If not the CLI then open the GUI environment
		app = QtGui.QApplication(sys.argv)
		_ = window()
		sys.exit(app.exec_())



if __name__ == '__main__':
	main()
