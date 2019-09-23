from Config.Person import Person
import datetime
import keyring
import pickle


# Need to set your own API codes
#keyring.set_password('skybio','api_key','XX')
#keyring.set_password('skybio','api_secret','XX')
#keyring.set_password('skybio','app_name','XX')
#keyring.set_password('skybio','namespace','XX')
#keyring.set_password('wolfram','app_id','XX')
#keyring.set_password('msft_azure','api_secret','XX')
#keyring.set_password('msft_azure','api_client','XX')
#keyring.set_password('google','api_secret','XX')

class Config:
    def __init__(self, person_list):
        self.personList = person_list
        self.threshold = 100
        self.sensitivity = 180
        self.forceCapture = True
        self.forceCaptureTime = 60 * 60  # Once an hour
        self.diskSpaceToReserve = 40 * 1024 * 1024  # Keep 40 mb free on disk
        self.CaptureDuration = 0

        self.gettingVoiceInput = False
        self.gettingVisualInput = False
        self.gettingStillImages = False
        self.gettingStillAudio = False

        # How long to wait before stopping routine if nothing is happening
        self.audioHangout = 60  # seconds
        self.videoHangout = 300  # seconds

        # How long to wait before starting up the routine again
        self.timeTimeout = 0

        # Force facial recognition
        self.lookForFaces = 0

        self.debugging = True

        self.tasksLoaded = False
        self.no_faces_available = True
        self.people_available = 0

        self.face_probability = 0.50
        self.faces_detected = []

