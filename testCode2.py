import serial
import time
import keyboard
from pumpTimer import PumpTimer

class TestSerialCommunication:
    def __init__(self, port):
        self.serial_port = port
        self.ser = None

### SERIAL COMMUNICATION ###

    def connect(self):
        try:
            self.ser = serial.Serial(self.serial_port, baudrate=9600, timeout=0.1)
            print("Serial connection established.")
        except serial.SerialException as e:
            print("Error:", e)

    def send_receive(self, command):
        if not self.ser:
            print("Serial port not connected.")
            return
        try:
            self.ser.write(command.encode('ASCII'))
            response = self.ser.read_until('\x0D')
            print("Sent command:", command)
            print("Received response:", response)
            return response
        except serial.SerialException as e:
            print("Error:", e)
            
    def disconnect(self):
        if self.ser:
            self.ser.close()
            print("Serial connection closed.")
    
### System Returns ###

        
### Operational Modes and Settings ###
    def setPumpDirection(self, pumpNumber, direction):
        if direction == 0:
            self.send_receive(f"{pumpNumber}J\x0D")
        else:
            self.send_receive(f"{pumpNumber}K\x0D")
            
    def setPumpRPM(self, pumpNumber, speed):
        self.send_receive(f"{pumpNumber}L\x0D")  # Set the flow rate
        self.send_receive(f"{pumpNumber}S{self._discrete3(speed)}\x0D")  # Set speed
    
    def setTubeDiameter(self, pumpNumber, width):
        self.send_receive(f"{pumpNumber}+{self._discrete2(width)}\x0D") #Set tube diameter
        
    def setFlowRate(self, pumpNumber, volume):
        self.send_receive(f"{pumpNumber}M\x0D")  # Set the flow rate mode
        self.send_receive(f"{pumpNumber}f{self._volume2(volume)}\x0D") # Set mL/min rate
    """"
    def resetCalibration(self):
        self.send_receive("000000\x0D") # Sets pump to default settings
    """
### CALIBRATION CONTROLS ###

            
    def setCalibration(self, pumpNumber, direction, volume, calTime):         
        self.send_receive(f"{pumpNumber}xU{self._volume2(volume)}\x0D")  # Set the calibration volume
        #calTime = [time, units of Time] 's' = seconds, 'm' = minutes, 'h' = hours
        self.send_receive(f"{pumpNumber}xW{self._time2(calTime[0], calTime[1])}\x0D")
        self.send_receive(f"{pumpNumber}xRJ\x0D")
        
    def startCalibration(self, pumpNumber):
        self.send_receive(f"{pumpNumber}xY\x0D")
    
    def setCalibrationMeasured(self, pumpNumber):
        time.sleep(3)
        while str(self.send_receive(f"{pumpNumber}E\x0D").decode()) != "-": #Checking if pump is done running
            time.sleep(1)
        #Requesting user for mL measured for pump to calibrate to, 0.1 = 100 uL (micro-militers)
        print("Please enter your measured value in mL:")
        volume = input()
        #Sets pump volume to input from user
        self.send_receive(f"{pumpNumber}xV{self._volume2(float(volume))}\x0D")
            
### ACTUATION CONTROLS ###

    def allPumpsOn(self):
        #self.send_receive("1H\x0D")
        #self.send_receive("2H\x0D")
        self.send_receive("3H\x0D")
        self.send_receive("4H\x0D")
        
    def allPumpsOff(self):
        #self.send_receive("1I\x0D")
        #self.send_receive("2I\x0D")
        self.send_receive("3I\x0D")
        self.send_receive("4I\x0D")

### CONVERSION METHODS ###

    def _time1(self, number, units='s'):
        """Convert number to 'time type 1'.

        1-8 digits, 0 to 35964000 in units of 0.1s
        (0 to 999 hr)
        """
        number = 10 * number  # 0.1s
        if units == 'm':
            number = 60 * number
        if units == 'h':
            number = 60 * number
        return str(min(number, 35964000)).replace('.', '')

    def _time2(self, number, units):
        """Convert number to 'time type 2'.

        8 digits, 0 to 35964000 in units of 0.1s, left-padded with zeroes
        (0 to 999 hr)
        """
        number = 10 * number  # 0.1s
        if units == 'm':
            number = 60 * number
        if units == 'h':
            number = 60 * number
        return str(min(number, 35964000)).replace('.', '').zfill(8)

    def _volume2(self, number):
        # convert number to "volume type 2"
        number = '%.3e' % abs(number)
        number = number[0] + number[2:5] + number[-3] + number[-1]
        return str(number)
        
    def _volume1(self, number):
        # convert number to "volume type 1"
        number = '%.3e' % abs(number)
        number = number[0] + number[2:5] + 'E' + number[-3] + number[-1]
        return number

    def _discrete2(self, number):
        # convert float to "discrete type 2"
        number = int(number * 100)
        s = str(number)
        return str(number).zfill(4)

    def _discrete3(self, number):
        """Convert number to 'discrete type 3'.

        6 digits, 0 to 999999, left-padded with zeroes
        """
        number = int(number * 100)
        s = str(number)
        return str(number).zfill(6)


def main():

    serial_port = 'COM7'  # Replace with your pump's serial port
    test_comm = TestSerialCommunication(serial_port)
    test_comm.connect() 
    
    """"
    #Example Calibration Loop
    userInput = ""
    while userInput.capitalize() != 'Q':
        test_comm.setTubeDiameter(4, 0.38) #Tube diameter at channel 4 to 0.38mL
        test_comm.setCalibration(4, 0, 3, [2, 'h']) #Pump 4, clockwise = 0, 0.2mL in 60seconds
        test_comm.startCalibration(4) #Start Pump 4 calibration
        test_comm.setCalibrationMeasured(4) #Set Calibration Measured -> Looping function
        print("NEW CYCLE: Press enter to continue or 'q' to quit")
        userInput = input()

    test_comm.disconnect()
    """

    #Example Running Loop with Pump Timer
    
    pump_timer = PumpTimer(30)
    print("Press 'q' to pause the timer.")
    test_comm.setTubeDiameter("3", 0.38) #Setting channel 3 pump to a diameter of 0.13 mL
    test_comm.setTubeDiameter("4", 0.38) #Setting channel 3 pump to a diameter of 0.13 mL
    test_comm.setPumpDirection("3", 0)
    test_comm.setPumpDirection("4", 1)
    test_comm.setFlowRate("3", 0.35) #Setting channel 3 to flow rate mode - RPM speed dependent on Tube Diameter
    test_comm.setFlowRate("4", 0.30) #Setting channel 3 to flow rate mode - RPM speed dependent on Tube Diameter
    pump_timer.start()
    test_comm.allPumpsOn()
    
    while pump_timer.running:
        if keyboard.is_pressed('q'):  # Check for 'q' key
            test_comm.allPumpsOff()
            pump_timer.pause()
            print("Timer paused.")
        elif keyboard.is_pressed('r'):
            test_comm.allPumpsOn()
            pump_timer.resume()
            print("Timer resumed.")
    
    pump_timer.join()
    test_comm.allPumpsOff()

    
if __name__ == "__main__":
    main()
