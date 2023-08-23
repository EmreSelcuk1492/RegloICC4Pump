import sys
import serial
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget

class PumpControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pump Control GUI")
        self.setGeometry(100, 100, 400, 300)

        self.init_ui()
        self.init_serial_communication()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        label = QLabel("Pump Control System")
        layout.addWidget(label)

        self.start_button = QPushButton("Start Pump")
        layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_pump)

        self.stop_button = QPushButton("Stop Pump")
        layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop_pump)

        self.speed_label = QLabel("Enter Speed:")
        layout.addWidget(self.speed_label)

        self.speed_input = QLineEdit()
        layout.addWidget(self.speed_input)

        central_widget.setLayout(layout)

    def init_serial_communication(self):
        self.serial_port = 'COM7'  # Replace with your pump's serial port
        self.ser = None
        self.connect()

    def connect(self):
        try:
            self.ser = serial.Serial(self.serial_port, baudrate=9600, timeout=5)
            print("Serial connection established.")
        except serial.SerialException as e:
            print("Error:", e)

    def send_receive(self, command):
        if not self.ser:
            print("Serial port not connected.")
            return

        try:
            self.ser.write(command.encode('ASCII'))
            response = self.ser.read_until(b'\x0D')
            print("Sent command:", command)
            print("Received response:", response)
        except serial.SerialException as e:
            print("Error:", e)

    def start_pump(self):
        self.send_receive("2L\x0D")  # Set the flow rate
        self.send_receive("2K\x0D")  # Set direction to clockwise
        speed = self.speed_input.text()
        self.send_receive(f"2S{speed.zfill(6)}\x0D")  # Set speed
        self.send_receive("2H\x0D")  # Turn pump on

    def stop_pump(self):
        self.send_receive("2I\x0D")  # Turn pump off

    def disconnect(self):
        if self.ser:
            self.ser.close()
            print("Serial connection closed.")

def main():
    app = QApplication(sys.argv)
    window = PumpControlGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
