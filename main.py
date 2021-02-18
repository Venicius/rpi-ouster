from os1 import OS1
from os1.utils import xyz_points, xyz_points_raw
import csv
import os
from datetime import datetime


def handler(raw_packet):
    #filename = 'Raw_' + str(getDateTime()) + '.txt'
    with open("saida-teste2.txt", 'a') as f:
        ch, ch_range, reflectivity, intensity, timeStamp, encoderCount, measurementID, frameID, x, y, z, noise = xyz_points_raw(
            raw_packet)
        f.write("*------------------------------------------------------* \n")
        f.write("timeStamp: " + str(timeStamp[0]) + "measurementID : " +
                str(measurementID[0]) + "frameID : " + str(frameID[0]) +
                "amazimuthDataBlockStatus 1" + "\n")

        for data in zip(ch, ch_range, encoderCount, reflectivity, intensity, x,
                        y, z, noise):
            f.write(str(data) + "\n")
            print(str(data))


def getDateTime():
    now = datetime.now()
    date_time = now.strftime("%m%d%Y_%H%M%S")
    print("Running at", date_time)
    return date_time


def startOuster():
    # OS1 sensor IP, destination IP, and resolution
    os1 = OS1('10.5.5.86', '10.5.5.1', mode='1024x10')
    # Inform the sensor of the destination host and reintialize it
    os1.start()
    # Start the loop which will handle and dispatch each packet to the handler
    # function for processing
    os1.run_forever(handler)


while True:
    hostname = "10.5.5.86"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        startOuster()
        print("running")
        break
