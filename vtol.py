from dronekit import *
import time 
import socket 
from pymavlink import mavutil
from threading import Thread
import jetson1 as jp
import logging

# Enable dronekit logging
logging.basicConfig(level=logging.DEBUG)
def vehicle_connection():
    #for usb serial connection
    connection_string = "/dev/ttyACM0"

    #for ardupilot sitl connection
    connection_string = "tcp:127.0.0.1:5760"
    baud_rate = 57600
    try:
        vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)
        logging.info("Connecting to vehicle on: " + connection_string)
        return vehicle
    except Exception as e:
        logging.error("Error connecting to vehicle on id: %s", connection_string)
        logging.error(e)
        return None

def arm_and_takeoff(TargetAltitude):

    vehicle = vehicle_connection()

    #Arm vehicle once GUIDED mode is confirmed
    vehicle.armed = True
    while vehicle.armed == False:
        print("Waiting for vehicle to become armed")
        time.sleep(1)
    
    #Switch vehicle to GUIDED mode and wait for change
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode != "GUIDED":
        print("Waiting for vehicle to enter GUIDED mode")
        time.sleep(1)
 
    # Wait for GPS to become available
    while not vehicle.gps_0.fix_type:
        print('Waiting for GPS...')

    # Print the drone's latitude and longitude
    print('Current GPS location: {0}, {1}'.format(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon))
    
    # Define the mission
    mission_items = [
                mavutil.mavlink.MAVLink_mission_item_message(
                            vehicle.commands.target_system,  # target system ID
                            vehicle.commands.target_component,  # target component ID
                            seq,  # sequence number
                            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,  # frame
                            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,  # command ID
                            0,  # current WP
                            0,  # autocontinue
                            0, 0, 0,  # x, y, z position
                            speed,  # speed
                            0, 0, 0),  # parameters
                        ]
    for item in mission_items:
        vehicle.commands.add(item)
    vehicle.commands.upload()

    vehicle.simple_takeoff(TargetAltitude)

    # Set the vehicle mode to AUTO
    #vehicle.mode = VehicleMode("AUTO")
    
    my_thread = Thread(target = jp.execute)
    my_thread.start()
    # Monitor mission execution
    while True:
        nextwaypoint = vehicle.commands.next
        if nextwaypoint == len(vehicle.commands):
            print("Mission complete")
            break
        time.sleep(1)
    # Land the vehicle
    vehicle.mode = VehicleMode("LAND")

    # Disarm the vehicle
    vehicle.armed = False
    while vehicle.armed:
        print("Waiting for vehicle to disarm...")
        time.sleep(1)



if __name__ == "__main__":
    TargetAltitude = 1
    arm_and_takeoff(TargetAltitude)

