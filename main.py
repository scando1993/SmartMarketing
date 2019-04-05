from VisualCortex.visual_cortex import look_at_surroundings
from VisualCortex.CountPeople.people_counter import be_aware_of_surroundings
from AudioCortex.audio_cortex import listen_to_surroundings
from Config.Config import Config
import _thread
import argparse
from multiprocessing import Pool, Process

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--prototxt", required=True,
                    help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=True,
                    help="path to Caffe pre-trained model")
    ap.add_argument("-i", "--input", type=str,
                    help="path to optional input video file")
    ap.add_argument("-o", "--output", type=str,
                    help="path to optional output video file")
    ap.add_argument("-c", "--confidence", type=float, default=0.4,
                    help="minimum probability to filter weak detections")
    ap.add_argument("-s", "--skip-frames", type=int, default=30,
                    help="# of skip frames between detections")
    ap.add_argument("-d", "--detector", required=True,
                    help="path to OpenCV's deep learning face detector")
    ap.add_argument("-m1", "--embedding-model", required=True,
                    help="path to OpenCV's deep learning face embedding model")
    ap.add_argument("-r", "--recognizer", required=True,
                    help="path to model trained to recognize faces")
    ap.add_argument("-l", "--le", required=True,
                    help="path to label encoder")
    args = vars(ap.parse_args())

    config = Config()

    try:
        # p = Process(target=listen_to_surroundings, args=("AudioCortex", config))
        # p.start()
        _thread.start_new_thread(listen_to_surroundings, ("AudioCortex", config))
        # _thread.start_new_thread(look_at_surroundings, ("VisualCortex", config))
        _thread.start_new_thread(be_aware_of_surroundings, ("VisualCortexAwareness", config, args))
    except :
        print("Error, unable to start thread.")

    while True:
        pass

