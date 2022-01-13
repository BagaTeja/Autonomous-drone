from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative


# Set up option parsing to get connection string
import argparse
#import Spray as S


parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', help="Vehicle connection target string. If not specified, SITL automatically started and used.")
parser.add_argument('--point', help="Number of points drone should visit.")
args = parser.parse_args()
connection_string = args.connect
Point_String = int(args.point)

Lati = []
Longi = []

for i in range(Point_String):
    mark = input("Enter Point " + str(i+1) + ": ")
    mark = mark.split(":")
    Lati.append(mark[0])
    Longi.append(mark[1])


sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


arm_and_takeoff(1)

print("Set default/target airspeed to 3")
vehicle.airspeed = 1

#print("Going towards first point for 30 seconds ...")
#point = LocationGlobalRelative(17.7108176,83.1644175, 2)
#vehicle.simple_goto(point)

# sleep so we can see the change in map
#time.sleep(30)

for i in range(Point_String):
    print("Going Towards Point " + str(i+1))
    point = LocationGlobalRelative(float(Lati[i]),float(Longi[i]), 2)
    vehicle.simple_goto(point)
    time.sleep(15)
    Pstatus = str(vehicle.location.global_frame)
    print("Lati: ", Pstatus[19:29])
    print("Longi: ", Pstatus[34:44])
    if i == 0:
        print("Spraying Started.......")
#        S.Spray().Start()


print("Spraying Stopped.......")
#S.Spray().Stop()

vehicle.mode = VehicleMode("LAND")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()

