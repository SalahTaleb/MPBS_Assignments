import RPi.GPIO as RPI
import time
import statistics
#import matplotlib.pyplot as mpl
from matplotlib import pyplot as mpl



#Acquisition of range measurement data
def init_ultrasonic(pin_trigger, pin_echo):
    RPI.setmode(RPI.BCM)
    RPI.setup(pin_trigger, RPI.OUT, pull_up_down=RPI.PUD_OFF)
    RPI.setup(pin_echo, RPI.IN, pull_up_down=RPI.PUD_OFF)

def get_echo_time(pin_trigger, pin_echo):
        while True:
            RPI.output(pin_trigger, True)
            time.sleep(0.001)
            RPI.output(pin_trigger, False)
            while not RPI.input(pin_echo):
                raising_time = time.time()
            while RPI.input(pin_echo):
                falling_time = time.time()
            t_echo = falling_time - raising_time
            return t_echo


#Calibration routine
def calibrate_ultrasonic(pin_trigger, pin_echo):
    buzzer = 18
    RPI.setup(buzzer, RPI.OUT, pull_up_down=RPI.PUD_OFF)
    while True:
        RPI.output(buzzer, True)
        measurments=[]
        for i in range(0,10):
            measurments.append(get_echo_time(pin_trigger, pin_echo))
            time.sleep(0.5)

        RPI.output(buzzer, False)
        mpl.figure(figsize=(10, 6))
        mpl.plot(measurments, marker='o', color='blue', linestyle='-', label='Ultrasonic Measurements')
        mpl.title('Ultrasonic readings')
        mpl.xlabel('reading number')
        mpl.ylabel('Echo time')
        mpl.legend()
        mpl.grid(True)
        mpl.show()
        std_dev = statistics.stdev(measurments)
        mean_of_measurments = statistics.mean(measurments)
        if std_dev < 0.1:
            a = 0.1 / mean_of_measurments
            return a * mean_of_measurments
        else:
            return -1 * mean_of_measurments

#Overall program routine

#Defining GPIOs
up_button_gpio= 26
down_button_gpio= 13
pin_trigger = 16
pin_echo = 12

init_ultrasonic(pin_trigger, pin_echo)

#Initializing inputs & outputs
RPI.setup(up_button_gpio, RPI.IN, pull_up_down=RPI.PUD_OFF)
RPI.setup(down_button_gpio, RPI.IN, pull_up_down=RPI.PUD_OFF)

#Calling the needed functions
gpio_list_input=[up_button_gpio, down_button_gpio]
while True:
    for gpio in gpio_list_input:
        state=RPI.input(gpio)
        if not state:
            if gpio == up_button_gpio:
                get_echo_time(pin_trigger, pin_echo)
                distance = get_echo_time(pin_trigger, pin_echo) * 17241
                print('the distance is')
                print(round(distance, 0))
                time.sleep(1)
            if gpio == down_button_gpio:
                calibrated_tech = get_echo_time(pin_trigger, pin_echo) * calibrate_ultrasonic(pin_trigger, pin_echo)
                calibrated_distance = calibrated_tech * 17241
                print('Calibrated distance is ')
                print(round(calibrated_distance, 0))


























