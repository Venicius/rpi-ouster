from datetime import datetime


def handler():
    filename = 'Raw_' + str(getDateTime()) + '.txt'
    with open("teste.txt", 'a') as f:
        numbers = [1, 2, 3]
        letters = ['a', 'b', 'c']
        f.write("*------------------------------------------------------* \n")
        f.write(
            "timeStamp 545940314780 measurementID 0 frameID 5266 azimuthDataBlockStatus 1\n")
        for x in range(3):
            f.write(str(letters[x])+"\n")


def getDateTime():
    now = datetime.now()
    date_time = now.strftime("%m%d%Y_%H%M%S")
    print("Running at", date_time)
    return date_time

while True:
    handler()
