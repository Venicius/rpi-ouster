from os1 import OS1
from os1.utils import raw_values
import os
from datetime import datetime


def handler(raw_packet):
    filename = 'Raw_' + str(getdatetime()) + '.txt'
    print("Generating output in " + filename)
    with open(filename, 'a') as f:
        ch, ch_range, reflectivity, intensity, timeStamp, encoderCount, measurementID, frameID, x, y, z, noise = raw_values(
            raw_packet)

        f.write("TimeStamp: " + str(timeStamp[0]) + " measurementID: " + str(measurementID[0]) + " frameID: " + str(frameID[0]) + "\n")
        for vetorDadosColetados in zip(ch, ch_range, encoderCount, reflectivity, intensity, x, y, z noise):

            linhaImpressaNoArquivo = str(vetorDadosColetados)
            linhaImpressaNoArquivo = linhaImpressaNoArquivo.replace(',', ' ')
            linhaImpressaNoArquivo = linhaImpressaNoArquivo.replace('(', ' ')
            linhaImpressaNoArquivo = linhaImpressaNoArquivo.replace(')', ' ')
            f.write(linhaImpressaNoArquivo + "\n")


def getdatetime():
    now = datetime.now()
    date_time = now.strftime("%m%d%Y_%H%M")
    print("Running at", date_time)
    return date_time


def startouster():
    os1 = OS1('10.5.5.86', '10.5.5.1', mode='1024x10')
    os1.start()
    os1.run_forever(handler)


while True:
    hostname = "10.5.5.86"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        startouster()
        print("running")
        break
