import jetson.utils
import jetson.inference
import cv2
import time
import os 
import numpy as np
import threading
import imagezmq
import socket
#### REMARQUES
# if suddenly unable to access camera, it means another session using this same camera (hung or alive) 
# reset the nvargus-daemon to reset the argus framework and try nvgstcapture-1.0 again.
# sudo systemctl restart nvargus-daemon
# jetson_inference has to be built with cmake -DENABLE_NVMM=off ../

# Load neural network 
net = jetson.inference.detectNet("ssd-mobilenet-v2", argv=["--log-level=error", f"--threshold=0.5"])

# Initialize ImageZMQ sender
ip = "tcp://192.168.134.22:5555"
sender = imagezmq.ImageSender(ip)
rpi_name = socket.gethostname()

# Connect to CSI camera 
camera = jetson.utils.videoSource("csi://0") 
#camera = jetson.utils.videoSource("footage.mp4")

def saveImage(img):
    #jetson.utils.saveImageRGBA("./img/test.png", img)
    numpyImage = jetson.utils.cudaToNumpy(img)
    #np.save("./npy/img", numpyImage)
    
    sender.send_image(rpi_name, numpyImage)
    return

def execute(vehicle=None):
    person_index = 0
    while True:
        start = time.time()
        
       # Capture camera frame
        img = camera.Capture()

        # Apply prediction function
        detections = net.Detect(img)
        
        end = time.time()

        # Inference Time
        duration = (end - start)*1000
        
        # Parse inference results
        person = []
        for detection in detections:
            if detection.ClassID == 1: # ClassID 1 refers to humans
                print("Found a person.")
                person.append(detection)

                # if script is used in vtol.py, prints GPS coords when detecting a person
                if vehicle is not None:
                     print('Current GPS location: {0}, {1}'.format(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon))
                if threading.active_count() <= 2:
                    my_thread = threading.Thread(target = saveImage, args=(img,))
                    my_thread.start()
        

        print("the amount of people detected in this frame: {} in {}ms".format(len(person), duration))
        print("FPS = {}".format(1000/duration))
        print("DONE")
        #os.system("clear")

# jetson_inference has to be built with cmake -DENABLE_NVMM=off ../
if __name__ == "__main__":
    execute()
