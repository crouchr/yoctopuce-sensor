#!/usr/bin/env python3
# This is a version of the code refactored into a function that can be called
# There are lots of low-level kernel calls here - maybe they don't work in Docker
# If so then make this a native application that presents as a Flask service

import usb.core
import usb.util
# import sys

VERSION = "1.5"
# [volker-dev app]# lsusb
# Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
# Bus 001 Device 004: ID 04ca:7066 Lite-On Technology Corp. Integrated Camera
# Bus 001 Device 003: ID 8087:0a2b Intel Corp. Bluetooth wireless interface
# Bus 001 Device 014: ID 24e0:0050 Yoctopuce Sarl Yocto-Light-V3
# Bus 001 Device 013: ID 24e0:0084 Yoctopuce Sarl Yocto-Meteo-V2
# Bus 001 Device 012: ID 1a86:e025 QinHeng Electronics TEMPerHUM
# Bus 001 Device 011: ID 1a40:0201 Terminus Technology Inc. FE 2.1 7-port Hub
# Bus 001 Device 002: ID 3938:1031 MOSART Semi. 2.4G Wireless Mouse
# Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub




# Look for ids using dmesg
# New USB device found, idVendor=1a86, idProduct=e025, bcdDevice= 1.00
# Temperhum_Vendor = 0x1a86
# Temperhum_Product = 0xe025
#
# Temperhum_Interface = 1
# Temperhum_ID = hex(Temperhum_Vendor) + ':' + hex(Temperhum_Product)
# Temperhum_ID = Temperhum_ID.replace( '0x', '')

# Function to return a string of hex character representing a byte array


def byte_array_to_hex_string( byte_array ):
    array_size = len(byte_array)
    if array_size == 0:
        s = ""
    else:
        s = ""
        for var in list(range(array_size)):
            b = hex(byte_array[var])
            b = b.replace( "0x", "")
            if len(b) == 1:
                b = "0" + b
            b = "0x" + b
            s = s + b + " "
    return (s.strip())

# The temperature is a 16 bit signed integer, this function converts it to signed decimal

def twos_complement(value,bits):
#    value = int(hexstr,16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

# Check the parameters passed

#params = [x.lower() for x in sys.argv]

# if "--help" in params:
#     print ("")
#     print ("Usage: temperhum.py [OPTION]")
#     print ("Reads the temperature and humidity from a PCSensor, TEMPerHum, USB sensor, USB ID", Temperhum_ID)
#     print ("")
#     print ("--help          shows this :-)")
#     print ("--version       displays version information and exits")
#     print ("--f             output temperature in Fahrenheit, default is Celsius")
#     print ("--nosymbols     do not show C, F or %")
#     print ("--raw           include the raw data from the sensor in the output, as hex bytes")
#     print ("--debug         turn on debugging output")
#     print ("--reattach      if the usb device is attached to a kernel driver, default is to detach it, and leave it that way")
#     print ("                this option forces a reattach to the kernel driver on exit")
#     print ("")
#     exit(0)

# if "--version" in params:
#     print ("")
#     print ("temperhum.py  version", VERSION)
#     print ("Copyright (C) 2019 Colin J Mair")
#     print ("License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>")
#     print ("This is free software: you are free to change and redistribute it")
#     print ("There is NO WARRANTY, to the extent permitted by law")
#     print ("")
#     exit(0)

# if "--debug" in params:
#     DEBUG = True
# else:
#     DEBUG = False
#
# if "--f" in params:
#     CELSIUS = False
# else:
#     CELSIUS = True
#
# if "--nosymbols" in params:
#     NOSYMBOLS = True
# else:
#     NOSYMBOLS = False
#
# if "--reattach" in params:
#     REATTACH = True
# else:
#     REATTACH = False
#
# if "--raw" in params:
#     RAW = True
# else:
#     RAW = False


# If debug is true tell the user

# if DEBUG == True:
#     print ("--debug =", DEBUG, "  --f =", not CELSIUS, "  --nosymbols =", NOSYMBOLS, "  --reattach =", REATTACH)

# Try to find the Temperhum usb device

