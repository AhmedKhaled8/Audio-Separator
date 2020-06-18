import matplotlib.pyplot as plt
import numpy as np
import wave

fileNames = ["bass", "drums", "piano", "vocals"]

for i in range(4):
    signalReader = wave.open("SeparationResults/InstrumentsSeparation/Fly Me To The Moon -- Beegie Adair Trio/{}.wav".format(fileNames[i]))
    signal = signalReader.readframes(-1)
    signal = np.fromstring(signal, "Int16")
    fs = signalReader.getframerate()
    time = np.linspace(0, len(signal)/fs, num=len(signal))
    plt.figure(i)
    plt.title(fileNames[i].capitalize())
    plt.plot(time, signal)

plt.show()
