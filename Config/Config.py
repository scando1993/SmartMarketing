from Config.Person import Person
import datetime
import keyring
import pickle

# make a list of class Person(s)
try:
    personList = pickle.load(open("Ai_data/personlist.p","rb"))
except:
    personList = []
    personList.append(Person(name="Kevin", job="Master of Creation"))
    pickle.dump(personList, open("Ai_data/personlist.p","wb"))

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
    def __init__(self):
        self.threshold = 100
        self.sensitivity = 180
        self.forceCapture = True
        self.forceCaptureTime = 60 * 60  # Once an hour
        self.filepath = "/home/pi/rpi_ai/video/"
        self.filenamePrefix = "pgm"
        self.fileType = "jpg"
        self.saveWidth = 800  # File photo size settings
        self.saveHeight = 600
        self.diskSpaceToReserve = 40 * 1024 * 1024  # Keep 40 mb free on disk
        self.CaptureDuration = 0
        self.publicIP = keyring.get_password('my', 'public_ip')

        self.gettingVoiceInput = False
        self.gettingVisualInput = False
        self.gettingStillImages = False
        self.gettingStillAudio = False

        self.blackLight = False
        self.windowLamp = False

        # How long to wait before stopping routine if nothing is happening
        self.audioHangout = 60  # seconds
        self.videoHangout = 300  # seconds
        # How long to wait before starting up the routine again
        self.timeTimeout = 0

        # Force facial recognition
        self.lookForFaces = 0

        self.debugging = True

        self.tasksLoaded = False


