import serial
import time
import keyboard
import threading
import time

class PumpTimer(threading.Thread):
    def __init__(self, run_time):
        super().__init__()
        self.run_time = run_time
        self.running = True
        self.paused = False

    def run(self):
        start_time = time.time()
        while self.running:
            if not self.paused:
                current_time = time.time()
                elapsed_time = current_time - start_time
                print(f"Running time: {elapsed_time:.2f}")
                if elapsed_time >= self.run_time:
                    print("Pump time is up!")
                    self.running = False
                    break
                
            else:  # If paused, don't update the elapsed time
                start_time = time.time() - elapsed_time  # Reset the start time to account for paused time
                print(f"Pause time: {elapsed_time:.2f}")
               
            time.sleep(1) 


    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False