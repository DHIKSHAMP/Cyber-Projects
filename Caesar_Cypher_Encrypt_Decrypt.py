import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QRadioButton, QTextEdit, QMessageBox, QFrame
)
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QPropertyAnimation, QPoint


def caesar_cipher(text, shift, mode="encrypt"):
    result = ""
    if mode == "decrypt":
        shift = -shift
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result += chr(shifted + base)
        else:
            result += char
    return result



class CaesarCipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caesar Cipher - PyQt App with Background")
        self.setGeometry(100, 100, 700, 500)

        # Set background image
        self.set_background("C:/Users/ACER/Documents/Cyber journey/Practise Cyber Projects/background.gif")
        
        self.heading = QLabel("Caesar Cipher", self)
        self.heading.setStyleSheet("""
            QLabel {
            font-size: 32px;
            font-weight: bold;
            color: #04116E;
            background-color: #D9DDFA;
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 48px;
            }
        """)
        self.heading.setAlignment(Qt.AlignRight)
        


        # Central Frame to hold widgets
        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(173, 216, 230, 200);  /* light blue, semi-transparent */
                border-radius: 15px;
                padding: 20px;
            }
        """)
        self.container.setFixedWidth(450)

        # Widgets
        self.input_label = QLabel("Enter Message:")
        self.input_text = QTextEdit()
        self.input_text.setStyleSheet("""
            QTextEdit {
            background-color: #f0f8ff;      /* Light blue background */
            color: #003366;                 /* Dark blue text */
            border: 1px solid #66a3ff;
            border-radius: 8px;
            padding: 6px;
            font-size: 24px;
                }
            """)

        self.shift_label = QLabel("Shift Value:")
        self.shift_input = QLineEdit()

        self.encrypt_radio = QRadioButton("Encrypt")
        self.encrypt_radio.setChecked(True)
        self.decrypt_radio = QRadioButton("Decrypt")
        self.encrypt_radio.setStyleSheet("color: #a32e2e; font-weight: bold;")
        self.decrypt_radio.setStyleSheet("color: #a32e2e; font-weight: bold;")


        self.run_button = QPushButton("Run")
        self.run_button.setStyleSheet("""
            QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #e0f7fa, stop:1 #80deea);
            color: black;
            font-weight: bold;
            padding: 8px 16px;
            border: none;
            border-radius: 10px;
            font-size: 24px;
            }
            QPushButton:hover {
            background-color: #3346D6;
            }
            """)
        self.clear_button = QPushButton("Clear Result")
        self.clear_button.setStyleSheet("""
            QPushButton {
            background-color: #3346D6;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            }
            QPushButton:hover {
            background-color: #46C4F2;
            }
            """)


        self.result_label = QLabel("Result:")
        self.result_output = QTextEdit()
        self.result_output.setStyleSheet("""
            QTextEdit {
            background-color: #f0f8ff;      /* Light blue background */
            color: #003366;                 /* Dark blue text */
            border: 1px solid #66a3ff;
            border-radius: 8px;
            padding: 6px;
            font-size: 24px;
            }
            """)

        self.result_output.setReadOnly(True)

        # Layout inside container
        inner_layout = QVBoxLayout()
        inner_layout.addWidget(self.input_label)
        inner_layout.addWidget(self.input_text)
        

        h_shift = QHBoxLayout()
        h_shift.addWidget(self.shift_label)
        h_shift.addWidget(self.shift_input)
        inner_layout.addLayout(h_shift)

        h_mode = QHBoxLayout()
        h_mode.addWidget(self.encrypt_radio)
        h_mode.addWidget(self.decrypt_radio)
        inner_layout.addLayout(h_mode)

        inner_layout.addWidget(self.run_button)
        inner_layout.addWidget(self.result_label)
        inner_layout.addWidget(self.result_output)
        inner_layout.addWidget(self.clear_button)


        self.container.setLayout(inner_layout)

        # Outer layout to center the container
        outer_layout = QVBoxLayout()
        outer_layout.setSpacing(20)
        outer_layout.addWidget(self.heading, alignment=Qt.AlignTop | Qt.AlignHCenter)
        outer_layout.setContentsMargins(100, 20, 490, 20)  # left, top, right, bottom
        outer_layout.addStretch()
        outer_layout.addWidget(self.container, alignment=Qt.AlignRight)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

        self.run_button.clicked.connect(self.process)
        self.clear_button.clicked.connect(self.clear_result)

    def animate_heading(self):
    # Center based on window width
        center_x = self.width() // 2 - self.heading.width() // 2
        self.heading.move(center_x, self.heading.y())

        self.anim = QPropertyAnimation(self.heading, b"pos")
        self.anim.setDuration(1200)
        self.anim.setStartValue(QPoint(center_x, -100))
        self.anim.setEndValue(QPoint(center_x, 30))  # final Y position
        self.anim.start()


    def set_background(self, gif_path):
        movie = QMovie(gif_path)
        if not movie.isValid():
            print(f"Error: Failed to load gif at {gif_path}")
            return

        self.bg_label = QLabel(self)
        self.bg_label.setMovie(movie)
        self.bg_label.setScaledContents(True)
        self.bg_label.resize(self.size())
        self.bg_label.lower()  # Send background behind other widgets
        movie.start()
        
    def resizeEvent(self, event):
        if hasattr(self, 'bg_label'):
            self.bg_label.resize(self.size())
            self.animate_heading()
        super().resizeEvent(event)

    def process(self):
        text = self.input_text.toPlainText()
        shift_val = self.shift_input.text()

        try:
            shift = int(shift_val)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Shift value must be an integer.")
            return

        mode = "encrypt" if self.encrypt_radio.isChecked() else "decrypt"
        result = caesar_cipher(text, shift, mode)
        self.result_output.setPlainText(result)
        
    def clear_result(self):
        self.result_output.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarCipherApp()
    window.showMaximized()
    sys.exit(app.exec_())
