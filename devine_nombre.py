import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class GuessNumberGame(QMainWindow):
    def __init__(self):
        super(GuessNumberGame, self).__init__()

        # Nombre secret à deviner
        self.secret_number = 42
        # Nombre maximum de tentatives
        self.max_attempts = 10
        # Compteur de tentatives
        self.attempt_count = 0

        self.setWindowTitle("Devine le Nombre")
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel(self)
        self.label.setGeometry(20, 20, 260, 40)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Devine le nombre entre 1 et 100")

        self.input = QLineEdit(self)
        self.input.setGeometry(20, 60, 260, 30)
        self.input.setAlignment(Qt.AlignCenter)

        self.button = QPushButton(self)
        self.button.setGeometry(20, 100, 260, 40)
        self.button.setText("Devine")
        self.button.clicked.connect(self.check_guess)

    def check_guess(self):
        guess = int(self.input.text())
        self.attempt_count += 1

        if guess == self.secret_number:
            self.label.setText(f"Félicitations, vous avez trouvé le nombre en {self.attempt_count} tentatives !")
            self.button.setEnabled(False)
        elif guess < self.secret_number:
            self.label.setText("Plus grand")
        else:
            self.label.setText("Plus petit")

        if self.attempt_count >= self.max_attempts:
            self.label.setText(f"Vous avez atteint le nombre maximum de tentatives ({self.max_attempts}). Le nombre secret était {self.secret_number}.")
            self.button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GuessNumberGame()
    window.show()
    sys.exit(app.exec_())
