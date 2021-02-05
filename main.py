from os1 import OS1
from os1.utils import xyz_points, xyz_points_raw
import csv



def handler(raw_packet):
    with open('saida.txt', 'a') as f:
        ch, timeStamp, encoderCount, measurementID, frameID = xyz_points_raw(raw_packet)
        writer = csv.writer(f, delimiter=' ')
        print("running")
        for data in zip(ch, timeStamp, encoderCount, measurementID, frameID):
            writer.writerow(data)


os1 = OS1('10.5.5.86', '10.5.5.1', mode='1024x20')  # OS1 sensor IP, destination IP, and resolution

# Inform the sensor of the destination host and reintialize it
os1.start()
# Start the loop which will handle and dispatch each packet to the handler
# function for processing
os1.run_forever(handler)
