from ctypes import cdll, util
import logging


class RobotArm(object):
    def __init__(self, app):
        handle = self.setup()
        app.logger.info("setting up")
        self.fd = handle.wiringPiI2CSetup(0x40)
        self.write = handle.wiringPiI2CWriteReg8
        self.app = app

    @staticmethod
    def setup():
        lib_name = util.find_library("wiringPi")
        return cdll.LoadLibrary(lib_name)

    def move(self, servo, value):
        mask_l = 255
        mask_h = 4095-255
        low_bits = value ^ mask_l
        high_bits = value ^ mask_h
        self.app.logger.info(high_bits, low_bits, bin(high_bits + low_bits))

        self.write(self.fd, 0x06, low_bits)
        self.write(self.fd, 0x07, high_bits)
        self.app.logger.info("written")

# fd = setup()
#
# write(fd, 0x00, 0x00)
# write(fd, 0xFE, 0x40)
# write(fd, 0x06, 0x0)
# write(fd, 0x07, 0x0)
# write(fd, 0x08, 0x0)
# write(fd, 0x0E, 0x0)
# write(fd, 0x0F, 0x0)
# while True:
#     for i in range(2, 8):
#         write(fd, 0x09, i)
#         for j in range(0, 256):
#             write(fd, 0x08, j)
#             write(fd, 0x11, i)
#             write(fd, 0x10, j)
#             sleep(0.05)
#     for i in range(9, 2, -1):
#         write(fd, 0x09, i)
#         write(fd, 0x11, i)
#         sleep(0.2)
