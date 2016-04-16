from ctypes import cdll, util


class RobotArm(object):
    servos = {
        'rotate': ['LED0_OFF_L', 'LED0_OFF_H'],
        'arm_fw_bw': ['LED1_OFF_L', 'LED1_OFF_H'],
        'arm_up_down': ['LED2_OFF_L', 'LED2_OFF_H'],
        'claw_open_close': ['LED3_OFF_L', 'LED3_OFF_H']
    }

    registers = {
        'LED0_OFF_L': 0x08,
        'LED0_OFF_H': 0x09,
        'LED1_OFF_L': 0x0C,
        'LED1_OFF_H': 0x0D,
        'LED2_OFF_L': 0x10,
        'LED2_OFF_H': 0x11,
        'LED3_OFF_L': 0x14,
        'LED3_OFF_H': 0x15,
    }

    def __init__(self):
        handle = self.setup()
        self.fd = handle.wiringPiI2CSetup(0x40)
        self.write = handle.wiringPiI2CWriteReg8
        self.write(self.fd, 0x00, 0x00)
        self.write(self.fd, 0x06, 0x00)
        self.write(self.fd, 0x07, 0x00)

    @staticmethod
    def setup():
        lib_name = util.find_library("wiringPi")
        return cdll.LoadLibrary(lib_name)

    def move(self, servo_name, value):
        mask_l = 255
        mask_h = 3840
        low_bits = value & mask_l
        high_bits = (value & mask_h) >> 8

        servo_registers = self.servos[servo_name]

        self.write(self.fd, self.registers[servo_registers[0]], low_bits)
        self.write(self.fd, self.registers[servo_registers[1]], high_bits)


if __name__ == '__main__':
    robot_arm = RobotArm()

    # robot_arm.move(fd, 0x06, 0x0)
    # robot_arm.move(fd, 0x07, 0x0)
    # robot_arm.move(fd, 0x08, 0x0)
    # robot_arm.move(fd, 0x0E, 0x0)
    # robot_arm.move(fd, 0x0F, 0x0)
    # while True:
    #     for i in range(2, 8):
    #         robot_arm.move(fd, 0x09, i)
    #         for j in range(0, 256):
    #             robot_arm.move(fd, 0x08, j)
    #             robot_arm.move(fd, 0x11, i)
    #             robot_arm.move(fd, 0x10, j)
    #             sleep(0.05)
    #     for i in range(9, 2, -1):
    #         robot_arm.move(fd, 0x09, i)
    #         robot_arm.move(fd, 0x11, i)
    #         sleep(0.2)
