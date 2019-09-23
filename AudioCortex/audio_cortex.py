from Config.Config import Config
import os
import pyaudio
from AudioCortex.mouth_function import say_something
# from TemporalLobe import temporal_lobe
import time
import datetime
import audioop
import numpy

import speech_recognition as sr

# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def recognize_speech_from_mic(_recognizer, _microphone, time_limit=None):
	"""Transcribe speech from recorded from `microphone`.

	Returns a dictionary with three keys:
	"success": a boolean indicating whether or not the API request was
			   successful
	"error":   `None` if no error occured, otherwise a string containing
			   an error message if the API could not be reached or
			   speech was unrecognizable
	"transcription": `None` if speech could not be transcribed,
			   otherwise a string containing the transcribed text
	"""
	# check that recognizer and microphone arguments are appropriate type
	if not isinstance(_recognizer, sr.Recognizer):
		raise TypeError("`recognizer` must be `Recognizer` instance")

	if not isinstance(_microphone, sr.Microphone):
		raise TypeError("`microphone` must be `Microphone` instance")

	# adjust the recognizer sensitivity to ambient noise and record audio
	# from the microphone
	with _microphone as source:
		_recognizer.adjust_for_ambient_noise(source)
		if time_limit is None:
			audio = _recognizer.listen(source)
		else:
			audio = _recognizer.listen(source, phrase_time_limit=time_limit)

	# set up the response object
	response = {
		"success": True,
		"error": None,
		"transcription": None
	}

	# try recognizing the speech in the recording
	# if a RequestError or UnknownValueError exception is caught,
	#     update the response object accordingly
	try:
		response["transcription"] = _recognizer.recognize_google(audio, language="es-EC")
	except sr.RequestError:
		# API was unreachable or unresponsive
		response["transcription"] = ""
		response["success"] = False
		response["error"] = "API unavailable"
	except sr.UnknownValueError:
		# speech was unintelligible
		response["error"] = "Unable to recognize speech"

	return response


def get_user_permission(question):
	answer = False
	say_something(question, "en")
	response = get_users_voice(2)
	if "yes" in response or "sure" in response or "okay" in response:
		answer = True
	return answer


def listen_to_surroundings(thread_name, config):
	try:
		print("Started listening on thread %s" % thread_name)

		# check that recognizer and microphone arguments are appropriate type
		if not isinstance(config, Config):
			raise TypeError("`recognizer` must be `Config` instance")

		volume_threshold = calibrate_ambient_noise()

		while True:
			# set after running the previous commands and looking at vtput
			print("Volume threshold set at %2.1f" % volume_threshold)

			if config.gettingStillImages and config.gettingStillAudio:
				pass
			elif config.gettingVisualInput:
				time.sleep(5)
			else:
				print("Starting listening stream")
				lastInterupt = time.datetime.now()
				config.gettingStillAudio = False
				rmsTemp = 0

				# listen to surroundings
				while rmsTemp < volume_threshold and not config.gettingVisualInput:
					# adjust the recognizer sensitivity to ambient noise and record audio
					# from the microphone
					with microphone as source:
						recognizer.adjust_for_ambient_noise(source)
						audio = recognizer.listen(source)

					data = audio.frame_data
					rmsTemp = audioop.rms(data, 2)
					timeDifference = datetime.datetime.now() - lastInterupt

					if timeDifference.total_seconds() > config.audioHangout:
						config.gettingStillAudio = True
						volume_threshold = calibrate_ambient_noise()

					if config.gettingStillAudio and config.gettingStillImages:
						break

				if not config.gettingVisualInput and not config.gettingStillAudio:
					config.timeTimeout = 0 # reset timeout
					config.gettingVoiceInput = True
					output = get_users_voice(5)
					# temporal_lobe.process_input(output, config)
					print("user said: " + output)
					config.gettingVoiceInput = False
	except:
		import traceback
		print(traceback.format_exc())


def get_users_voice(speaking_time, prompt_limit=5):
	for j in range(prompt_limit):
		print('Speak now!')
		guess = recognize_speech_from_mic(recognizer, microphone, time_limit=speaking_time)
		if guess["transcription"]:
			break
		if not guess["success"]:
			break
		print("I didn't catch that. What did you say?\n")

	# if there was an error, stop the game
	if guess["error"]:
		print("ERROR: {}".format(guess["error"]))

	return guess["transcription"]


def calibrate_ambient_noise():
	rms = []
	rms_mean = 0
	for i in range(0, 10):
		# adjust the recognizer sensitivity to ambient noise and record audio
		# from the microphone
		with microphone as source:
			recognizer.adjust_for_ambient_noise(source)
			audio = recognizer.listen(source, phrase_time_limit=1)
		data = audio.frame_data
		rms_temp = audioop.rms(data, 2)
		print(rms_temp)
		rms.append(rms_temp)
		rms_mean = numpy.mean(rms)
		rms_std = numpy.std(rms)
		print(rms)
		print(rms_mean)
		print(rms_std)
	return rms_mean
