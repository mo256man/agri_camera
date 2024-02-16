import serial
import time
import sys

class Omron():
	def __init__(self):
		try:
			self.ser = serial.Serial("/dev/ttyUSB_OMRON", 115200, serial.EIGHTBITS, serial.PARITY_NONE)
			self.light(True)
			ret = self.ser.read(self.ser.inWaiting())
			time.sleep(2)
			self.is_available = True
		except Exception as e:
			self.light(False)
			self.is_available = False
			print(e)
	
	def light(self, bool):
		if bool:
			command = bytearray([0x52, 0x42, 0x0a, 0x00, 0x02, 0x11, 0x51, 1, 0x00, 0, 255, 0])
		else:
			command = bytearray([0x52, 0x42, 0x0a, 0x00, 0x02, 0x11, 0x51, 0, 0x00, 0, 0, 0])
		command = command + calc_crc(command, len(command))
		self.ser.write(command)
		time.sleep(0.1)

	def read(self):
		if self.is_available:
			try:
				command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x21, 0x50])
				command = command + calc_crc(command, len(command))
				self.ser.write(command)
				time.sleep(0.1)
				data = self.ser.read(self.ser.inWaiting())		
				temp_hex = hex(data[9]) + format(data[8], '02x')
				temp = s16(int(temp_hex, 16))/100
				humi_hex = hex(data[11]) + format(data[10], "02x")
				humi = int(humi_hex, 16)/100
				ret = "OK"
			except Exception as ret:
				self.is_available = False
				self.light(False)
				print(ret)
				temp = 0
				humi = 0
			finally:
				return ret, temp, humi
		else:
			ret = "not found"
			temp = 0
			humi = 0
			return ret, temp, humi


def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)

def calc_crc(buf, length):
    """
    CRC-16 calculation.

    """
    crc = 0xFFFF
    for i in range(length):
        crc = crc ^ buf[i]
        for i in range(8):
            carrayFlag = crc & 1
            crc = crc >> 1
            if (carrayFlag == 1):
                crc = crc ^ 0xA001
    crcH = crc >> 8
    crcL = crc & 0x00FF
    return (bytearray([crcL, crcH]))

def main():
	omron = Omron()
	while True:
		ret, temp, humi = omron.read()
		if ret == "OK":
			print(f"temperature: {temp}")
			print(f"humi: {humi}")
		else:
			print(ret)

	print("done.")


if __name__ == "__main__":
	main()
