import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
class GuessNumber(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tab = [2, 8, 4, 32, 1, 16]
        self.res = 0
        self.current_index = 0

        self.label = QLabel("Le chiffre choisi est-il présent dans le tableau {} ?".format(self.current_index+1))
        self.label.setAlignment(Qt.AlignCenter)

        self.present_button = QPushButton("Présent")
        self.present_button.clicked.connect(self.present_clicked)

        self.not_present_button = QPushButton("Non présent")
        self.not_present_button.clicked.connect(self.not_present_clicked)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.present_button)
        self.button_layout.addWidget(self.not_present_button)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def present_clicked(self):
        self.res += self.tab[self.current_index]
        self.current_index += 1
        self.update_ui()

    def not_present_clicked(self):
        self.current_index += 1
        self.update_ui()

    def update_ui(self):
        if self.current_index == len(self.tab):
            self.label.setText("Le chiffre choisi est : " + str(self.res))
            self.present_button.setEnabled(False)
            self.not_present_button.setEnabled(False)
            return

        self.label.setText("Le chiffre choisi est-il présent dans le tableau {} ?".format(self.current_index+1))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Jeu de devinette binaire")
        self.setGeometry(100, 100, 500, 200)
        self.setCentralWidget(GuessNumber())

def print_dev():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    print_dev()
