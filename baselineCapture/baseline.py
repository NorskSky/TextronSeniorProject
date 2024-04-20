from time import time, sleep, perf_counter
from threading import Thread, Event
from pydub import AudioSegment
from pydub.playback import play
import ADS1256
import RPi.GPIO as GPIO
import errorHandler


#define linear sweep function
def linearSweep():
    with errorHandler.noalsaerr():
        linSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Lin-CA-10sec.mp3")
        print('Starting Linear Sine Sweep Audio on Outputs 1 & 2')
        play(linSweepMp3)
        sleep(1)
        print('Linear Sweep Complete')

#define exponential sweep function    
def exponentialSweep():
    expSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Exp-CA-10sec.mp3")
    print('Starting Exponential Sine Sweep Audio on Outputs 1 & 2')
    play(expSweepMp3)
    sleep(1)
    print('Exponential Sweep Complete')
    
#define ADC read function
def adcRead():
    t_end = time() + 10
    try:	
        ADC = ADS1256.ADS1256()
        ADC.ADS1256_init()
        sleep(0.1) 

        while time() < t_end:
            ADC_Value = ADC.ADS1256_GetAll()
            print ("0 ADC = %lf"%(ADC_Value[0]*5.0/0x7fffff))
            print ("1 ADC = %lf"%(ADC_Value[1]*5.0/0x7fffff))
            print ("2 ADC = %lf"%(ADC_Value[2]*5.0/0x7fffff))
            print ("3 ADC = %lf"%(ADC_Value[3]*5.0/0x7fffff))
            print ("4 ADC = %lf"%(ADC_Value[4]*5.0/0x7fffff))
            print ("5 ADC = %lf"%(ADC_Value[5]*5.0/0x7fffff))
            print ("6 ADC = %lf"%(ADC_Value[6]*5.0/0x7fffff))
            print ("7 ADC = %lf"%(ADC_Value[7]*5.0/0x7fffff))
            print ("\33[9A")
            
    except :
        GPIO.cleanup()
        print ("\r\nProgram end     ")
        exit()

# create two new threads
t1 = Thread(target=linearSweep)
t2 = Thread(target=adcRead)

# start the threads
t1.start()
t2.start()

# wait for the threads to complete
t1.join()
t2.join()

print(f'Baseline Capture Complete')
