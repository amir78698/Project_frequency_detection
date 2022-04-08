#!/usr/bin/env python

"""
Command line interface code for ENF detection for 50 and 60 HZ
"""

# import required packages
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from PIL import Image
import cv2
import numpy as np
import json
import argparse

# Defining class


class EnfDet:

    def __init__(self, aud_file, enf_fre):
        self.aud_file = aud_file
        self.enf_fre = enf_fre

    def main_code(self):
        """
        Function for ENF line detection and save the result in JSON format.
        aud_file:  path to the audio file (Only wav format is supported)
        enf_fre:  ENF to be detected ( Only 50 and 60Hz)
        return: Save result in JSON format
        """

        # error handling for wrong input for ENF to be detected
        if self.enf_fre != "50":
            if self.enf_fre != "60":
                print("Specify only 50 or 60 Hz -f")
                exit(1)

        # Check for wav format
        if not self.aud_file.endswith(".wav"):
            print("Only wav format audio file is supported")
            exit(1)


        # variable to assign ENF line length
        enf_len = 0

        # loading audio file
        fs1, audio1 = wav.read(self.aud_file)

        # Calculating time duration of given audio
        duration_seconds = len(audio1) / float(fs1)

        # condition for taking only one channel of stereo audio
        if len(audio1.shape) == 2:
            snd = audio1[:, 1]
        else:
            snd = audio1

        # plotting spectrum and saving as image
        fig = plt.figure(figsize=(10, 5))
        plt.specgram(snd, Fs=fs1, NFFT=32768, scale_by_freq=100, noverlap=900)
        plt.ylim([0, 200])
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.set_cmap('Dark2_r')
        plt.title('Audio Spectrum')
        plt.xlabel('time')
        plt.ylabel('frequency')
        fig.savefig(OutputPath+'/0-spec1.jpg', bbox_inches='tight', dpi=250)

        # Create an Image Object from an Image
        im = Image.open(OutputPath+'/0-spec1.jpg')

        # Crop (left, upper, right, lower)
        cropped = im.crop((400, 700, 2000, 900))

        # save cropped image
        cropped.save(OutputPath+'/1-crop.jpg')

        # reading crop image
        image1 = cv2.imread(OutputPath+'/1-crop.jpg')

        # copying imaage for final display
        real_img = image1.copy()

        # Edge detection in an image
        edges = cv2.Canny(image1, 100, 200, apertureSize=3)
        cv2.imwrite(OutputPath+'/2-edges.jpg', edges)

        # Line detection in an image after edge detection
        lines = cv2.HoughLinesP(edges, rho=1, theta=1*np.pi/180, threshold=45, minLineLength=145, maxLineGap=80)

        # loop to draw line on image
        # comment sse: This should draws only one line
        for x1, y1, x2, y2 in lines[0]:
            cv2.line(image1, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imwrite(OutputPath+'/3-lines.jpg', image1)

        # Green color range
        lower2 = [0, 0, 0]
        upper2 = [0, 255, 0]

        # converting color range into numpy array
        lower2 = np.array(lower2, dtype="uint8")
        upper2 = np.array(upper2, dtype="uint8")

        # creating mask
        mask2 = cv2.inRange(image1, lower2, upper2)  # mask for green color
        cv2.imwrite(OutputPath+'/4-mask.jpg', mask2)

        # putting mask on image
        output = cv2.bitwise_and(image1, image1, mask=mask2)
        cv2.imwrite(OutputPath+'/5-mask+image.jpg', output)

        # finding contour
        ret, thresh = cv2.threshold(mask2, 40, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            # draw in blue the contours that were founded
            cv2.drawContours(output, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)


            # for ENF 50Hz
            if self.enf_fre == "50":
                # condition for false positive
                if 100 > y > 80:
                    # draw the biggest contour (c) in red
                    cv2.rectangle(output, (x, y), (x+w, y+h), (0, 0, 255), 1)
                    enf_len = w

                else:
                    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 0), 3)
            # for ENF 60Hz
            elif self.enf_fre == "60":
                # condition for false positive
                if 40 > y > 20:
                    # draw the biggest contour (c) in red
                    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    enf_len = w
                else:
                    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 0), 3)

        cv2.imwrite(OutputPath+'/6-result.jpg', output)
        im_final = Image.open(OutputPath+'/6-result.jpg')
        width, height = im_final.size

        # Minimum ENF line length to declare as tempered or not
        line_len = 0.987*width
        #print("len: " + str(line_len))

        # for ENF 50Hz
        if self.enf_fre == "50":
            enfDetected = 100 > y > 80 and w != 0
            fileTampered = 100 > y > 80 and w < line_len

        # for ENF 60Hz
        elif self.enf_fre == "60":
            enfDetected =  40 > y > 20 and w != 0
            fileTampered = 40 > y > 20 and w < line_len



        # remove comment to display the ENF line image
        #cv2.imshow("ENF line Detection ", output)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


        if __name__ == '__main__':

            # saving results in json format
            data = {
                "file_name": args["audio"],
                "sampling_rate": fs1,
                "required_enf": args["Hz"],
                "audio_duration": duration_seconds,
                "enf_detected": enfDetected,
                "file_tampered": fileTampered,
                "width_of_spectrum_image": width,
                "line_to_spectrum_length_ratio": enf_len / width * 100

            }

            # Saving result in JSON format
            with open(OutputPath+"/result.json", 'w') as outfile:
                json.dump(data, outfile, indent=4)
            print("Result has been saved in JSON format")


        else:
            return enfDetected, fileTampered, enf_len / width * 100


if __name__ == '__main__':
    # creating argument parser for command line
    ap = argparse.ArgumentParser("ENF line detection for 50 and 60 Hz")
    ap.add_argument("-a", "--audio", type=str, required=True, default=None, help="Path to the audio file")
    ap.add_argument("-f", "--Hz", type=str, required=True, default=None,
                    help="Required electrical frequency to be detected")
    ap.add_argument("-o", "--OutputPath", type=str, required=False, default=None, help="Path to save result")

    args = vars(ap.parse_args())

    AudPath = args["audio"]
    freq = args["Hz"]
    OutputPath = args["OutputPath"]

    p = EnfDet(AudPath, freq)
    p.main_code()
