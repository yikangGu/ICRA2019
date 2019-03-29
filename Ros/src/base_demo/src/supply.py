import time
import cv2

def supply():
    request = input("supply request send ")
    if request:
        print "supplying!"
        time.sleep(2)
        print "supply done"

    cv2.waitKey(0)

if __name__ == "__main__":
    supply()