def read_from_sensor(vendor, product, DEBUG):
    # DEBUG = False
    CELSIUS = True
    REATTACH = False
    NOSYBMOLS = False
    RAW = True

    Temperhum_Interface = 1
    # Temperhum_ID = hex(vendor).__str__() + ':' + hex(product).__str__()
    # Temperhum_ID = Temperhum_ID.replace('0x', '')

    try:
        device = usb.core.find(idVendor=vendor, idProduct=product)

    # If it was not found report the error and exit
        if device is None:
            # print(f"Error: Device {Temperhum_ID} not found")
            print("error: Temperhum device not found")
            return -99.9, -99.9
        # else:
        #     if DEBUG == True:
        #         print ("Found Device ID", Temperhum_ID)
        #         print ("-" * 20, "Device Information", "-" * 20)
        #         print (device)
        #         print ("-" * 20, "Device Information", "-" * 20)

        # check if it has a kernel driver, if so set a reattach flag and detach it
        reattach = False
        if device.is_kernel_driver_active(1):
            reattach = True
            if DEBUG == True:
                print("Warning: kernel driver attached to Temperhum device, will try to detach it", end='')
                if REATTACH:
                    print(" and reattach at the end")
                else:
                    print(" and leave it detached")

            result = device.detach_kernel_driver(1)

            if result != None:
                print("Error: unable to detach kernel driver from Temperhum device")
                return -99.9, -99.9
            else:
                if DEBUG == True:
                    print("Kernel driver detached ok for Temperhum device")

        # Extract the correct interface information from the device information
        cfg = device[0]
        inf = cfg[Temperhum_Interface, 0]

        if DEBUG == True:
            print(f"Claiming the Temperhum device interface {Temperhum_Interface} for use")

        result = usb.util.claim_interface(device, Temperhum_Interface)
        if result != None:
            print("Error: unable to claim the Temperhum interface")
            return -99.9, -99.9
        else:
            if DEBUG == True:
                print("Claimed Temperhum interface ok")

        # Extract the read and write endpoint information
        ep_read = inf[0]
        ep_write = inf[1]
        if DEBUG == True:
            print("-" * 20, "Read Endpoint Information", "-" * 20)
            print(ep_read)
            print("-" * 20, "Read Endpoint Information", "-" * 20)
            print("-" * 20, "Write Endpoint Information", "-" * 20)
            print(ep_write)
            print("-" * 20, "Write Endpoint Information", "-" * 20)

        # Extract the addresses to read from and write to
        ep_read_addr = ep_read.bEndpointAddress
        ep_write_addr = ep_write.bEndpointAddress

        if DEBUG == True:
            print("Read endpoint address =", hex(ep_read_addr))
            print("Write endpoint address =", hex(ep_write_addr))
            print("Sending request for temperature/humidity data to Temperhum device")

        try:
            msg = b'\x01\x80\x33\x01\0\0\0\0'
            sendit = device.write(ep_write_addr, msg)
        except:
            print("Error: sending request to Temperhum device")
            return -99.9, -99.9

        if DEBUG == True:
            print("Sending request went ok")
            print("Reading data from Temperhum device")

        try:
            data = device.read(ep_read_addr, 0x8)
        except:
            print("Error: reading data from Temperhum device")
            return -99.9, -99.9
        else:
            if DEBUG == True:
                print("Data returned from Temperhum device =", data)

        # Decode the temperature and humidity
        if CELSIUS == True:
            temperature = round((twos_complement((data[2] * 256) + data[3], 16)) / 100, 1)
        else:
            temperature = round((twos_complement((data[2] * 256) + data[3], 16)) / 100 * 9/5 + 32, 1)

        humidity = int(((data[4] * 256) + data[5]) / 100)

        return temperature, humidity

    # Add symbols unless turned off by --nosymbols parameter
    #     if NOSYMBOLS == False:
        if CELSIUS == True:
            temperature = str(temperature) + "C"
        else:
            temperature = str(temperature) + "F"

        humidity = str(humidity) + "%"

        #print(f'temp={temperature} humidy={humidity}')

    # Output the temperature and humidity
    #     if DEBUG == True:
    #         print ("")
    #         if RAW == True:
    #             dashes = 50
    #         else:
    #             dashes = 12
    #         print ("-" * dashes)
    #         print (temperature, humidity, end="")
    #
    #         if RAW == True:
    #             print ("", byte_array_to_hex_string(data))
    #         else:
    #             print ("")
    #
    #         print ("-" * dashes)
    #         print ("")
    #     else:
    #         print (temperature, humidity, end="")

            # if RAW == True:
            #     print ("", byte_array_to_hex_string(data))
            # else:
            #     print ("")

        # Release the usb resources
        if DEBUG == True:
            print("Releasing USB resources for Temperhum device")

        result = usb.util.dispose_resources(device)

        if result != None:
            print("Error: releasing USB resources for Temperhum device")
        else:
            if DEBUG == True:
                print("Resources released ok for Temperhum device")

        # Reattach device to the kernel driver if requested by parameter
        if REATTACH:
            if DEBUG == True:
                print("Reattaching the kernel driver to Temperhum device")
            result = device.attach_kernel_driver(1)
            if result != None:
                print("Error: reattaching the kernel driver to Temperhum device")
                return -99.9, -99.9

    except Exception as e:
        print(f'read_from_sensor() : exception : {e}')
        return -99.9, -99.9


# test harness
if __name__ == '__main__':
    import time
    # Read from looking in dmesg output
    # Bus 001 Device 012: ID 1a86:e025 QinHeng Electronics TEMPerHUM

    vendor = 0x1a86
    product = 0xe025
    print("Temperhum device vendor=0x{0:02x}".format(vendor))
    print("Temperhum device product=0x{0:02x}".format(product))
    # print(f'Temperhum device vendor={vendor}, product={product}')

    while True:
        print('-----------------')
        temperature, humidity = read_from_sensor(vendor, product, DEBUG=True)
        print(f'temperature={temperature}, humidity={humidity}')
        time.sleep(10)
