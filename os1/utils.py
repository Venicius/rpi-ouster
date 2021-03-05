import math
import struct
import sys

from os1.packet import (AZIMUTH_BLOCK_COUNT, CHANNEL_BLOCK_COUNT,
                        azimuth_angle, azimuth_block, azimuth_measurement_id,
                        azimuth_timestamp, azimuth_valid, channel_block,
                        channel_range, unpack, azimuth_encoder_count,
                        azimuth_frame_id, channel_reflectivity,
                        channel_signal_photons, channel_noise_photons)

# The OS-16 will still contain 64 channels in the packet, but only
# every 4th channel starting at the 2nd will contain data .
OS_16_CHANNELS = (2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62)
OS_128_CHANNELS = tuple(i for i in range(CHANNEL_BLOCK_COUNT))


class UninitializedTrigTable(Exception):
    def __init__(self):
        msg = (
            "You must build_trig_table prior to calling xyz_point or"
            "xyz_points.\n\n"
            "This is likely because you are in a multiprocessing environment.")
        super(UninitializedTrigTable, self).__init__(msg)


_trig_table = []


def build_trig_table(beam_altitude_angles, beam_azimuth_angles):
    if not _trig_table:
        for i in range(CHANNEL_BLOCK_COUNT):
            _trig_table.append([
                math.sin(beam_altitude_angles[i] * math.radians(1)),
                math.cos(beam_altitude_angles[i] * math.radians(1)),
                beam_azimuth_angles[i] * math.radians(1),
            ])


def xyz_point(channel_n, azimuth_block):
    if not _trig_table:
        raise UninitializedTrigTable()

    channel = channel_block(channel_n, azimuth_block)
    table_entry = _trig_table[channel_n]
    range = channel_range(channel) / 1000  # to meters
    adjusted_angle = table_entry[2] + azimuth_angle(azimuth_block)
    x = -range * table_entry[1] * math.cos(adjusted_angle)
    y = range * table_entry[1] * math.sin(adjusted_angle)
    z = range * table_entry[0]

    return [x, y, z]


def raw_values(packet, os16=False):

    channels = OS_16_CHANNELS if os16 else OS_128_CHANNELS
    if not isinstance(packet, tuple):
        packet = unpack(packet)

    ch = []
    timeStamp = []
    encoderCount = []
    measurementID = []
    frameID = []
    x = []
    y = []
    z = []
    ch_range = []
    reflectivity = []
    intensity = []
    noise = []

    for b in range(AZIMUTH_BLOCK_COUNT):
        block = azimuth_block(b, packet)

        if not azimuth_valid(block):
            continue

        for c in channels:
            channel = channel_block(c, block)
            ch.append(c)
            ch_range.append(channel_range(channel))
            timeStamp.append(azimuth_timestamp(block))
            encoderCount.append(azimuth_encoder_count(block))
            measurementID.append(azimuth_measurement_id(block))
            frameID.append(azimuth_frame_id(block))
            point = xyz_point(c, block)
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
            reflectivity.append(channel_reflectivity(channel))
            intensity.append(channel_signal_photons(channel))
            noise.append(channel_noise_photons(channel))

    return ch, ch_range, reflectivity, intensity, timeStamp, encoderCount, measurementID, frameID, x, y, z, noise


_unpack = struct.Struct("<I").unpack


def peek_encoder_count(packet):
    return _unpack(packet[12:16])[0]


def frame_handler(queue):
    buffer = []
    rotation_num = 0
    sentinel = None
    last = None

    def handler(packet):
        nonlocal rotation_num, sentinel, last, buffer

        encoder_count = peek_encoder_count(packet)
        if sentinel is None:
            sentinel = encoder_count

        if buffer and last and encoder_count >= sentinel and last <= sentinel:
            rotation_num += 1
            queue.put({"buffer": buffer, "rotation": rotation_num})
            buffer = []

        buffer.append(packet)
        last = encoder_count

    return handler
