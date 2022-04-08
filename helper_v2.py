"""
code for helping functions to use in dataset genereator
"""
import random
import pydub as pd


def match_target_amp(sound, target_dBFS):
    """
    function to reduce amplitude of the wav format audio file
    :param sound: pydub object
    :param target_dBFS: value in dB for normalization
    :return: normalized audio
    """
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def audio_trim(x):
    """
    function to extract random segment of random length from the original clean audio
     in between 30 sec to 50 sec
    :param x: audio file name
    :return: extracted and trimmed audio
    """
    aud = pd.AudioSegment.from_wav(x)
    sec = aud.duration_seconds
    random.seed(0)
    start = (random.randint(0, int(sec // 2))) * 1000
    end = random.randint(int(sec/2), int(sec)) * 1000
    extract = aud[start:end]
    return extract

def enf_trim(x, y):
    """
    function to trim already generated ENF files according to duration of trimmed clean audio
    :param x: ENF file name
    :param y: time duration in sec
    :return: trimmed ENF audio
    """
    aud = pd.AudioSegment.from_wav(x)
    sec = aud.duration_seconds
    start = 0
    end = y * 1000
    extract = aud[start:end]
    return extract

