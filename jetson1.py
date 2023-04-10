import jetson.utils
import jetson.inference
import cv2
import time
import os 


#### REMARQUES
# if suddenly unable to access camera, it means another session using this same camera (hung or alive) 
# reset the nvargus-daemon to reset the argus framework and try nvgstcapture-1.0 again.
# 
# jetson_inference has to be built with cmake -DENABLE_NVMM=off ../

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

camera = jetson.utils.videoSource("csi://0") 
#camera = jetson.utils.videoSource("footage.mp4")


def execute(vehicle=None):
    while True:
        start = time.time()
        person = []
        img = camera.Capture()
        detections = net.Detect(img)
        end = time.time()
        duration = (end - start)*1000
        for detection in detections:
            if detection.ClassID == 1:
                print("FOUND YOU")
                if vehicle is not None:
                     print('Current GPS location: {0}, {1}'.format(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon))
                person.append(detection)
                #img.save()
        print("the amount of people detected in this frame: {} in {}ms".format(len(person), duration))
        print("FPS = {}".format(1000/duration))
        print("DONE")
        os.system("clear")
# jetson_inference has to be built with cmake -DENABLE_NVMM=off ../
if __name__ == "__main__":
    execute()
