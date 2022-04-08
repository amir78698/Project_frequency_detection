"""
Code for detecting ENF Signal in an audio file, if ENF is present in the given signal then "ENF detected"
will be printed on terminal otherwise "Not Detected" will be printed
"""

# import required packages
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from PIL import Image
import cv2
import numpy as np
import os
import json
import argparse

def maincode():
    tempered = None
    result = None
    currentPath = os.path.dirname(os.path.realpath(__file__))
    #audioPath = os.path.join(currentPath, 'audio')
    outputPath = os.path.join(currentPath, 'output')

    # creating argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--audio", help="path to the audio file")
    ap.add_argument("-a", "--Hz", help="Electrical frequency")
    args = vars(ap.parse_args())

    # loading audio file
    fs1, audio1 = wav.read(args["audio"])

    # audio file duration
    duration_seconds = len(audio1) / float(fs1)

    # condition for taking only one channel of stereo audio
    if len(audio1.shape) == 2:
        snd = audio1[:, 1]
    else:
        snd = audio1

    # plotting spectrum and saving as image
    fig = plt.figure(figsize=(10,5))
    plt.specgram(snd, Fs=fs1, NFFT=32768, scale_by_freq=100, noverlap=900)
    plt.ylim([0, 200])
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.set_cmap('Dark2_r')
    plt.title('Audio Spectrum ')
    plt.xlabel('time')
    plt.ylabel('frequency')
    fig.savefig(outputPath+'/0-spec1.jpg', bbox_inches='tight', dpi=250)

    if args["Hz"] == "50":
        # Create an Image Object from an Image
        im = Image.open(outputPath+'/0-spec1.jpg')

        # Crop (left, upper, right, lower)
        cropped = im.crop((400, 700, 2000, 900))

        # save cropped image
        cropped.save(outputPath+'/1-crop.jpg')

        # reading crop image
        image1 = cv2.imread(outputPath+'/1-crop.jpg')

        # copying imaage for final display
        real_img = image1.copy()
        # Edge detection in an image
        edges = cv2.Canny(image1, 100, 200, apertureSize=3)
        cv2.imwrite(outputPath+'/2-edges.jpg',edges)

        # Line detection in an image after edge detection
        lines = cv2.HoughLinesP(edges, rho=1, theta=1*np.pi/180, threshold=45, minLineLength=145, maxLineGap=80)

        # loop to draw line on image
        # comment sse: This should draws only one line
        for x1, y1, x2, y2 in lines[0]:
            cv2.line(image1, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imwrite(outputPath+'/3-lines.jpg', image1)

        # Green color range
        lower2 = [0, 0, 0]
        upper2 = [0, 255, 0]


        # converting color range into numpy array
        lower2 = np.array(lower2, dtype = "uint8")
        upper2 = np.array(upper2, dtype = "uint8")

        # creating mask
        mask2 = cv2.inRange(image1, lower2, upper2)  # mask for green color
        cv2.imwrite(outputPath+'/4-mask.jpg',mask2)

        # putting mask on image
        output = cv2.bitwise_and(image1, image1, mask = mask2)
        cv2.imwrite(outputPath+'/5-mask+image.jpg',output)
        # show the resulted image



        # finding contour
        ret,thresh = cv2.threshold(mask2, 40, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            # draw in blue the contours that were founded
            cv2.drawContours(output, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)



            # condition for false positive
            # comment sse: Does this range really cover 50 and 60 Hz?
            if 100 > y > 80:
            # draw the biggest contour (c) in red
                cv2.rectangle(output,(x,y),(x+w,y+h),(0,0,255),1)
            else:
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 0), 3)


        cv2.imwrite(outputPath+'/6-result.jpg', output)

        # loading final output and calculating width and height
        im_final = Image.open(outputPath+'/6-result.jpg')
        width, height = im_final.size

        # threshold for detecting tempering
        line_len = 0.987*width


        # condition for ENF detection
        if 100 > y > 80 and w !=0:
            result = "ENF Detected"
        else:
            result = "ENF Not Detected"

        # condition for tempering detecion

        if 100 > y > 80 and w < line_len:
            tempered = "Audio File is Tempered"

        else:
            tempered = "Tempering not Detected "




        # Displaying cropped spectrogram image
        cv2.imshow("ENF Line Detection ", output)
        cv2.waitKey(0)

        # saving results in json format

        data = {
                "filename": args["audio"],
                "samplingRate": fs1,
                "Electrical frequency": args["Hz"],
                "lengthInSeconds": duration_seconds,
                "result": result,
                "details": tempered,
                "width_of_spectrum_image": width,
                "line_to_spectrum_length_ratio": w/width*100
            }

        with open(outputPath+'/data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)


maincode()