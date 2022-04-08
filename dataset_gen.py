"""
Code to generate audio samples for training according to the labels using audio files
only wav format"
"""

import random
import glob
import pydub as pd
import helper  # self created utility functions
import argparse


def nENF():
    """
    function to generate clean audio files with different length
    and segments from the original audio files
     """
    i = 0
    while i < files_per_labels:
        x = random.choice(aud_data)
        trim_audio = helper.audio_trim(x)
        trim_audio.export(out_nENF+"/nENF%s.wav" % i, format="wav")
        i += 1
    print("Done")


def ENF(freq):
    """
    function to generate audio files with ENF at 50/60 Hz
    :param freq: "50" or "60"
    """
    i = 0
    while i < files_per_labels:
        x = random.choice(aud_data)
        trim_audio = helper.audio_trim(x)

        loud_enf = pd.AudioSegment.empty()

        if freq == "50":
            loud_enf = helper.enf_trim(ENF50_path, trim_audio.duration_seconds)

        elif freq == "60":
            loud_enf = helper.enf_trim(ENF60_path, trim_audio.duration_seconds)

        quiet_enf = helper.match_target_amp(loud_enf, -40)
        enf_signal = trim_audio.overlay(quiet_enf, position=0)

        if freq == "50":
            enf_signal.export(out_ENF50+"/ENF50%s.wav" % i, format="wav")

        elif freq == "60":
            enf_signal.export(out_ENF60+"/ENF60%s.wav" % i, format="wav")

        i += 1
    print("Done")


def tampered():
    """
    function to generate tampered audio files with random tampering patterns"

    """
    n = 0
    while n < files_per_labels:
        x = random.choice(aud_data)
        trim_audio = helper.audio_trim(x)
        sliced_audio = []
        changed_slices = []
        tampering_operations = []
        numberofslices = range(random.choice(range(3, 7)))
        for i in numberofslices:
            x = len(trim_audio) // (i+1)
            y = trim_audio[: x]
            sliced_audio.append(y)

        for slice in sliced_audio:
            operation = random.choice(labels)
            if operation == "nENF":
                slice = slice
                changed_slices.append(slice)
                tampering_operations.append(operation)

            elif operation == "ENF50":
                loud_enf = helper.enf_trim(ENF50_path, slice.duration_seconds)
                quiet_enf = helper.match_target_amp(loud_enf, -40)
                enf_signal = slice.overlay(quiet_enf, position=0)
                slice = enf_signal
                changed_slices.append(slice)
                tampering_operations.append(operation)

            elif operation == "ENF60":
                loud_enf = helper.enf_trim(ENF60_path, slice.duration_seconds)
                quiet_enf = helper.match_target_amp(loud_enf, -40)
                enf_signal = slice.overlay(quiet_enf, position=0)
                slice = enf_signal
                changed_slices.append(slice)
                tampering_operations.append(operation)
        merged_sound = pd.AudioSegment.empty()
        for i in changed_slices:
            merged_sound += i
        merged_sound.export(out_tampered+"/tampered%s.wav" % n, format="wav")

        n += 1

    print("Done")


if __name__ == "__main__":
    # creating argument parser for command line
    ap = argparse.ArgumentParser("Dataset generator for DNN training")
    ap.add_argument("-ad", "--audio_data", type=str, required=True, default=None,
                    help="Path to the original audio files only wav format")
    ap.add_argument("-f", "--files_per_class", type=int, required=True, default=None,
                    help="number of samples per class/label")
    ap.add_argument("-nENF", "--clean_audio", type=str, required=True, default=None,
                    help="Path to save clean audio files")
    ap.add_argument("-ENF50", "--audio_ENF50", type=str, required=True, default=None,
                    help="Path to save audio files with ENF at 50Hz")
    ap.add_argument("-ENF60", "--audio_ENF60", type=str, required=True, default=None,
                    help="Path to save audio files with ENF at 60Hz  ")
    ap.add_argument("-tam", "--audio_tampered", type=str, required=True, default=None,
                    help="Path to save tampered audio files")
    ap.add_argument("-enf50", "--path_ENF50", type=str, required=True, default=None,
                    help="Path to get file for ENF at 50 HZ")
    ap.add_argument("-enf60", "--path_ENF60", type=str, required=True, default=None,
                    help="Path to get file for ENF at 60 HZ")
    args = vars(ap.parse_args())

    # assigning variables
    aud_data = glob.glob(args["audio_data"])
    labels = ["nENF", "ENF50", "ENF60"]
    files_per_labels = args["files_per_class"]
    ENF50_path = args["path_ENF50"]
    ENF60_path = args["path_ENF60"]
    out_nENF = args["clean_audio"]
    out_ENF50 = args["audio_ENF50"]
    out_ENF60 = args["audio_ENF60"]
    out_tampered = args["audio_tampered"]

    # calling functions
    nENF()
    ENF("50")
    ENF("60")
    tampered()
