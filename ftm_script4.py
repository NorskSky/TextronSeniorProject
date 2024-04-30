import os,sys,warnings,time
from multiprocessing import Process
os.sys.path.append('/home/jmonson/High-Precision-AD-DA-Board-Code/RaspberryPI/ADS1256/python3')
import ADS1256
from pydub import AudioSegment
from pydub.playback import play
apth = '/home/jmonson/Music/TwisterTheme.mp3'
song1 = AudioSegment.from_file(apth)
import numpy as np
warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=DeprecationWarning)
from scipy.io.wavfile import write
ADC = ADS1256.ADS1256()
ADC.ADS1256_init()

#audio_pth = str(sys.argv[1])
#print('{}'.format(audio_pth))
#song1 = AudioSegment.from_file(audio_pth)

duration = int(song1.duration_seconds)

def output_generate(audio_path,loudness=0):
    song = AudioSegment.from_file(audio_path)
    play(song+loudness)

def channel_collection(channel):
    t_end = time.time() + duration
    data = list()
    while time.time()<t_end:
        ADC_Value = ADC.ADS1256_GetAll()
        data.append(ADC_Value[channel])
    samplerate = int(len(data)/duration)
    npdata = np.array(data,dtype=np.int16)
    write('/home/jmonson/Music/sample_Ch{}.wav'.format(channel),samplerate,npdata)        

process1 = Process(target=output_generate, args=(apth,))
process1.start()
procs = []
for i in range(8):
    proc = Process(target=channel_collection, args=(i,))
    procs.append(proc)
    proc.start()
    
process1.join()
for proc in procs:
    proc.join()