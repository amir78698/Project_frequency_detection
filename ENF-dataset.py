import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import glob

wav_list = []
for i in glob.glob("H1/*.wav"):
    fs, audio = wav.read(i)
    wav_list.append(audio)


for j in wav_list:
    plt.specgram(j, Fs=fs, NFFT=32768, scale_by_freq=100, noverlap=900)
    plt.ylim([0, 100])
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.set_cmap("jet")
    plt.title("Audio Spectrum with ENF Signal")
    plt.show()