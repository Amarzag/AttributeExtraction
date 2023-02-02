import time

"""
Cronometer class useful for check the execution
time of functions in any Python code
"""
class ChronoMeter():
    # properties
    start_time = 0
    end_time = 0

    """
    Method to start the cronometer
    """
    def start_chrono(self):
        self.start_time = self.current_milli_time()

    """
    Method for stopping chronometer
    """
    def stop_chrono(self):
        self.end_time = self.current_milli_time()

    """
    Method that return the execution time,
    the difference between end time and
    start time
    """
    def get_execution_time(self):
        return self.end_time - self.start_time

    """
    Method that print the execution time
    """
    def print_time(self):
        print(f"execution time: {self.get_execution_time()} ms")
    
    """
    Method that return the current time in 
    milliseconds
    """
    def current_milli_time(self):
        return round(time.time() * 1000)