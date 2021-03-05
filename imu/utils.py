import math
import struct
import sys

from imu.packet import (unpack)


class UninitializedTrigTable(Exception):
    def __init__(self):
        msg = (
            "You must build_trig_table prior to calling xyz_point or"
            "xyz_points.\n\n"
            "This is likely because you are in a multiprocessing environment.")
        super(UninitializedTrigTable, self).__init__(msg)


def data_imu(packet, os16=False):
    packet = unpack(packet)
    return packet
