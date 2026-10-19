#!/usr/bin/env python3
"""Send simulated vessel data to OpenCPN on localhost. Stop with Ctrl+C."""

import argparse
import datetime
import math
import socket
import time


def sentence(body):
    checksum = 0
    for byte in body.encode("ascii"):
        checksum ^= byte
    return f"${body}*{checksum:02X}\r\n".encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=int, default=600, help="Duration in seconds")
    args = parser.parse_args()
    latitude, longitude = 36.0, 25.0
    legs = [(12.0, 90.0), (8.0, 0.0), (6.0, 270.0), (10.0, 180.0)]
    print("SIMULASYON: UDP 127.0.0.1:10119; durdurmak icin Ctrl+C", flush=True)
    start = previous = time.monotonic()
    previous_speed, previous_course = legs[0]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while time.monotonic() - start < args.duration:
            current = time.monotonic()
            elapsed = current - previous
            distance = previous_speed * elapsed / 3600
            angle = math.radians(previous_course)
            longitude += distance * math.sin(angle) / (60 * math.cos(math.radians(latitude)))
            latitude += distance * math.cos(angle) / 60
            previous = current
            speed, course = legs[int((current - start) // 60) % len(legs)]
            now = datetime.datetime.now(datetime.timezone.utc)
            lat = f"{int(latitude):02d}{(latitude % 1) * 60:07.4f}"
            lon = f"{int(longitude):03d}{(longitude % 1) * 60:07.4f}"
            bodies = [
                f"GPRMC,{now:%H%M%S}.00,A,{lat},N,{lon},E,{speed:.1f},{course:.1f},{now:%d%m%y},0.0,E,A",
                f"GPGGA,{now:%H%M%S}.00,{lat},N,{lon},E,1,08,0.9,0.0,M,0.0,M,,",
                f"GPHDT,{course:.1f},T",
            ]
            for body in bodies:
                sock.sendto(sentence(body), ("127.0.0.1", 10119))
            print(f"SIM {latitude:.6f}, {longitude:.6f} | {speed:.1f} kn | {course:.0f} deg", flush=True)
            previous_speed, previous_course = speed, course
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSimulasyon durduruldu.")
