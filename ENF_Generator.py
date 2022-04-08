# ENF Generator (Concept based on a chirp function)
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
outputPath = os.path.join(currentPath, 'output')

# Define necessary variables
samplerate = 44100
audioLenth = 300
t = np.arange(0, audioLenth, 1/samplerate)
enfFrequency=50
frequencyDelta = 0.4
phase=0.25

integral=[]
q2=[]
enfSignal=[]

# Each ENF singnal has a small variation of 40 mHz/s, and does not exceed enfFrequency ± 0.1
# This function simulates the variation over time
def generateENF(t):
    ft= enfFrequency+frequencyDelta*np.cos(2*np.pi*t*phase)
    return ft

for i in range(len(t)-1):
    Y = [generateENF(t[i]), generateENF(t[i+1])]
    X = [t[i],t[i+1]]
    # Compute a single integral step
    iy = np.trapz(Y, x=X)
    integral.append(iy)

# Remove the last Element so that the lengths are the same
t=t[:-1]
#plt.plot(t,integral)
#plt.show()

# Create cumulative sum (retrieve f(t) from the single steps)
qsum=np.cumsum(integral)
#plt.plot(t,qsum)
#plt.show()

# Gernate the ENF-Signal 
for i in range(len(qsum)):
    e=np.cos(2*np.pi*qsum[i])
    enfSignal.append(e)
#plt.plot(t,enfSignal)
#plt.show()

# This part is only for checking the ENf signal
fourier = np.fft.fft(enfSignal)
# The fft contains the real and imaginary parts, we only need the real
fourier_side = fourier[0:int(len(t)/2)]
# Get a float array of the frequency
freq = np.fft.fftfreq(fourier.size, d=1/(samplerate))[0:int(len(t)/2)]

# Plot for visual check
fig, ax= plt.subplots()
ax.plot(freq, np.abs(fourier_side))
plt.ylim([0, 100])
ax.set_xlabel('frequency in Hz')
ax.set_ylabel('spectrum magnitude')
ax.set_xlim(0,samplerate/2)
plt.show()

# Write ENF to wave
amplitude = np.iinfo(np.int16).max
data = amplitude * np.array(enfSignal)
write(outputPath+f'/genENF-{enfFrequency}Hz.wav', samplerate, data.astype(np.int16))