import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget

class PumpControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pump Control GUI")
        self.setGeometry(100, 100, 400, 300)
        
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        label = QLabel("Pump Control System")
        layout.addWidget(label)

        start_button = QPushButton("Start Pump")
        layout.addWidget(start_button)

        stop_button = QPushButton("Stop Pump")
        layout.addWidget(stop_button)

        speed_label = QLabel("Enter Speed:")
        layout.addWidget(speed_label)

        speed_input = QLineEdit()
        layout.addWidget(speed_input)

        central_widget.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = PumpControlGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
