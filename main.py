from os1 import OS1
from os1.utils import raw_values, build_trig_table
import os
from datetime import datetime
import json
from multiprocessing import Process, Queue

OS1_IP = '10.5.5.86'
HOST_IP = '10.5.5.1'
unprocessed_packets = Queue()


def handler(packet):
    unprocessed_packets.put(packet)


def worker(queue, beam_altitude_angles, beam_azimuth_angles):
    build_trig_table(beam_altitude_angles, beam_azimuth_angles)
    while True:
        packet = queue.get()
        ch, ch_range, reflectivity, intensity, timeStamp, encoderCount, measurementID, frameID, x, y, z, noise = raw_values(
            packet)
        print_lines(ch, ch_range, reflectivity, intensity, timeStamp, encoderCount, measurementID, frameID, x, y, z,
                    noise)


def spawn_workers(n, worker, *args, **kwargs):
    processes = []
    for i in range(n):
        process = Process(
            target=worker,
            args=args,
            kwargs=kwargs
        )
        process.start()
        processes.append(process)
    return processes


def print_lines(ch, ch_range, reflectivity, intensity, timeStamp, encoderCount, measurementID, frameID, x, y, z, noise):
    filename = 'Raw_' + str(getdatetime()) + '.txt'
    print("Generating output in " + filename)
    with open(filename, 'a') as f:
        f.write("TimeStamp: " + str(timeStamp[0]) + " measurementID: " + str(measurementID[0]) + " frameID: " + str(
            frameID[0]) + "\n")
        for vetorDadosColetados in zip(ch, ch_range, encoderCount, reflectivity, intensity, x, y, z, noise):
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
    os1 = OS1(OS1_IP, HOST_IP)
    beam_intrinsics = json.loads(os1.get_beam_intrinsics())
    beam_alt_angles = beam_intrinsics['beam_altitude_angles']
    beam_az_angles = beam_intrinsics['beam_azimuth_angles']
    workers = spawn_workers(4, worker, unprocessed_packets, beam_alt_angles, beam_az_angles)
    os1.start()
    try:
        os1.run_forever(handler)
    except KeyboardInterrupt:
        for w in workers:
            w.terminate()
    finally:
        print("Programa finalizado!")


while True:
    hostname = "10.5.5.86"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        startouster()
        print("running")
        break
