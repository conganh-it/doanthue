import cv2
import numpy as np
from pyzbar.pyzbar import decode
import serial
from fxplc_lib import FXPLC
#img = cv2.imread('1.png')
cap = cv2.VideoCapture(0)
# serial.Serial('COM 3',9600)
f = FXPLC('COM9')
while True:
    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(myData)
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        pts2 = barcode.rect
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 255), 2)
        if myData == "K205520114130":
            f.write_bit("M100", True)
            f.write_bit('M101', False)
        if myData == "K205520114093":
            f.write_bit("M100", False)
            f.write_bit("M101", True)
    cv2.imshow('Result', img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
