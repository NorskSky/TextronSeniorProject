from time import time, sleep, perf_counter
from threading import Thread, Event
from pydub import AudioSegment
from pydub.playback import play
import ADS1256
import RPi.GPIO as GPIO
import errorHandler
import inputSelection


t_end = time() + duration
numGMAOutSelected = inputSelection.
GMAOutMax = 0 * numGMAOutSelected
GMAOutMin = 5 * numGMAOutSelected


#define linear sweep function
def LinearSweep():
    with errorHandler.noalsaerr():
        linSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Lin-CA-10sec.mp3")
        print('Starting Linear Sine Sweep Audio on Outputs 1 & 2')
        play(linSweepMp3)
        sleep(1)
        print('Linear Sweep Complete')

#define exponential sweep function    
def ExponentialSweep():
    expSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Exp-CA-10sec.mp3")
    print('Starting Exponential Sine Sweep Audio on Outputs 1 & 2')
    play(expSweepMp3)
    sleep(1)
    print('Exponential Sweep Complete')
    
#define ADC Min/Max Capture Function
def ADCRead():
    i = 0
    try:	
        ADC = ADS1256.ADS1256()
        ADC.ADS1256_init()
        sleep(0.1) 

        while time() < t_end:
            ADC_Value = ADC.ADS1256_GetAll()
            for i in range (numGMAOutSelected-1):
                if %(ADC_Value[i]*5.0/0x7fffff) > GMAOutMax[i]:
                    GMAoutMax[i] == %(ADC_Value[i]*5.0/0x7fffff)
                if  (ADC_Value[i]*5.0/0x7fffff) < GMAoutMin[i]:
                    GMAoutMin[i] == %(ADC_Value[i]*5.0/0x7fffff)
                i+=1
            
    except :
        GPIO.cleanup()
        print ("\r\nProgram end     ")
        exit()

#Select Input and Print Current Baseline
inputSelection.inputSelection()



# create two new threads
t1 = Thread(target=LinearSweep)
t2 = Thread(target=ADCRead)

# start the threads
t1.start()
t2.start()

# wait for the threads to complete
t1.join()
t2.join()

print(f'ADC Read Complete')