import jetson.utils
import jetson.inference
import cv2
import time



#### REMARQUES
# if suddenly unable to access camera, it means another session using this same camera (hung or alive) 
# reset the nvargus-daemon to reset the argus framework and try nvgstcapture-1.0 again.
# 

# jetson_inference has to be built with cmake -DENABLE_NVMM=off ../
if __name__ == "__main__":
    net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
    display = jetson.utils.glDisplay()
    #camera = jetson.utils.videoSource("csi://0") 
    camera = jetson.utils.videoSource("footage.mp4")

    while True:
        start = time.time()
        print("hello")
        person = []
        img = camera.Capture()
        detections = net.Detect(img)
        end = time.time()
        duration = (end - start)*1000
        for detection in detections:
            if detection.ClassID == 1:
                print("WE HAVE DETECTED A HUMAN")
                person.append(detection)
        print("the amount of people detected in this frame: {} in {}ms".format(len(person), duration))
        print("FPS = {}".format(1000/duration))


        print("DONE \n\n\n\n\n\n")
