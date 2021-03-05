import math
import struct

PACKET_SIZE = 48

_unpack = struct.Struct(PACKET).unpack


def unpack(raw_packet):
    s = struct.Struct('I I I f f f f f f')
    unpacked_data = s.unpack(raw_packet)
    return unpacked_data