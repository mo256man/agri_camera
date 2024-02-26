import numpy as np
import cv2
import rtsp
from PIL import Image, ImageTk
from onvifreq import OnvifRequest
import urllib.request
import base64

class Camera():
    def __init__(self):
        user = "mo256man"
        password = "momo1024"
        ipaddr = "192.168.0.8"
        port = "554"
        stream = "stream2"          # 高画質：stream1、低画質:stream2
        onvif_port = "2020"
        self.width = 640
        self.height = 360
        self.dx = 0.02
        self.dy = 0.02
        self.rtsp_url = f"rtsp://{user}:{password}@{ipaddr}:{port}/{stream}"

        self.is_mirror = True

        self.onvif_request = OnvifRequest(username=user, password=password)
        self.url = f"http://{ipaddr}:{onvif_port}/"
        self.headers = {"Content-Type": "text/xml; charset=utf-8"}
        self.is_streaming = True

    def connect(self):
        self.client = rtsp.Client(rtsp_server_uri=self.rtsp_url, verbose=True)
        ret = False
        while not ret:
            ret, _ = self.read()
        self.absolute_move(0,0)

    def read(self):
        frame = self.client.read()                              # PIL画像として取得される　色の並びはRGB
        if frame is not None:
            ret = True
            imgCV = np.array(frame, dtype=np.uint8)             # OpenCVにする
            imgCV = cv2.cvtColor(imgCV, cv2.COLOR_RGB2BGR)      # 色の並びをBGRにする
            if self.is_mirror:
                imgCV = np.flip(imgCV, 1)
            imgB64 = img2base64(imgCV)
        else:
            ret = False
            imgB64 = None
        return ret, imgB64

    def relative_move(self, x, y):
        if self.is_mirror:
            x, y = -x, -y
        oreq = self.onvif_request.relative_move(x, y)
        self.call_onvif(oreq)

    def absolute_move(self, x, y):
        oreq = self.onvif_request.absolute_move(x, y)
        self.call_onvif(oreq)

    def call_onvif(self, oreq):
        req = urllib.request.Request(self.url, data=oreq.encode(), method="POST", headers=self.headers)
        try:
            with urllib.request.urlopen(req) as response:
                pass
        except urllib.error.URLError as e:
            print(e)

def img2base64(image):
    _, imgEnc = cv2.imencode(".jpg", image)                     # メモリ上にエンコード
    imgB64 = base64.b64encode(imgEnc)                           # base64にエンコード
    strB64 = "data:image/jpg;base64," + str(imgB64, "utf-8")    # 文字列化
    return strB64


def main():
    camera = Camera()
    camera.connect()
    dx, dy = 0, 0
    while True:
        ret, frame = camera.read()
        if ret:
            cv2.imshow("camera", frame)
            key = cv2.waitKey(1)
            input = False
            if key == 27:
                camera.absolute_move(0,0)
                break
            elif key == ord("w"):
                dx, dy = 0, -.1
                input = True
            elif key == ord("s"):
                dx, dy = 0, .1
                input = True
            elif key == ord("a"):
                dx, dy = .1, 0
                input = True
            elif key == ord("d"):
                dx, dy = -.1, 0
                input = True
            elif key == ord("0"):
                camera.absolute_move(0,0)
            elif key == ord("m"):
                camera.is_mirror = not camera.is_mirror
            if input:
                camera.relative_move(dx, dy)

        else:
            print("camera not connected")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
