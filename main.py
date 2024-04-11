import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLCDNumber

from lib.lexica import MyLexer
from lib.parsers import MyParser

class MainWindow(QMainWindow):

    button_1: QPushButton
    button_2: QPushButton
    button_3: QPushButton
    button_4: QPushButton
    button_5: QPushButton
    button_6: QPushButton
    button_7: QPushButton
    button_8: QPushButton
    button_9: QPushButton
    button_0: QPushButton
    button_plus: QPushButton
    button_star: QPushButton
    button_equal: QPushButton
    button_clear: QPushButton
    input_text:QLineEdit
    post_fix_text:QLineEdit
    pre_fix_text:QLineEdit
    output_lcd:QLCDNumber

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("main.ui", self)

        #### Binding button to function ####
        # # Method 1:
        # self.button_1.clicked.connect(self.push_1)
        # # Method 2:
        self.button_1.clicked.connect(lambda: self.push("1"))
        self.button_2.clicked.connect(lambda: self.push("2"))
        self.button_3.clicked.connect(lambda: self.push("3"))
        self.button_4.clicked.connect(lambda: self.push("4"))
        self.button_5.clicked.connect(lambda: self.push("5"))
        self.button_6.clicked.connect(lambda: self.push("6"))
        self.button_7.clicked.connect(lambda: self.push("7"))
        self.button_8.clicked.connect(lambda: self.push("8"))
        self.button_9.clicked.connect(lambda: self.push("9"))
        self.button_0.clicked.connect(lambda: self.push("0"))
        self.button_plus.clicked.connect(lambda: self.push_literal("+"))
        self.button_star.clicked.connect(lambda: self.push_literal("x"))
        self.button_equal.clicked.connect(self.push_equal)
        self.button_clear.clicked.connect(self.clear)

    def push_1(self):
        current_text:str = self.input_text.text()
        self.input_text.setText(f"{current_text}1")
    
    def push(self, text:str):
        current_text:str = self.input_text.text()
        self.input_text.setText(f"{current_text}{text}")

    def push_literal(self, text:str):
        current_text:str = self.input_text.text()
        self.input_text.setText(f"{current_text} {text} ")

    def clear(self):
        current_text:str = ''
        self.input_text.setText(current_text)
        self.output_lcd.display('0')
        self.pre_fix_text.setText('')
        self.post_fix_text.setText('')
    
    def push_equal(self):
        lexer = MyLexer()
        parser = MyParser()
        
        input_text = self.input_text.text()
        tokens = lexer.tokenize(input_text)

        print(tokens)

        result = parser.parse(tokens)
        prefix = parser.pre_fix_expr(input_text)
        postfix = parser.post_fix_expr(input_text)

        self.output_lcd.display(result)
        self.post_fix_text.setText(postfix)
        self.pre_fix_text.setText(prefix)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()