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

'''
class text_highlighter(QtGui.QSyntaxHighlighter):
	# Class highlights text
    def __init__( self, parent, theme ):
        QSyntaxHighlighter.__init__( self, parent )
        self.parent = parent
        self.highlightingRules = []

        keyword = QTextCharFormat()
        keyword.setForeground( Qt.darkBlue )
        keyword.setFontWeight( QFont.Bold )
        keywords = QStringList( [ "break", "else", "for", "if", "in",
                                  "next", "repeat", "return", "switch",
                                  "try", "while" ] )
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule( pattern, keyword )
            self.highlightingRules.append( rule )
'''

class find_replace_window(QtGui.QWidget):
	# Small dialog that pops up when the user wants to search through the text

	# Window constructor
	def __init__(self, parent=None):
		super(find_replace_window, self).__init__()
		self.initUI()

	def initUI(self):

		self.setFixedWidth(225)
		self.setFixedHeight(210)

		self.notice = QtGui.QLabel("Find", self)
		self.notice.move(37, 25)
		self.notice.resize(self.notice.sizeHint())

		self.notice2 = QtGui.QLabel("Replace With", self)
		self.notice2.move(37, 100)
		self.notice2.resize(self.notice2.sizeHint())

		self.input 	= QtGui.QLineEdit(self)
		self.input.move(37, 50)
		self.input.textChanged.connect(self.text_changed)
		self.input.setFixedWidth(150)

		self.input2 = QtGui.QLineEdit(self)
		self.input2.move(37, 125)
		self.input2.textChanged.connect(self.text_changed)

		self.search = QtGui.QPushButton("Find and Replace", self)
		self.search.move(68, 175)
		self.search.resize(self.search.sizeHint())
		self.search.clicked.connect(self.return_value)
		self.search.setEnabled(False)

		self.setWindowTitle("Replace")

	def open_window(self):
		self.show()

	def text_changed(self):
		if self.input.text() != "" and self.input2.text() != "":
			self.search.setEnabled(True)
		else:
			self.search.setEnabled(False)

	def return_value(self):
		self.emit(SIGNAL("return_value(QString)"), self.input.text()+"|||"+self.input2.text())
		self.input.setText("")
		self.input2.setText("")
		self.hide()

	def keyPressEvent(self, event):
		# Responds when user clicks key
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			if self.search.isEnabled():
				self.return_value()


class find_window(QtGui.QWidget):
	# Small dialog that pops up when the user wants to search through the text

	# Window constructor
	def __init__(self, parent=None):
		super(find_window, self).__init__()
		self.initUI()

	def initUI(self):

		self.setFixedWidth(225)
		self.setFixedHeight(130)

		self.notice = QtGui.QLabel("Enter text to search for.", self)
		self.notice.move(37, 25)
		self.notice.resize(self.notice.sizeHint())

		self.input 	= QtGui.QLineEdit(self)
		self.input.move(37, 50)
		self.input.textChanged.connect(self.text_changed)
		self.input.setFixedWidth(150)

		self.search = QtGui.QPushButton("Search", self)
		self.search.move(75, 100)
		self.search.clicked.connect(self.return_value)
		self.search.setEnabled(False)

		self.setWindowTitle("Find")

	def open_window(self):
		self.show()

	def text_changed(self):
		if self.input.text() != "":
			self.search.setEnabled(True)
		else:
			self.search.setEnabled(False)

	def return_value(self):
		self.emit(SIGNAL("return_value(QString)"), self.input.text())
		self.input.setText("")
		self.hide()

	def keyPressEvent(self, event):
		# Responds when user clicks key
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			if self.search.isEnabled():
				self.return_value()


