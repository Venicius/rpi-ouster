import csv
from datetime import datetime

def handler(datetime):
    with open('Raw_' + str(datetime) +'.txt', 'a') as f:
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


handler(getDateTime())



