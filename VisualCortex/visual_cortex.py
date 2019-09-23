from Config.Config import Config
import datetime 
import io
import subprocess
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
# from face_client import FaceClient
from Config import Person
from AudioCortex import mouth_function
import pickle
import time
import os
# import keyring
import sys
import math

#---------Motion detection and face recognition-----------

def recognize_face(config):
	num_faces = len(config.faces_detected)
	print("Detected " + str(num_faces) + " faces.")
	iii = 0

	the_speech = ""
	while iii < num_faces:
		for person in config.personList:
			try:
				found_name = config.faces_detected[iii]
				print("I see " + found_name)
				if person.name in found_name:
					the_speech = the_speech + "%s" % person.greeting

					timeDifference = datetime.datetime.now() - person.lastSeen
					person.lastSeen = datetime.datetime.now()
					# personList[j].lastSeen = person.lastSeen
					days = math.floor(timeDifference.total_seconds() / 60 / 60 / 24)
					hours = math.floor(timeDifference.total_seconds() / 60 / 60	)	
					minutes = math.floor(timeDifference.total_seconds() / 60 )	
					if days > 0:
						the_speech = the_speech + "It's been %d days since I have seen you, %s. " % (days, person.name)
					elif hours > 4:
						the_speech = the_speech + "It's been %d hours since I have seen you, %s. " % (hours, person.name)
					elif minutes > 0:
						the_speech = the_speech + "It's been %d minutes since I have seen you, %s. " % (minutes, person.name)

			except:
				print("Error locating face in person database.")
				print("Unexpected error:", sys.exc_info()[0])
				raise
		iii = iii + 1
	
	if len(the_speech) > 2:
		# proxy for if something happened
		pickle.dump(config.personList, open("ai_data/personlist.p", "wb"))
	return the_speech


# Check whether a face has been seen recently
def seen_a_face_in_a_while(config):
	# first check if anybody has been seen
	has_seen_someone = False
	for person in config.personList:
		timeDifference = datetime.datetime.now() - person.lastSeen
		# personList[j].lastSeen = person.lastSeen
		days = round(timeDifference.total_seconds() / 60 / 60 / 24)
		hours = round(timeDifference.total_seconds() / 60 / 60	)	
		minutes = round(timeDifference.total_seconds() / 60)
		if minutes < 10 and days < 1 and hours < 1:
			has_seen_someone = True
	return has_seen_someone


# Save a full size image to disk
def save_image(config):
	# keep_disk_space_free(config)
	time_ = datetime.datetime.now()

	theSpeech = recognize_face(config)
	if len(theSpeech) > 2:
		print(theSpeech)
		# saySomething(theSpeech, "en")
		config.lookForFaces = False


# Keep free space above given level
def keep_disk_space_free(config):
	bytes_to_reserve = config.diskSpaceToReserve
	if get_free_space() < bytes_to_reserve:
		for filename in sorted(os.listdir(".")):
			if filename.startswith(config.filenamePrefix) and filename.endswith("." + config.fileType):
				os.remove(filename)
				print("Deleted %s to avoid filling disk" % filename)
				if get_free_space() > bytes_to_reserve:
					return


# Get available disk space
def get_free_space():
	st = os.statvfs(".")
	du = st.f_bavail * st.f_frsize
	return du


def look_at_surroundings(threadName, config):
	# check that recognizer and microphone arguments are appropriate type
	if not isinstance(config, Config):
		raise TypeError("`recognizer` must be `Config` instance")

	motionDetectedLast = datetime.datetime.now()
	motionDetectedNow = datetime.datetime.now()
	print("Started listening on thread %s" % threadName)

	# look at surroundings
	lastCapture = time.time()

	while True:
		# check if CPU intensive processes are running
		if config.gettingStillImages and config.gettingStillAudio:
			if config.timeTimeout == 0:
				config.timeTimeout = 10
			print("No one is around, closing eyes for %d seconds" % config.timeTimeout)
			time.sleep(config.timeTimeout)
			config.gettingStillImages = 0
			motionDetectedLast = datetime.datetime.now()

		if config.gettingVoiceInput:
			time.sleep(6)
		else:
			if config.people_available > 0:
				motionDetectedLast = datetime.datetime.now()
				motionHasBeenDetected = True
				config.timeTimeout = 0  # reset timeout
				if not seen_a_face_in_a_while(config):
					config.gettingVisualInput = True
					save_image(config)  # face detection
					config.gettingVisualInput = False

			time_difference = datetime.datetime.now() - motionDetectedLast

			if time_difference.total_seconds() > config.videoHangout:
				config.gettingStillImages = True
			else:
				config.gettingStillImages = False

			if config.lookForFaces:
				config.gettingVisualInput = True
				save_image(config) # face detection
				config.gettingVisualInput = False
