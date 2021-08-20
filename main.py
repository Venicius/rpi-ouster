from os1 import OS1
from os1.utils import raw_values, build_trig_table
import os
from datetime import datetime
import json
from multiprocessing import Process, Queue

#definicao de ips
OS1_IP = '10.5.5.86'
HOST_IP = '10.5.5.1'
unprocessed_packets = Queue()


def handler(packet):
    unprocessed_packets.put(packet)

#funcao que faz a captura dos pacotes, insere na fila de escrita e chama a funcao print_lines
def worker(queue, beam_altitude_angles, beam_azimuth_angles):
    build_trig_table(beam_altitude_angles, beam_azimuth_angles)
    while True:
        packet = queue.get()
        ch, ch_range, reflectivity, intensity, timeStamp, encoderCount, measurementID, frameID, x, y, z, noise = raw_values(
            packet)
        print_lines(ch, ch_range, reflectivity, intensity, timeStamp,
                    encoderCount, measurementID, frameID, x, y, z, noise)

#funcao auxiliar para ajudar no buffer
def spawn_workers(n, worker, *args, **kwargs):
    processes = []
    for i in range(n):
        process = Process(target=worker, args=args, kwargs=kwargs)
        process.start()
        processes.append(process)
    return processes

#funcao para imprimir linhas no arquivo, ela eh chamada na funcao worker
def print_lines(ch, ch_range, reflectivity, intensity, timeStamp, encoderCount,
                measurementID, frameID, x, y, z, noise):
    filename = 'Raw_' + str(get_date_time()) + '.txt'
    print("Generating output in " + filename)
    with open(filename, 'a') as f:
        f.write("TimeStamp: " + str(timeStamp[0]) + " measurementID: " +
                str(measurementID[0]) + " frameID: " + str(frameID[0]) + "\n")
        for vetor_dados_coletados in zip(ch, ch_range, encoderCount,
                                         reflectivity, intensity, x, y, z,
                                         noise):
            linha_impressa_no_arquivo = str(vetor_dados_coletados)
            linha_impressa_no_arquivo = linha_impressa_no_arquivo.replace(
                ',', ' ')
            linha_impressa_no_arquivo = linha_impressa_no_arquivo.replace(
                '(', ' ')
            linha_impressa_no_arquivo = linha_impressa_no_arquivo.replace(
                ')', ' ')
            f.write(linha_impressa_no_arquivo + "\n")

#funcao para pegar data e hora para o nome do arquivo
def get_date_time():
    now = datetime.now()
    date_time = now.strftime("%m%d%Y_%H%M")
    print("Running at", date_time)
    return date_time

#Função que inicia a captura dos dados do sensor
def start_ouster():
    os1 = OS1(OS1_IP, HOST_IP) #Configurando o ip da maquina que está rodando o programa e o ip do Ouster
    beam_intrinsics = json.loads(os1.get_beam_intrinsics()) #carregando configurações do sensor
    beam_alt_angles = beam_intrinsics['beam_altitude_angles']
    beam_az_angles = beam_intrinsics['beam_azimuth_angles']
    #a partir daqui é feito um esquema de buffer para nao sobrecarregar o arduino com a escrita e tentar perder menos dados
    workers = spawn_workers(4, worker, unprocessed_packets, beam_alt_angles,
                            beam_az_angles)
    #iniciada a leitura de fato
    os1.start()
    try:
        os1.run_forever(handler)
    except KeyboardInterrupt:
        for w in workers:
            w.terminate()
    finally:
        print("Programa finalizado!")

##Iniciando programa, fica rodando até o usuario cancelar com ctrl+C
while True:
    hostname = "10.5.5.86" ##IP do ouster
    response = os.system("ping -c 1 " + hostname) # testando a conexão com o sensor ouster
    if response == 0:
        start_ouster() # Se estiver conectado, ele inicia a captura
        print("running")
        break
