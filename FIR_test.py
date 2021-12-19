from Filters import hFIRDOL, hFIR2GOR, hFIR3DOL, hFIR3GOR,\
                    hFIRCROSS, hFIR2CROSS, hFIR_CROSS_COMB1,\
                    hFIR2DOL, hFIRGOR, sample_rate

from Main_apk import filterFIR, BUFOR, BUFOR_SIZE
import numpy as np
import matplotlib.pyplot as plt

FILTR_FIRS_Hs = [hFIRDOL, hFIR2GOR, hFIR3DOL, hFIR3GOR, hFIRCROSS, hFIR2CROSS,
                 hFIR_CROSS_COMB1, hFIR2DOL, hFIRGOR]

if __name__ == "__main__":

    '''This is a scrypt to DSP functionaity '''
    '''  This is a part which test FIRes    '''

    f1 = 1000
    f2 = 10000
    f3 = 20000
    f4 = 30000

    x = np.linspace(0, 2, 400)
    y = np.sin(f1 * x) + np.sin(f2 * x) + np.sin(f3 * x) + np.sin(f4 * x)

    for h in FILTR_FIRS_Hs:
        output = filterFIR(y, h)
        plt.figure(1)
        plt.title("Sygnal w czasie rzeczywistym")
        plt.plot(x, output[0:len(x)], '-', label="Sygnał po filtracji")
        plt.plot(x, y, '-', label="Sygnał przed filtracja")
        plt.xlabel("Czas(s)")
        plt.ylabel("Amplituda")
        plt.legend()

        plt.figure(2)
        H = np.abs(np.fft.fft(output, 1024))  # take the 1024-point FFT and |A|
        H = np.fft.fftshift(H)  # make 0 Hz in the center
        w = np.linspace(0, sample_rate/2, len(H))  # x axis
        plt.plot(w, H, '.-')
        plt.title("Widmo sygalu po filtracji")
        plt.xlabel("Czestotliwość(Hz)")
        plt.ylabel("Amplituda")

        plt.figure(3)
        H = np.abs(np.fft.fft(y, 1024))  # take the 1024-point FFT and |A|
        H = np.fft.fftshift(H)  # make 0 Hz in the center
        w = np.linspace(0, sample_rate/2, len(H))  # x axis
        plt.plot(w, H, '.-')
        plt.title("Widmo sygalu przed filtracją")
        plt.xlabel("Czestotliwość(Hz)")
        plt.ylabel("Amplituda")

        plt.figure(4)
        H = np.abs(np.fft.fft(h, 1024))  # take the 1024-point FFT and |A|
        H = np.fft.fftshift(H)  # make 0 Hz in the center
        w = np.linspace(0, sample_rate/2, len(H))  # x axis
        plt.plot(w, H, '.-')
        plt.title("Widmo filtru")
        plt.xlabel("Czestotliwość(Hz)")
        plt.ylabel("Amplituda")
        plt.show()

    '''  This is a part which test echo effect algorytm   '''

    x_echo = np.linspace(0, 2, 1024)
    y_echo = np.sin(f1 * x_echo) + np.sin(f2 * x_echo) + np.sin(f3 * x_echo)

    for i in range(BUFOR_SIZE):
        if i <= 200:
            BUFOR.append(y_echo[i])
        elif i >= 200 and i < 600:
            BUFOR.append(y_echo[i] * 0.7)
        elif i >= 600 and i <= 800:
            BUFOR.append(y_echo[i] * 0.5)
        else:
            BUFOR.append(y_echo[i] * 0.2)

    plt.figure(1)
    plt.plot(x_echo, y_echo, '-')
    plt.title("Sygnał - testowy ")
    plt.xlabel("Czas(s)")
    plt.ylabel("Amplituda")

    plt.figure(2)
    plt.plot(x_echo, BUFOR, '-')
    plt.title("Sygnał - efekt echo ")
    plt.xlabel("Czas(s)")
    plt.ylabel("Amplituda")
    plt.show()
