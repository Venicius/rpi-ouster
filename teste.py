import csv
from datetime import datetime

def handler():
    filename = 'Raw_' + str(getDateTime()) + '.txt'
    with open(filename, 'a') as f:
        writer = csv.writer(f, delimiter=' ')
        print("Running")
        writer.writerow("*------------------------------------------------------*")
        for x in range(0, 128):
            writer.writerow(str(x))


def getDateTime():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    print("timestamp =", now)
    return now


handler()



