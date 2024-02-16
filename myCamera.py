import cv2
import numpy as np
import datetime

class Camera():
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		self.title = "camera"
		self.imgW = 640
		self.imgH = 480
		self.is_mirror = True
		self.show_clock = True
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.imgW)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.imgH)

	def read(self):
		ret, frame = self.cap.read()
		if ret:
			if self.is_mirror:
				frame = cv2.flip(frame, 1)
			if self.show_clock:
				dt = datetime.datetime.now()
				strdt = dt.strftime("%Y-%m-%d %H:%M:%S")
				frame = cv2.putText(frame, strdt, (20,40), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1)
		return ret, frame
	
	def close(self):
		self.cap.release()
		cv2.destroyAllWindows()


def main():
	camera = Camera()
	while True:
		ret, frame = camera.read()
		if ret:
			cv2.imshow(camera.title, frame)
			key = cv2.waitKey(1)
			if key == 27:
				break

	camera.close()

if __name__ == "__main__":
	main()
