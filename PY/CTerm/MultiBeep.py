import os
import sys
import time
import urllib.request as ulib
import winsound
from multiprocessing.dummy import Pool as ThreadPool

import math
import wave
import struct

defaultTime = 100
pathOutput = "G:/Programs/c++.txt"
sample_rate = 44100.0


frequencies = {"c0" : 16, 
"C0" : 17, 
"d0" : 18, 
"D0" : 19, 
"e0" : 20, 
"f0" : 21, 
"F0" : 23, 
"g0" : 24, 
"G0" : 25, 
"a0" : 27, 
"A0" : 29, 
"b0" : 30, 
"c1" : 32, 
"C1" : 34, 
"d1" : 36, 
"D1" : 38, 
"e1" : 41, 
"f1" : 43, 
"F1" : 46, 
"g1" : 49, 
"G1" : 51, 
"a1" : 55, 
"A1" : 58, 
"b1" : 61, 
"c2" : 65, 
"C2" : 69, 
"d2" : 73, 
"D2" : 77, 
"e2" : 82, 
"f2" : 87, 
"F2" : 92, 
"g2" : 98, 
"G2" : 103, 
"a2" : 110, 
"A2" : 116, 
"b2" : 123, 
"c3" : 130, 
"C3" : 138, 
"d3" : 146, 
"D3" : 155, 
"e3" : 164, 
"f3" : 174, 
"F3" : 185, 
"g3" : 196, 
"G3" : 207, 
"a3" : 220, 
"A3" : 233, 
"b3" : 246, 
"c4" : 261, 
"C4" : 277, 
"d4" : 293, 
"D4" : 311, 
"e4" : 329, 
"f4" : 349, 
"F4" : 369, 
"g4" : 392, 
"G4" : 415, 
"a4" : 440, 
"A4" : 466, 
"b4" : 493, 
"c5" : 523, 
"C5" : 554, 
"d5" : 587, 
"D5" : 622, 
"e5" : 659, 
"f5" : 698, 
"F5" : 739, 
"g5" : 783, 
"G5" : 830, 
"a5" : 880, 
"A5" : 932, 
"b5" : 987, 
"c6" : 1046, 
"C6" : 1108, 
"d6" : 1174, 
"D6" : 1244, 
"e6" : 1318, 
"f6" : 1396, 
"F6" : 1479, 
"g6" : 1567, 
"G6" : 1661, 
"a6" : 1760, 
"A6" : 1864, 
"b6" : 1975, 
"c7" : 2093, 
"C7" : 2217, 
"d7" : 2349, 
"D7" : 2489, 
"e7" : 2637, 
"f7" : 2793, 
"F7" : 2959, 
"g7" : 3135, 
"G7" : 3322, 
"a7" : 3520, 
"A7" : 3729, 
"b7" : 3951, 
"c8" : 4186, 
"C8" : 4434, 
"d8" : 4698, 
"D8" : 4978, 
"e8" : 5274, 
"f8" : 5587, 
"F8" : 5919, 
"g8" : 6271, 
"G8" : 6644, 
"a8" : 7040, 
"A8" : 7458, 
"b8" : 7902
}

def blockextractor(path):
    blocks = []
    temp = []

    try:
        with open(path) as f:
            text = f.read().splitlines()
    except:
        text = path

        for line in text:
            if line:
                temp.append(line)
            else:
                blocks.append(temp)
                temp = []
        
    return blocks

def block2letter(block, multiVoices = False):

    if not multiVoices:
        letters = ["-"]*26

        for line in block:
            octave = str(line[:1])
            characters = line[2:-1]
            for charIndex in range(len(characters)):
                if characters[charIndex] != "-" and letters[charIndex] == "-":
                    letters[charIndex] = f"{characters[charIndex]}{octave}"
        return letters
    
    else:
        letters = [["-"]*26 for voice in range(len(block))]

        voiceIndex = 0
        for line in block:
            octave = str(line[:1])
            characters = line[2:-1]
            for charIndex in range(len(characters)):
                if characters[charIndex] != "-":
                    letters[voiceIndex][charIndex] = f"{characters[charIndex]}{octave}"
            voiceIndex += 1
        return letters


def url2string(url):

    html = ulib.urlopen(url).read().splitlines()
    searchParam = "<br />"
    emptyParam = "b'<br />'"
    foundLines = []
    parsedLines = []

    for line in html:
        line = str(line)
        if searchParam in line:
            foundLines.append(line)
        
    for line in foundLines:

        if line != emptyParam:
            firstSweep = line.split("<")
            secondSweep = firstSweep[1].split(">")

            parsedLine = secondSweep[1]
            parsedLines.append(parsedLine)
       
        else:
            parsedLines.append("")
    
    return parsedLines

def letters2sound(letters):
    for letter in letters:
            if letter != "-":                       
                winsound.Beep(frequencies[letter], defaultTime)
            else:
                time.sleep(defaultTime/1000)

#################################################################################################

def append_silence(audio, duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)): 
        audio.append(0.0)

def append_sinewave(audio, freq=440.0, duration_milliseconds=500, volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :) 
    """ 

    #global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * ( x / sample_rate )))


def save_wav(audio, file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the 
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

#################################################################################################

def main():
    #blocks = blockextractor("F:/Downloads/wii.txt")

    while True:
        os.system("cls")
        print(r"""
         _______  _______  _______  _______  __   __  
        |  _    ||       ||       ||       ||  | |  |
        | |_|   ||    ___||    ___||    _  ||  |_|  |
        |       ||   |___ |   |___ |   |_| ||       |
        |  _   | |    ___||    ___||    ___||_     _|
        | |_|   ||   |___ |   |___ |   |      |   |  
        |_______||_______||_______||___|      |___|  

        [URL IMPORTADAS DE PIANOLETTERNOTES.BLOGSPOT]
                    """)

        play = input("0 = Exportar archivo de texto para C++ | 1 = Tocar cancion: ")
        if play == "0":
            outputName = input("Inserte el camino a donde exportar el archivo: ")
            pathOutput = f"{os.path.dirname(os.path.realpath(__file__))}/{outputName}.txt"
            print(f"El archivo sera importado a {pathOutput}")

        path = input("Inserte el camino o URL de la cancion: ")

        if path[:4] == "http":
            blocks = blockextractor(url2string(path))
        else:
            blocks = blockextractor(path)

        if play == "1":
        
            for block in blocks:
                letters = block2letter(block)
                voices = block2letter(block, True)
                
                pool = ThreadPool(len(voices))
                pool.map(letters2sound, voices)
                
        elif play == "0":
            with open(pathOutput, "w") as f:

                for block in blocks:
                    letters = block2letter(block)
                    for letter in letters:
                        if letter != "-":
                            f.write(f"Beep({frequencies[letter]},{defaultTime});\n")
                        else:
                            f.write(f"Sleep({defaultTime});\n")
        elif play == "2":
            
            audio = []

            for block in blocks:
                voices = block2letter(block, True)

            append_sinewave(audio, 1000, 500)
            append_silence(audio, 600)
            append_sinewave(audio, 1000, 500)
            append_sinewave(audio, 1500, 500)
            save_wav(audio, "sugfa.wav")

        else:
            break

main()
