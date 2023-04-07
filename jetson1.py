import jetson.utils
import jetson.inference
import cv2


#### REMARQUES
# if suddenly unable to access camera, it means another session using this same camera (hung or alive) 
# reset the nvargus-daemon to reset the argus framework and try nvgstcapture-1.0 again.
# sudo service nvargus-daemon restart
# jetson_inference has to be built with cmake -DENABLE_NVMM=off ../

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

camera= jetson.utils.videoSource("csi://0")


""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""



display = jetson.utils.videoOutput("video.mp4") 

camera = jetson.utils.videoSource("csi://0") 

while display.IsStreaming():
    
    img = camera.Capture()
    detections = net.Detect(img)
    for detection in detections:
        print(detection) 
    display.RenderOnce(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    print("DONE \n\n\n\n\n\n")


    
