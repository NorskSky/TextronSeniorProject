from pydub import AudioSegment
from pydub.playback import play
import time

linearSweep = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Lin-CA-10sec.mp3")
expSweep = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Exp-CA-10sec.mp3")

play(linearSweep)
time.sleep(3)
play(expSweep)
