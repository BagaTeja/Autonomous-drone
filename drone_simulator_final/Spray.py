import RPi.GPIO as pi

Trigger_Pin = 17

pi.setmode(pi.BCM)
pi.setwarnings(False)
pi.setup(Trigger_Pin, pi.OUT)

class Spray:

	def Start(self):
		print("Triggering High Input")
		pi.output(Trigger_Pin, pi.HIGH)

	def Stop(self):
		print("Triggering Low Input")
		pi.output(Trigger_Pin, pi.LOW)
