##########################################################################################################################
# Project : Autonomous Drone											                                               	#
# Hardware: Raspberry pi ,Arducopter , laptop or desktop ,ultrasonic sensor HC-SR04					                    #
#	  : Arducopter(APM2.6)												                                                #
# Author  : Teja narayana                                                   #
# Author  : Mohan 
# Author  : Brijesh
# Author  : Surya
#															                                                            #
#by running this code, drone will go point A to point B autonomously.												    #
#															                                                            #
# Requrinment: Refer Tutorial Folder											                                        #
#########################################################################################################################


from dronekit import connect, VehicleMode, LocationGlobalRelative
import time




print ("connecting to vehicle....")
vehicle = connect('/dev/ttyACM0')
print ("connected")

#changing vehicle mode to stabilize
print ("\nSet Vehicle.mode = (currently: %s)" % vehicle.mode.name)
while not vehicle.mode=='GUIDED':
    vehicle.mode = VehicleMode('GUIDED')
    vehicle.flush()

print ("vehicle mode: %s" % vehicle.mode)

# ARMING the vehicle
vehicle.armed = True
while not vehicle.armed:
    vehicle.armed = True
    vehicle.flush()
    print (" trying to change mode and arming ...")
    time.sleep(1)

print ("its armed")

def arm_and_takeoff(aTargetAltitude):
    print ("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print (" Altitude: ", vehicle.location.global_relative_frame.alt) 
        #Break and return from function just below target altitude.        
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
            print ("Reached target altitude")
            break
        time.sleep(1)

arm_and_takeoff(3)

print ("Set default/target airspeed to 3")
vehicle.airspeed = 3

print ("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(17.7103992, 83.1650200, 3)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(10)

print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
point2 = LocationGlobalRelative(17.710276, 83.164871, 3)
vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(10)

print ("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print ("Close vehicle object")
vehicle.close()