class main_window(QtGui.QWidget):
	# Window to allow the user to set up the encryption/decryption settings,
	# select their source file, choose whether or not to create a copy, etc.

	# Window constructor
	def __init__(self, parent=None):
		super(main_window, self).__init__()
		#self.initThread()
		
		# Begin the user interface constructor
		self.initUI()

	def initUI(self):

		# Class resources
		self.title_font 			= QtGui.QFont("Lucida", 20)
		self.encryption_types 		= ["Affine", "Caesar (shift)"]
		self.transform_direction	= "encryption"
		self.transform_type 		= "affine"
		self.have_text 				= False
		self.alpha_validator 		= QtGui.QIntValidator(1, 1000000, self)
		self.beta_validator 		= QtGui.QIntValidator(0, 1000000, self)
		self.shift_validator 		= QtGui.QIntValidator(0, 1000000, self)

		# Initializing window
		self.resize(775,400)
		self.setWindowTitle("Encrpytion Suite")

		# Layouts
		self.main_vertical 			= QtGui.QVBoxLayout(self) # Outer layout
		self.main_horizontal 		= QtGui.QHBoxLayout() # Under self.logo in the self.main_vertical
		self.left_vertical 			= QtGui.QVBoxLayout() # First column on the self.main_horizontal
		self.right_vertical 		= QtGui.QVBoxLayout() # Second column on the self.main_horizontal
		self.right_upper_horizontal = QtGui.QHBoxLayout() # First row of self.right_vertical
		self.right_lower_horizontal = QtGui.QHBoxLayout() # Last for of self.right_vertical
		self.form_layout 			= QtGui.QStackedWidget() # List of layouts for the different encryption types 
		self.affine_layout 			= QtGui.QHBoxLayout() # Holds the alpha and beta inputs for affine
		self.shift_layout 			= QtGui.QHBoxLayout() # Holds the shift input for shift cipher
		self.shift_widget 			= QtGui.QWidget() # Parent for shift layout
		self.affine_widget 			= QtGui.QWidget() # Parent for affine layout

		# Widgets
		self.logo = QtGui.QLabel("Encryption Suite", self)
		self.logo.setFont(self.title_font)
		self.logo.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.main_vertical.addSpacing(18)
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

		# Menu bar widgets
		self.menu_bar 	= QtGui.QMenuBar(self)
		self.file_menu  = self.menu_bar.addMenu("File")
		self.edit_menu 	= self.menu_bar.addMenu("Edit")
		self.tool_menu 	= self.menu_bar.addMenu("Tools")
		self.menu_bar.resize(self.menu_bar.sizeHint())

		# Menu bar actions
		self.parse_text_action 	= self.file_menu.addAction("Import Text...", self.parse, QtGui.QKeySequence("Ctrl+O"))
		self.file_menu.addSeparator()
		self.save_action 		= self.file_menu.addAction("Save...", self.save, QtGui.QKeySequence("Ctrl+S"))
		self.file_menu.addSeparator()
		self.new_window_action 	= self.file_menu.addAction("New Window", self.new_window, QtGui.QKeySequence("Ctrl+Shift+N"))
		self.quit_action 		= self.file_menu.addAction("Quit", self.quit)
		
		self.clear_action 		= self.edit_menu.addAction("Clear", self.clear, QtGui.QKeySequence("Ctrl+E"))
		self.edit_menu.addSeparator()
		self.find_action		= self.edit_menu.addAction("Find...", self.find, QtGui.QKeySequence("Ctrl+F"))
		self.find_action.setEnabled(False)
		self.find_replace_action= self.edit_menu.addAction("Find and replace...", self.find_and_replace_launcher, QtGui.QKeySequence("Ctrl+Shift+F"))
		self.find_replace_action.setEnabled(False)

		# Child windows
		self.find_dialog = find_window()
		self.find_replace_dialog = find_replace_window()

		# Connecting signals and slots
		QtCore.QObject.connect(self.find_dialog, QtCore.SIGNAL("return_value(QString)"), self.rec_value)
		QtCore.QObject.connect(self.find_replace_dialog, QtCore.SIGNAL("return_value(QString)"), self.find_and_replace)

		# Showing the window
		self.show()
		self.encryption_type_selected()

	def find_and_replace_launcher(self):
		self.find_replace_dialog.open_window()

	def find_and_replace(self, value):
		# Slot the gets text to replace from find and replace dialog
		value = str(value)
		old = value[:value.find("|||")]
		new = value[value.find("|||")+3:]

		text = str(self.pastebox.toPlainText())
		text = text.replace(old, new)
		self.pastebox.setText(text)

	def rec_value(self, value):
		# Slot that gets text to search for from find dialog
		print value

	def find(self):
		# Allows user to locate all locations of text they input
		self.find_dialog.open_window() # Open the find dialog

	def new_window(self):
		self.child_window = main_window()

	def save(self):
		# Saves the text in the window
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Save As')
		if filename != "":
			text = self.pastebox.toPlainText()
			new_file = open(filename+".txt", 'w')
			new_file.write(text)

	def quit(self):
		# Quits entire application
		QtCore.QCoreApplication.instance().quit()

	def parse(self):
		# Pulls in text from file
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Select File')

		if filename != "":
			with open(filename, 'r') as source:
				data = source.read()
			self.pastebox.setText(data)

			if data != "":
				self.have_text = True
				self.find_action.setEnabled(True)
				self.find_replace_action.setEnabled(True)
			else:
				self.find_action.setEnabled(False)
				self.find_replace_action.setEnabled(False)
				self.have_text = False
			return

	def param_changed(self):
		# Called when user changes value in one of the key QLineEdit widgets
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
		# Called when user changes the text in the pastebox
		text = self.pastebox.toPlainText()
		if text != "":
			self.have_text = True
			self.find_action.setEnabled(True)
			self.find_replace_action.setEnabled(True)
		else:
			self.have_text = False
			self.find_action.setEnabled(False)
			self.find_replace_action.setEnabled(False)

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
		self.find_action.setEnabled(False)
		self.find_replace_action.setEnabled(False)
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
		app.setWindowIcon(QtGui.QIcon('resources/icon_300x300.png'))
		_ = main_window()
		sys.exit(app.exec_())



if __name__ == '__main__':
	main()
