from os1 import OS1
from os1.utils import raw_values, raw_packets
import os
from datetime import datetime


def handler(raw_packet):
    filename = 'Raw_' + str(getdatetime()) + '.txt'
    print("Generating output in " + filename)
    with open(filename, 'a') as f:
        packet = raw_packets(raw_packet)
        for vetorDadosColetados in zip(packet):
            f.write("{}\n".format(','.join(vetorDadosColetados)))


# def handler_bin(raw_packet):
#     filename = 'Raw_' + str(getdatetime()) + 'bin.txt'
#     print("Generating output in " + filename)
#     with open(filename, 'ab') as f:
#         f.write(raw_packet)


def getdatetime():
    now = datetime.now()
    date_time = now.strftime("%m%d%Y_%H%M")
    print("Running at", date_time)
    return date_time


def startouster():
    os1 = OS1('10.5.5.86', '10.5.5.1', mode='1024x10')
    os1.start()
    os1.run_forever(handler)
    # os1.run_forever(handler_bin)


while True:
    hostname = "10.5.5.86"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        startouster()
        print("running")
        break
