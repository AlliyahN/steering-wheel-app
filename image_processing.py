import cv2
import numpy as np
from PIL import Image, ImageTk
# Library that can be used to grab contours
import imutils

class ImageProcessing:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.dir1_mask = None # Will be used to show only direction 1 colour
        self.dir2_mask = None # Will be used to show only direction 2 colour
        self.brake_mask = None # Will be used to show only brake colour
        self.acc_mask = None # Will be used to show only acceleration colour

        # All these contours will be found using the "find_contours" function of this class
        self.dir1_contours = None
        self.dir2_contours = None
        self.brake_contours = None
        self.acc_contours = None
    
    # Function that will be used in calibration window
    def calibration_frame(self, lower_bound, upper_bound):
        _, image_BGR = self.cap.read()
        image_BGR = cv2.flip(image_BGR, 1)
        # Blurs the BGR image using median blur
        blurred_image = cv2.medianBlur(image_BGR, 15)
        # Converts blurred image to HSV colour space and stored in self.image_HSV
        image_HSV = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)
        # Parts of HSV image within lower_bound and upper_bound
        mask = cv2.inRange(image_HSV, lower_bound, upper_bound)
        # Performs bitwise_and function which overlays the mask on the original BGR image, storing this result in a variable
        result = cv2.bitwise_and(image_BGR, image_BGR, mask=mask)
        
        # Converts the result from BGR to RGBA otherwise image is in wrong colour space (e.g. red colours will look blue)
        cv2image = cv2.cvtColor(result, cv2.COLOR_BGR2RGBA)
        # Converts cv2 image to a Pillow image
        img = Image.fromarray(cv2image)
        # Creates a PhotoImage of the Pillow image above
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Returns this for the GUI to use
        return imgtk

    # Function that will be used in play window once colours have been calibrated for
    def play_frame(self, dir1_HSV, dir2_HSV, brake_HSV, acc_HSV):
        _, image_BGR = self.cap.read()
        image_BGR = cv2.flip(image_BGR, 1)
        blurred_image = cv2.medianBlur(image_BGR, 15)
        image_HSV = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

        # ..._HSV = [Numpy array of lower bound, Numpy array of upper bound]
        self.dir1_mask = cv2.inRange(image_HSV, dir1_HSV[0], dir1_HSV[1])
        self.dir2_mask = cv2.inRange(image_HSV, dir2_HSV[0], dir2_HSV[1])
        self.brake_mask = cv2.inRange(image_HSV, brake_HSV[0], brake_HSV[1])
        self.acc_mask = cv2.inRange(image_HSV, acc_HSV[0], acc_HSV[1])

        # Creates a mask that contains all 4 of the colours
        resultant_mask = self.dir1_mask + self.dir2_mask + self.brake_mask + self.acc_mask

        result = cv2.bitwise_and(image_BGR, image_BGR, mask=resultant_mask)
        cv2image = cv2.cvtColor(result, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        
        return imgtk

    # Function used to find the contours in each of the separate colours' masks
    def find_contours(self):
        # Contours found using OpenCV's function "findContours"
        self.dir1_contours = cv2.findContours(self.dir1_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Contours grabbed to be stored using imutils' function "grab_contours"
        self.dir1_contours = imutils.grab_contours(self.dir1_contours)
        
        self.dir2_contours = cv2.findContours(self.dir2_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.dir2_contours = imutils.grab_contours(self.dir2_contours)

        self.brake_contours = cv2.findContours(self.brake_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.brake_contours = imutils.grab_contours(self.brake_contours)

        self.acc_contours = cv2.findContours(self.acc_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.acc_contours = imutils.grab_contours(self.acc_contours)

    # Function to find radius and centre of contours
    def find_radius_and_centre(self, contours):
        # Finds the largest contour by area of, for example, brake_contours
        c = max(contours, key=cv2.contourArea)
        # Finds the minimum enclosing circle of that biggest contour and gets the centre coordinates and radius of circle
        ((centre), radius) = cv2.minEnclosingCircle(c)

        return radius, centre

    # Function which returns True if accelerating colour is shown, otherwise False
    def check_acceleration(self):
        # Checks if the length of the acceleration contours is more than 0 suggesting acceleration colour could be being shown by user
        if len(self.acc_contours) > 0:
            # Uses "find_radius_and_centre" function to find the radius and centre
            radius, centre = self.find_radius_and_centre(self.acc_contours)

            # If radius is larger than 15 then this suggest user is showing their acceleration colour
            if radius > 15:
                return True
        return False

    # Function which returns True if braking colour is shown, otherwise False
    def check_braking(self):
        # Same logic from "check_acceleration" function except with the braking contours
        if len(self.brake_contours) > 0:
            radius, centre = self.find_radius_and_centre(self.brake_contours)

            if radius > 15:
                return True
        return False
    
    # Function which returns string of direction to turn if both direction colours are in frame
    def check_direction(self):
        # If the lengths of both direction contours are more than 0 then the steering direction can be determined
        if len(self.dir1_contours) > 0 and len(self.dir2_contours) > 0:
            # FInds radii and centres of direction contours
            dir1_radius, dir1_centre = self.find_radius_and_centre(self.dir1_contours)

            dir2_radius, dir2_centre = self.find_radius_and_centre(self.dir2_contours)

            # If both radii are more than 15 then it suggests both direction colours are in frame so that a direction can be determined
            if dir1_radius > 15 and dir2_radius > 15:
                # If the x-coordinate of the top colour is less than that of the bottom colour minus 40 (threshold)
                if dir1_centre[0] < (dir2_centre[0] - 40):
                    # Suggests user wants to steer left
                    return "LEFT"
                # Otherwise if the x-coordinate of the bottom colour is less than that of the top colour minus 40 (threshold)
                elif dir2_centre[0] < (dir1_centre[0] - 40):
                    # Suggests user wants to steer right
                    return "RIGHT"
                # Otherwise
                else:
                    # Suggests user wants to drive straight
                    return "STRAIGHT"
        
        # Returns message if at least one of the direction colours is missing from the frame
        return "Contour(s) missing"