from time import time, sleep, perf_counter
from threading import Thread, Event
from pydub import AudioSegment
from pydub.playback import play
import ADS1256
import RPi.GPIO as GPIO
import errorHandler
import inputSelection


#Select input of GMA to be tested
GMAinputData = inputSelection.GMAInputSelection()
#Load baseline Min and Max values, correlating to the GMA input
GMAoutputs_Thresholds = inputSelection.GMAOutputSelection(GMAinputData)
adc_channels = inputSelection.ADC_Channels(GMAoutputs_Thresholds)
test = str(input('Enter L for Linear-Sweep test or E for Exponential-Sweep test.'))

#GMAOutMax = [0] * len(GMAoutputs_Thresholds)
#GMAOutMin = [5] * len(GMAoutputs_Thresholds)
GMAOutMax = dict(); GMAOutMin = dict()
for ch in adc_channels.keys():
    GMAOutMax[ch] = 0
    GMAOutMin[ch] = 5

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
def ADCRead(duration):
    print('starting ADC reads')
    t_end = time() + duration
    i = 0
    try:
        ADC = ADS1256.ADS1256()
        ADC.ADS1256_init()
        sleep(0.1) 

        while time() < t_end:
            ADC_Value = ADC.ADS1256_GetAll()
            for i in adc_channels.keys():
                if (ADC_Value[i]*5.0/0x7fffff) > GMAOutMax[i]:
                    GMAOutMax[i] = (ADC_Value[i]*5.0/0x7fffff)
                if (ADC_Value[i]*5.0/0x7fffff) < GMAOutMin[i]:
                    GMAOutMin[i] = (ADC_Value[i]*5.0/0x7fffff)
                i+=1
            
    except :
        GPIO.cleanup()
        print ("\r\nProgram end     ")
        #exit()
    print('Done with ADC Reads')

# create two new threads
if test == 'L':
    linSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Lin-CA-10sec.mp3")
    duration = int(linSweepMp3.duration_seconds)
    t1 = Thread(target=LinearSweep)
if test == 'E':
    expSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Exp-CA-10sec.mp3")
    duration = int(expSweepMp3.duration_seconds)
    t1 = Thread(target=ExponentialSweep)
t2 = Thread(target=ADCRead, args=(duration,))

# start the threads
t1.start()
t2.start()

# wait for the threads to complete
t1.join()
t2.join()

for i in adc_channels.keys():
    measured_min = GMAOutMin[i]
    measured_max = GMAOutMax[i]
    GMA_acceptable_range = GMAoutputs_Thresholds[adc_channels[i]]
    if measured_min < GMA_acceptable_range[0]:
        print('GMA Output {} Failed: Measured {} below {} threshold'.format(adc_channels[i],measured_min,GMA_acceptable_range))
    elif measured_max > GMA_acceptable_range[1]:
        print('GMA Output {} Failed: Measured {} above {} threshold'.format(adc_channels[i],measured_min,GMA_acceptable_range))
    else:
        print('GMA Output {} Passed!'.format(adc_channels[i]))

#print(f'ADC Read Complete')
