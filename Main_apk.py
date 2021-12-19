from Filters import sample_rate, hFIRDOL, hFIR2GOR, hFIR3DOL, hFIR3GOR,\
                    hFIRCROSS, hFIR2CROSS, hFIR_CROSS_COMB1, hFIR2DOL,\
                    hFIRGOR

from tkinter.ttk import Label
from tkinter import ttk
import numpy as np
import serial
import tkinter as tk
import matplotlib.pyplot as plt

BAUD_RATE = 115200
PORT_COM = "COM3"
BUFOR_SIZE = 1024
BUFOR = list()

DESCRYPTION = '''Mix1:FIR,dolnoprzepustowy
Mix2:FIR dolnoprzepustowy
Mix3:FIR gornoprzepustowy
Mix4:FIR gornoprzepustowy
Mix5:FIR crossover, Mix1 + Mix3
Mix6:FIR crossover, Mix2 + Mix4
Mix7:FIR crossover, Mix8 + Mix9
Mix8:FIR dolnoprzepustowy
Mix9:FIR gornoprzepustowy
Mix10:Efekt echo
'''


class mixer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.ser = 0
        self.title("Mixer audio")
        self.geometry("600x700")
        self.config(bg='#80b0ff')
        self.f = 100
        self.x = np.linspace(0, 100, 1024)
        self.y = np.sin(self.f * self.x)
        self.y1 = list()
        self.authors = '''Praca inzynierska Adrian Brychner,Maciej Tonderski'''
        text_box = tk.Text(self, font=('American typewriter', 14),
                           background='#232323', foreground='yellow')
        text_box.place(x=50, y=550, height=100, width=500)
        text_box.insert(tk.END, DESCRYPTION)
        title_label = Label(self, text=self.authors, font=("fontsize", '15'))
        title_label.place(x=50, y=10)
        title_label.configure(background='#80b0ff', foreground='yellow')

        self.scrollbar = ttk.Scrollbar(self, orient='vertical',
                                       command=text_box.yview)
        self.scrollbar.place(x=570, y=550, width=20, height=100)

        style1 = ttk.Style()
        style1.theme_use('alt')
        style1.configure('TButton', font=('American typewriter', 14),
                         background='#232323', foreground='yellow')
        style1.map('TButton', background=[('active', '#ff0000')])

        Mix1 = ttk.Button(self, text="mix1", command=self.mix_1)
        Mix1.place(x=50, y=100, width=100, height=30)
        Mix2 = ttk.Button(self, text="mix2", command=self.mix_2)
        Mix2.place(x=50, y=200, width=100, height=30)
        Mix3 = ttk.Button(self, text="mix3", command=self.mix_3)
        Mix3.place(x=50, y=300, width=100, height=30)
        Mix4 = ttk.Button(self, text="mix4", command=self.mix_4)
        Mix4.place(x=50, y=400, width=100, height=30)
        Mix5 = ttk.Button(self, text="mix5", command=self.mix_5)
        Mix5.place(x=50, y=500, width=100, height=30)
        Mix6 = ttk.Button(self, text="mix6", command=self.mix_6)
        Mix6.place(x=450, y=100, width=100, height=30)
        Mix7 = ttk.Button(self, text="mix7", command=self.mix_7)
        Mix7.place(x=450, y=200, width=100, height=30)
        Mix8 = ttk.Button(self, text="mix8", command=self.mix_8)
        Mix8.place(x=450, y=300, width=100, height=30)
        Mix9 = ttk.Button(self, text="mix9", command=self.mix_9)
        Mix9.place(x=450, y=400, width=100, height=30)
        Mix10 = ttk.Button(self, text="mix10", command=self.mix_10)
        Mix10.place(x=450, y=500, width=100, height=30)
        connect = ttk.Button(self, text="Polacz sie z \n plytka ewaluacyjna ",
                             command=self.conncet)
        connect.place(x=225, y=100, width=170, height=70)

    def conncet(self):
        self.ser = serial.Serial(PORT_COM, BAUD_RATE)

    def mix_1(self):
        f1 = 1000
        f2 = 10000
        f3 = 20000
        x1 = np.linspace(0, 2, 400)
        y1 = np.sin(f1 * x1) + np.sin(f2 * x1) + np.sin(f3 * x1)
        output = filterFIR(y1, hFIRDOL)
        plt.figure(1)
        plt.plot(x1, output[0:len(x1)], '-')
        plt.plot(x1, y1, '-')
        self.show_frequency_response(hFIRDOL)

    def mix_2(self):
        self.show_frequency_response(hFIR2DOL)

    def mix_3(self):
        self.show_frequency_response(hFIRGOR)

    def mix_4(self):
        self.show_frequency_response(hFIR2GOR)

    def mix_5(self):
        self.show_frequency_response(hFIRCROSS)

    def mix_6(self):
        self.show_frequency_response(hFIR2CROSS)

    def mix_7(self):
        self.show_frequency_response(hFIR_CROSS_COMB1)

    def mix_8(self):
        self.show_frequency_response(hFIR3DOL)

    def mix_9(self):
        self.show_frequency_response(hFIR3GOR)

    def mix_10(self):
        echo_effect(self.y)
        plt.figure(2)
        plt.plot(self.x, BUFOR, "-.")
        plt.show()

    def show_frequency_response(self, filtr):
        plt.figure(10)
        H = np.abs(np.fft.fft(filtr, 1024))  # take the 1024-point FFT and ||
        H = np.fft.fftshift(H)  # make 0 Hz in the center
        w = np.linspace(0, sample_rate/2, len(H))  # x axis
        plt.plot(w, H, '-')
        plt.show()


def filterFIR(input, coef):
    sum = 0
    stat = list()
    TAPS = len(coef)
    NUM_SAMPLES = len(input)
    stat = [0 for i in range(0, TAPS+NUM_SAMPLES - 1)]

    for i in range(TAPS, NUM_SAMPLES):
        sum = 0
        for j in range(0, TAPS):
            sum += coef[j] * input[i-j]
        stat[i] = sum

    for i in range(0, TAPS - 1):
        sum = 0
        for j in range(0, i+1):
            sum += coef[j] * input[i-j]
        stat[i] = sum + stat[NUM_SAMPLES + 1]

    for i in range(NUM_SAMPLES, NUM_SAMPLES+TAPS - 1):
        sum = 0
        for j in range(0, NUM_SAMPLES + TAPS - i):
            sum += coef[TAPS - 1 - j] * input[i - TAPS - 1 + j]
        stat[i] = sum
    return stat


def echo_effect(input_samples):
    for i in range(BUFOR_SIZE):
        if i <= 200:
            BUFOR.append(input_samples[i])
        elif i >= 200 and i < 600:
            BUFOR.append(input_samples[i] * 0.7)
        elif i >= 600 and i <= 800:
            BUFOR.append(input_samples[i] * 0.5)
        else:
            BUFOR.append(input_samples[i] * 0.2)


if __name__ == "__main__":

    app = mixer()
    app.mainloop()
