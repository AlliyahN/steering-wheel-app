# Module used to create simple-looking GUI applications
import tkinter as tk
# Imports numpy for arrays used in CalibrationWindow
import numpy as np
# Imports the class that was created for image processing
from image_processing import ImageProcessing
# Module used for virtual keyboard presses
from pynput.keyboard import Key, Controller
# Module to be used to display images in the user guide
from PIL import Image, ImageTk

# Global variable used by CalibrationWindow class and PlayWindow class
global calibrated
calibrated = False # Set to false because when the program is run, calibration will not have been completed

#  Global variable to be used by PlayWindow class and KeyboardPref
global keys_to_use
keys_to_use = [Key.up, Key.left, Key.down, Key.right] # Default set to arrow keys

# Class for the main menu window
class MainMenuWindow:

    # __init__ function showing what will be on the window when first opened
    def __init__(self, master):
        self.master = master # Root
        self.master.resizable(0, 0) # Makes sure window cannot be resized in any direction
        # Text that will appear in the title bar of this window
        self.master.title("Steering Wheel Application")

        # Title label to appear at the top of the contents of the window
        self.lbl_title = tk.Label(self.master, text="STEERING WHEEL APPLICATION", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20) # Gives title padding around the outside of the label

        # "Begin Calibration" button is linked to the "open_cal_win" function
        self.btn_begin_calibration = tk.Button(self.master, text="Begin Calibration", background="orange", font=("Helvetica", 15), width=20, height=2, command=self.open_cal_win)
        self.btn_begin_calibration.grid(row=1, column=0, pady=10) # Underneath title and has 10 pixels of padding outside the top and bottom of the button

        # "Start Playing" button is linked to the "open_play_win" function
        self.btn_start_playing = tk.Button(self.master, text="Start Playing", background="orange", font=("Helvetica", 15), width=20, height=2, command=self.open_play_win)
        self.btn_start_playing.grid(row=2, column=0, pady=10)

        # "Keyboard Preferences" button is linked to the "open_key_prefs_win" function
        self.btn_key_prefs = tk.Button(self.master, text="Keyboard Preferences", background="orange", font=("Helvetica", 15), width=20, height=2, command=self.open_key_prefs_win)
        self.btn_key_prefs.grid(row=3, column=0, pady=10)

        # "About" button is linked to the "open_about_win" function
        self.btn_about = tk.Button(self.master, text="About", background="orange", font=("Helvetica", 15), width=20, height=2, command=self.open_about_win)
        self.btn_about.grid(row=4, column=0, pady=(10, 20)) # Needs to have different padding on the top and bottom
    
    # Function called to open the calibration window when the "Begin Calibration" button is pressed
    def open_cal_win(self):
        # Creates new window with the top level being the master (i.e. the root)
        self.newWindow = tk.Toplevel(self.master)
        # Calibration window has the self.newWindow as the master
        self.app = CalibrationWindow(self.newWindow)

    # Function called to open the play window when the "Start Playing" button is pressed
    def open_play_win(self):
        # Creates new window with the top level being the master (i.e. the root)
        self.newWindow = tk.Toplevel(self.master)        
        # Play window has the self.newWindow as the master
        self.app = PlayWindow(self.newWindow)

    # Function called to open the keyboard preferences window when the "Keyboard Preferences" button is pressed
    def open_key_prefs_win(self):
        # Creates new window with the top level being the master (i.e. the root)
        self.newWindow = tk.Toplevel(self.master)
        # Keyboard preferences window has the self.newWindow as the master
        self.app = KeyboardPrefsWindow(self.newWindow)

    # Function called to open the about window when the "About" button is pressed
    def open_about_win(self):
        # Creates new window with the top level being the master (i.e. the root)
        self.newWindow = tk.Toplevel(self.master)
        # About window has the self.newWindow as the master
        self.app = AboutWindow(self.newWindow)

# Class that contains the contents of the calibration window
class CalibrationWindow:
    
    def __init__(self, master):
        # Instance of "ImageProcessing" class which can be accessed by all functions in CalibrationWindow class
        self.image_processor = ImageProcessing()

        # Global variables to store lists of numpy arrays for the lower bound and upper bound of the colours
        global dir1_HSV
        dir1_HSV = []

        global dir2_HSV
        dir2_HSV = []

        global brake_HSV
        brake_HSV = []

        global acc_HSV
        acc_HSV = []

        self.master = master
        self.master.title("Calibration")
        self.master.resizable(0, 0)

        # Label to display the camera footage
        self.lbl_cam = tk.Label(self.master)
        self.lbl_cam.grid(row=0, column=0, rowspan=7) # Positioned to the right of window taking up 7 rows

        # Lower hue trackbar initially set to 0 and has a range from 0 to 179
        self.l_h = tk.Scale(self.master, label="L - H", from_=0, to=179, orient="horizontal", length=300, font=("Helvetica", 12))
        self.l_h.set(0)

        # Lower saturation trackbar initially set to 0 and has a range from 0 to 255
        self.l_s = tk.Scale(self.master, label="L - S", from_=0, to=255, orient="horizontal", length=300, font=("Helvetica", 12))
        self.l_s.set(0)

        # Lower value trackbar initially set to 0 and has a range from 0 to 255
        self.l_v = tk.Scale(self.master, label="L - V", from_=0, to=255, orient="horizontal", length=300, font=("Helvetica", 12))
        self.l_v.set(0)

        # Upper hue trackbar initially set to 179 and has a range from 0 to 179
        self.u_h = tk.Scale(self.master, label="U - H", from_=0, to=179, orient="horizontal", length=300, font=("Helvetica", 12))
        self.u_h.set(179)

        # Upper saturation trackbar initially set to 255 and has a range from 0 to 255
        self.u_s = tk.Scale(self.master, label="U - S", from_=0, to=255, orient="horizontal", length=300, font=("Helvetica", 12))
        self.u_s.set(255)

        # Upper value trackbar initially set to 255 and has a range from 0 to 255
        self.u_v = tk.Scale(self.master, label="U - V", from_=0, to=255, orient="horizontal", length=300, font=("Helvetica", 12))
        self.u_v.set(255)

        # All 6 trackbars stored in list for convenience
        self.trackbars = [self.l_h, self.l_s, self.l_v, self.u_h, self.u_s, self.u_v]

        # Will be programmed to ensure lbl_cam shows camera footage according to trackbar positions
        self.show_frame()
        # Shows the trackbars (convenience function called)
        self.show_trackbars()

        # Begin stage 1 of calibration
        self.stage_1()

    def show_frame(self):
        # All elements dependent on lower HSV trackbars
        lower_bound = np.array([self.l_h.get(), self.l_s.get(), self.l_v.get()])
        # All elements dependent on upper HSV trackbars
        upper_bound = np.array([self.u_h.get(), self.u_s.get(), self.u_v.get()])
        # "ImageProcessing" class' "calibration_frame" function called with above upper and lower bounds as parameters
        imgtk = self.image_processor.calibration_frame(lower_bound, upper_bound)
        # Sets lbl_cam's imgtk to the return of the function called in previous line
        self.lbl_cam.imgtk = imgtk
        self.lbl_cam.configure(image=imgtk)
        # Makes sure to repeat this function every 10 ms to give effect of video playing (just a series of images shown at rapid speed)
        self.lbl_cam.after(10, self.show_frame)

    # Convenience function to show all the trackbars without having to write it out one by one
    def show_trackbars(self):
        # Each trackbar will be positioned right of the calibration image with their row number being based on their position in the trackbars list
        for i in range(len(self.trackbars)):
            self.trackbars[i].grid(row=i, column=1) 

    # Function to reset the values of the trackbars to be at their default positions
    def reset_trackbars(self):
        # For the first 3 trackbars in the trackbars list (all of which are the lower HSV trackbars)
        for i in range(3):
            self.trackbars[i].set(0)
        
        # Manually reset upper HSV trackbars which have different maximum values
        self.u_h.set(179)
        self.u_s.set(255)
        self.u_v.set(255)

    # Function called when any of the store buttons are pressed
    def store_colour(self, mask_type, next_stage_number):
        # Gets the lower bound of this colour from getting the values of the lower HSV trackbars
        lower_HSV = np.array([self.l_h.get(), self.l_s.get(), self.l_v.get()])
        # Gets the upper bound of this colour from getting the values of the upper HSV trackbars
        upper_HSV = np.array([self.u_h.get(), self.u_s.get(), self.u_v.get()])

        # Checks the mask_type parameter
        if mask_type == "dir1":
            # Stores the upper and lower bound in the global variable for use in play window
            global dir1_HSV
            dir1_HSV = [lower_HSV, upper_HSV]
            # Destroys the store button for direction colour 1 so it can be replaced by the next button
            self.btn_dir1.destroy()
        elif mask_type == "dir2":
            # Stores the upper and lower bound in the global variable for use in play window
            global dir2_HSV
            dir2_HSV = [lower_HSV, upper_HSV]
            # Destroys the store button for direction colour 2 so it can be replaced by the next button
            self.btn_dir2.destroy()
        elif mask_type == "brake":
            # Stores the upper and lower bound in the global variable for use in play window
            global brake_HSV
            brake_HSV = [lower_HSV, upper_HSV]
            # Destroys the store button for brake colour so it can be replaced by the next button
            self.btn_brake.destroy()
        elif mask_type == "acc":
            # Stores the upper and lower bound in the global variable for use in play window
            global acc_HSV
            acc_HSV = [lower_HSV, upper_HSV]
            # Destroys the store button for acceleration colour so it can be replaced by the next button
            self.btn_acc.destroy()
        else:
            print("Invalid mask type") # If none of the above mask types are passed in as a parameter

        # Will be populated with next stages as more are coded
        next_stages = [self.stage_2, self.stage_3, self.stage_4]
        
        # Creates a next button that will link to starting the next stage of calibration if the stage is not the last stage
        if next_stage_number <= len(next_stages) + 1:
            self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=25, height=2, command=next_stages[next_stage_number-2])
            self.btn_next.grid(row=6, column=1, pady=10)
        # Otherwise a finish button will be created to finish the calibration
        else:
            self.btn_finish = tk.Button(self.master, text="Finish Calibration", background="light green", font=("Helvetica", 13), width=25, height=2, command=self.finish_calibration)
            self.btn_finish.grid(row=6, column=1, pady=10)

    # Function for stage 1 of the calibration
    def stage_1(self):
        # Button to store direction colour 1
        self.btn_dir1 = tk.Button(self.master, text="Store Direction Colour 1", background="orange", font=("Helvetica", 13), width=25, height=2, command=lambda: self.store_colour("dir1", 2))
        # Button positioned at the bottom right of screen
        self.btn_dir1.grid(row=6, column=1, pady=10)

    # Function for stage 2 of the calibration
    def stage_2(self):
        # Destroys next button so that it can be replaced by store button
        self.btn_next.destroy()
        # Calls function to reset value of trackbars following stage 1's adjustments
        self.reset_trackbars()
        # Button to store direction colour 2
        self.btn_dir2 = tk.Button(self.master, text="Store Direction Colour 2", background="orange", font=("Helvetica", 13), width=25, height=2, command=lambda: self.store_colour("dir2", 3))
        # Button positioned at the bottom right of screen
        self.btn_dir2.grid(row=6, column=1, pady=10)
    
    # Function for stage 3 of the calibration
    def stage_3(self):
        # Destroys next button so that it can be replaced by store button
        self.btn_next.destroy()
        # Calls function to reset value of trackbars following stage 2's adjustments
        self.reset_trackbars()
        # Button to store brake colour
        self.btn_brake = tk.Button(self.master, text="Store Brake Colour", background="orange", font=("Helvetica", 13), width=25, height=2, command=lambda: self.store_colour("brake", 4))
        # Button positioned at the bottom right of screen
        self.btn_brake.grid(row=6, column=1, pady=10)
    
    # Function for stage 4 (last stage) of the calibration
    def stage_4(self):
        # Destroys next button so that it can be replaced by store button
        self.btn_next.destroy()
        # Calls function to reset value of trackbars following stage 3's adjustments
        self.reset_trackbars()
        # Button to store acceleration colour
        self.btn_acc = tk.Button(self.master, text="Store Acceleration Colour", background="orange", font=("Helvetica", 13), width=25, height=2, command=lambda: self.store_colour("acc", 5))
        # Button positioned at the bottom right of screen
        self.btn_acc.grid(row=6, column=1, pady=10)
    
    # Function called when "Finish Calibration" button pressed
    def finish_calibration(self):
        # User's camera is no longer needed (until they need to play)
        self.image_processor.cap.release()
        # Destroy everything on screen to replace with prompt message
        self.lbl_cam.destroy()
        self.btn_finish.destroy()
        # Demonstrates convenience of storing all trackbars in a list
        for trackbar in self.trackbars:
            trackbar.destroy()

        # New content
        self.lbl_finish = tk.Label(self.master, text="Calibration finished!", font=("Helvetica", 20, "bold"))
        self.lbl_finish.grid(row=0, column=0, pady=10) # Padding given to title label
        
        self.lbl_prompt = tk.Label(self.master, text="You can now close this window and press the 'Start Playing' button on the main menu window.", font=("Helvetica", 15))
        self.lbl_prompt.grid(row=1, column=0, padx=40, pady=50) # Will be placed underneath lbl_finish's text

        # Since the user has pressed the "Finish Calibration" button the variable "calibrated" can be set to true
        global calibrated
        calibrated = True

# Class that contains the contents of the play window
class PlayWindow:
    
    # __init__ function to store the master and set the title of the window
    def __init__(self, master):
        # Instance of "ImageProcessing" class which can be accessed by all functions in PlayWindow class
        self.image_processor = ImageProcessing()

        self.master = master
        self.master.resizable(0, 0) # Cannot be resized in any direction
        self.master.title("Play")

        # Set up the keyboard controller for keyboard presses
        self.keyboard = Controller()
        # Global variable is set to the keys variable of this class that the program will "press"
        self.keys = keys_to_use
        # Stores the keys that are being pressed
        self.keys_pressed = []

        # If the user has not yet finished calibrating the software
        if not calibrated:
            print("Incomplete Calibration") # Displays in the console for debugging

            # Labels to give user feedback that they need to calibrate this software before playing
            self.lbl_warning = tk.Label(self.master, text="Calibration incomplete!", font=("Helvetica", 20, "bold"))
            self.lbl_warning.grid(row=0, column=0, pady=10) # Padding given to title label

            self.lbl_prompt = tk.Label(self.master, text="Close this window to return to the main menu window and press the 'Begin Calibration' button to calibrate this software", font=("Helvetica", 15))
            self.lbl_prompt.grid(row=1, column=0, padx=40, pady=50) # Will be placed underneath lbl_warning's text
        # Otherwise they have
        else:
            # Label to display the camera footage with mask applied
            self.lbl_cam = tk.Label(self.master)
            self.lbl_cam.pack() # Only widget needed on this screen
            print("Calibration has been completed")
            # Will be programmed to show camera footage with mask applied and produce the correct virtual keyboard presses
            self.main_loop()
    
    # The main loop for the image processing and gameplay
    def main_loop(self):
        # "ImageProcessing" class' "play_frame" function called with the global variables for the HSV upper and lower bounds passed as parameters
        imgtk = self.image_processor.play_frame(dir1_HSV, dir2_HSV, brake_HSV, acc_HSV)
        # Sets the attributes for the contours of each of the contour by calling this function
        self.image_processor.find_contours()

        # Now contours are found we can check the steering wheel gestures
        
        # Direction checking 
        direction = self.image_processor.check_direction()
        if direction == "LEFT":
            # Keyboard controller presses the left key (index 1 in arrow keys list)
            self.keyboard.press(self.keys[1])
            # If the left key is not in the keys that are being pressed...
            if self.keys[1] not in self.keys_pressed:
                # ... add it to the list of keys being pressed
                self.keys_pressed.append(self.keys[1])
        elif direction == "RIGHT":
            # Keyboard controller presses the right key (index 3 in arrow keys list)
            self.keyboard.press(self.keys[3])
            # If the right key is not in the keys that are being pressed...
            if self.keys[3] not in self.keys_pressed:
                # ... add it to the list of keys being pressed
                self.keys_pressed.append(self.keys[3])
        # Either direction contour(s) missing or steering straight
        else:
            # If the left key is in the list of keys that are being pressed...
            if self.keys[1] in self.keys_pressed:
                # ... remove it from the list
                self.keys_pressed.remove(self.keys[1])
                # and release that key (i.e. stop pressing it)
                self.keyboard.release(self.keys[1])

            # If the right key is in the list of keys that are being pressed...
            if self.keys[3] in self.keys_pressed:
                # ... remove it from the list
                self.keys_pressed.remove(self.keys[3])
                # and release that key
                self.keyboard.release(self.keys[3])

        # Brake checking
        is_braking = self.image_processor.check_braking() # Returns true or false
        if is_braking: 
            # Keyboard controller presses the brake key (index 2 in arrow keys list)
            self.keyboard.press(self.keys[2])
            # If the brake key is not in the keys that are being pressed...
            if self.keys[2] not in self.keys_pressed:
                # ... add it to the list of keys being pressed
                self.keys_pressed.append(self.keys[2])
        else:
            # If the brake key is in the list of keys that are being pressed...
            if self.keys[2] in self.keys_pressed:
                # ... remove it from the list
                self.keys_pressed.remove(self.keys[2])
                # and release that key
                self.keyboard.release(self.keys[2])

        # Acceleration checking
        is_accelerating = self.image_processor.check_acceleration() # Returns true or false
        if is_accelerating:
            # Keyboard controller presses the acceleration key (index 0 in arrow keys list)
            self.keyboard.press(self.keys[0])
            # If the acceleration key is not in the keys that are being pressed...
            if self.keys[0] not in self.keys_pressed:
                # ... add it to the list of keys being pressed
                self.keys_pressed.append(self.keys[0])
        else:
            # If the acceleration key is in the list of keys that are being pressed...
            if self.keys[0] in self.keys_pressed:
                # ... remove it from the list
                self.keys_pressed.remove(self.keys[0])
                # and release that key
                self.keyboard.release(self.keys[0])
        
        # Prints list of keys being pressed for debugging purposes
        print(self.keys_pressed)

        # Sets lbl_cam's imgtk to the return of the function called in previous line
        self.lbl_cam.imgtk = imgtk
        self.lbl_cam.configure(image=imgtk)
        # Makes sure to repeat this function every 10 ms to give effect of video playing (just a series of images shown at rapid speed)
        self.lbl_cam.after(10, self.main_loop)

# Class that contains the contents of the keyboard preferences window
class KeyboardPrefsWindow:

    # __init__ function to store the master and set the title of the window
    def __init__(self, master):
        self.master = master
        self.master.resizable(0, 0) # For better aesthetics
        self.master.title("Keyboard Preferences")
    
        # Title label at the top of the window
        self.lbl_title = tk.Label(self.master, text="KEYBOARD PREFERENCES", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20) # Gives title padding around the outside of the label

        # Button that will change the keys to use to WASD keys when pressed
        self.btn_WASD_keys = tk.Button(self.master, text="Use WASD keys", background="orange", font=("Helvetica", 15), width=20, height=2, command=self.change_to_WASD_keys)
        self.btn_WASD_keys.grid(row=1, column=0, pady=10) # Underneath title and has 10 pixels of padding outside the top and bottom of the button

        # Button that will change the keys to use to the arrow keys when pressed
        self.btn_arrow_keys = tk.Button(self.master, text="Use arrow keys", background="orange", font=("Helvetica", 15), width=20, height=2, command=self.change_to_arrow_keys)
        self.btn_arrow_keys.grid(row=2, column=0, pady=(10, 20))
    
    def change_to_WASD_keys(self):
        global keys_to_use
        keys_to_use = ["w", "a", "s", "d"]
        # Debugging purposes
        print(keys_to_use)
    
    def change_to_arrow_keys(self):
        global keys_to_use
        keys_to_use = [Key.up, Key.left, Key.down, Key.right]
        # Debugging purposes
        print(keys_to_use)

# Class that contains the contents of the about window
class AboutWindow:

    def __init__(self, master):
        self.master = master
        self.master.resizable(0, 0) # For better aesthetics
        self.master.title("About")

        # Title label to appear at the top of the contents of the window
        self.lbl_title = tk.Label(self.master, text="ABOUT", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=130, pady=20) # Padding to give space

        # "How to use this software" button is linked to the "open_using_software_win" function
        self.btn_using_software = tk.Button(self.master, text="How to use this software", background="orange", font=("Helvetica", 15), width=27, height=2, command=self.open_using_software_win)
        self.btn_using_software.grid(row=1, column=0, pady=10)

        # "Steering wheel requirements" button is linked to the "open_wheel_requirements_win" function
        self.btn_wheel_requirements = tk.Button(self.master, text="Steering wheel requirements", background="orange", font=("Helvetica", 15), width=27, height=2, command=self.open_wheel_requirements_win)
        self.btn_wheel_requirements.grid(row=2, column=0, pady=10)

        # "How to use your steering wheel" button is linked to the "open_using_wheel_win" function
        self.btn_using_wheel = tk.Button(self.master, text="How to use your steering wheel", background="orange", font=("Helvetica", 15), width=27, height=2, command=self.open_using_wheel_win)
        self.btn_using_wheel.grid(row=3, column=0, pady=(10, 20))
    
    # Function called to open the "How to use this software" window when the "How to use this software" button is pressed
    def open_using_software_win(self):
        # Creates new window with the top level being the master (i.e. the root)
        self.newWindow = tk.Toplevel(self.master)
        # "How to use this software" window has the self.newWindow as the master
        self.app = UsingSoftwareWindow(self.newWindow)

    # Function called to open the "Steering wheel requirements" window when the "Steering wheel requirements" button is pressed
    def open_wheel_requirements_win(self):
        # Creates new window with the top level being the master (i.e. the root)
        self.newWindow = tk.Toplevel(self.master)
        # "Steering wheel requirements" window has the self.newWindow as the master
        self.app = WheelRequirementsWindow(self.newWindow)

    # Function called to open the "How to use your steering wheel" window when the "How to use your steering wheel" button is pressed
    def open_using_wheel_win(self):
        # Creates new window with the top level being the master (i.e. the root)
        self.newWindow = tk.Toplevel(self.master)
        # "How to use your steering wheel" window has the self.newWindow as the master
        self.app = UsingWheelWindow(self.newWindow)

# Class that contains the contents of the "How to using this software" window
class UsingSoftwareWindow:

    def __init__(self, master):
        self.master = master
        self.master.resizable(0, 0) # For better aesthetics
        self.master.title("How to use this software")

        # Shows page 1 of the information to be shown
        self.page_1()
    
    # Removes information from page 2 and replaces with new content
    def page_1(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE THIS SOFTWARE", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Opens the image that will be displayed on screen
        self.img = ImageTk.PhotoImage(Image.open("main_menu_window.png"))
        # Makes a label for the image to be shown in
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0)

        # Text to use in the lbl_info variable
        info_text = "This is the main menu. To calibrate the software, \npress the 'Begin Calibration' button."
        
        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 1/6", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Next button
        self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_2)
        self.btn_next.grid(row=3, column=0, sticky="e", padx=10, pady=10)

    # Removes information from page 1 or 3 and replaces with new content
    def page_2(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE THIS SOFTWARE", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("calibration_window.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''You will see an image of you and your steering wheel. Make sure that the background
behind you is as clean as possible where there aren't too many colours. Also, make sure you have
good lighting (e.g. using your room's lights). Adjust the trackbars so that the image now only 
displays the colour specified on the button, like in the picture above. Once adjusted, press 
the button to save your colour.'''
        
        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 2/6", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Previous button
        self.btn_previous = tk.Button(self.master, text="Previous", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_1)
        self.btn_previous.grid(row=3, column=0, sticky="w", padx=10, pady=10)

        # Next button
        self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_3)
        self.btn_next.grid(row=3, column=0, sticky="e", padx=10, pady=10)
    
    # Will remove information from page 2 or 4 and replace with new content
    def page_3(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE THIS SOFTWARE", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("calibration_window2.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''Once the colour has been saved, press the "Next" button to continue to the
next stage. Repeat the process for the other colours on your steering wheel.'''
        
        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 3/6", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Previous button
        self.btn_previous = tk.Button(self.master, text="Previous", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_2)
        self.btn_previous.grid(row=3, column=0, sticky="w", padx=10, pady=10)

        # Next button
        self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_4)
        self.btn_next.grid(row=3, column=0, sticky="e", padx=10, pady=10)
    
    # Will remove information from page 3 or 5 and replace with new content
    def page_4(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE THIS SOFTWARE", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("calibration_window3.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''Once all 4 of your colours have been saved, press the "Finish Calibration" button
so that the program  knows that you have completed the calibration. Otherwise, the
program will think you haven't finished calibrating the software.'''
        
        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 4/6", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Previous button
        self.btn_previous = tk.Button(self.master, text="Previous", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_3)
        self.btn_previous.grid(row=3, column=0, sticky="w", padx=10, pady=10)

        # Next button
        self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_5)
        self.btn_next.grid(row=3, column=0, sticky="e", padx=10, pady=10)

    # Will remove information from page 4 or 6 and replace with new content
    def page_5(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE THIS SOFTWARE", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("play_window.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=50)

        # Text to use in the lbl_info variable
        info_text = '''Before you start playing, make sure to get the game you want to play 
ready. Then when you press the "Start Playing" button the window
above will show. You can place this window next to the game you wish
to play and then steer your wheel to play.'''
        
        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 5/6", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Previous button
        self.btn_previous = tk.Button(self.master, text="Previous", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_4)
        self.btn_previous.grid(row=3, column=0, sticky="w", padx=10, pady=10)

        # Next button
        self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_6)
        self.btn_next.grid(row=3, column=0, sticky="e", padx=10, pady=10)
    
    # Will remove information from page 5 and replace with new content
    def page_6(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE THIS SOFTWARE", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("keyboard_preferences_window.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''If you want to change the keys that the program uses, you
can press the "Keyboard Preferences" button on the main menu
to see this window. Here, you can press the button of the keys
you'd like to use and then close the window.'''

        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 6/6", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Previous button
        self.btn_previous = tk.Button(self.master, text="Previous", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_5)
        self.btn_previous.grid(row=3, column=0, sticky="w", padx=10, pady=10)   

# Class that contains the contents of the "Steering wheel requirements" window
class WheelRequirementsWindow:

    def __init__(self, master):
        self.master = master
        self.master.resizable(0, 0) # For better aesthetics
        self.master.title("Steering wheel requirements")

        # Title of window
        self.lbl_title = tk.Label(self.master, text="STEERING WHEEL REQUIREMENTS", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("steering_wheel.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''The colours don't have to be exactly the same as shown above, but
ensure the colours you use are all different from each other.

"Direction Colour 1" is the colour at the top of your wheel and
"Direction Colour 2" is the colour at the bottom of your wheel.

You can switch the places of the "Brake Colour" and "Acceleration
Colour" if you want.

Make sure the space taken up by each colour looks roughly like
what is pictured above.'''

        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13), justify="left")
        self.lbl_info.grid(row=2, column=0, pady=10)

# Class that contains the contents of the "How to use your steering wheel" window
class UsingWheelWindow:

    def __init__(self, master):
        self.master = master
        self.master.resizable(0, 0) # For better aesthetics
        self.master.title("How to use your steering wheel")

        # Show the first page of information when window first opens
        self.page_1()

    # Removes information from page 2 and replaces with new contents
    def page_1(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE YOUR STEERING WHEEL", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("accelerating.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''Show your acceleration colour when you want to accelerate.
In this case, the colour green is shown.'''

        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 1/5", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Next button
        self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_2)
        self.btn_next.grid(row=3, column=0, sticky="e", padx=10, pady=10)
    
    # Removes information from page 1 or 3 and replaces with new content
    def page_2(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE YOUR STEERING WHEEL", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("braking.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''Show your braking colour when you want to brake.
In this case, the colour red is shown.'''

        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 2/5", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Previous button
        self.btn_previous = tk.Button(self.master, text="Previous", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_1)
        self.btn_previous.grid(row=3, column=0, sticky="w", padx=10, pady=10) 

        # Next button
        self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_3)
        self.btn_next.grid(row=3, column=0, sticky="e", padx=10, pady=10)
    
    # Removes information from page 2 or 4 and replaces with new content
    def page_3(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE YOUR STEERING WHEEL", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("no_braking_or_accelerating.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''If you don't want to brake or accelerate, hide
those colours. In this case, neither green or red is shown.'''

        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 3/5", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Previous button
        self.btn_previous = tk.Button(self.master, text="Previous", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_2)
        self.btn_previous.grid(row=3, column=0, sticky="w", padx=10, pady=10) 

        # Next button
        self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_4)
        self.btn_next.grid(row=3, column=0, sticky="e", padx=10, pady=10)
    
    # Removes information from page 3 or 5 and replaces with new content
    def page_4(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE YOUR STEERING WHEEL", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("contours_missing.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''Make sure both direction colours are shown.
In this case, yellow is missing.'''

        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 4/5", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Previous button
        self.btn_previous = tk.Button(self.master, text="Previous", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_3)
        self.btn_previous.grid(row=3, column=0, sticky="w", padx=10, pady=10) 

        # Next button
        self.btn_next = tk.Button(self.master, text="Next", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_5)
        self.btn_next.grid(row=3, column=0, sticky="e", padx=10, pady=10)
    
    # Removes information from page 4 and replaces with new content
    def page_5(self):
        # Destroys any content that may be on the screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Needs a new title label in every page
        self.lbl_title = tk.Label(self.master, text="HOW TO USE YOUR STEERING WHEEL", font=("Helvetica", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=40, pady=20)

        # Show the new image
        self.img = ImageTk.PhotoImage(Image.open("steering.png"))
        self.lbl_img = tk.Label(self.master, image=self.img, relief="solid")
        # Puts image on screen
        self.lbl_img.grid(row=1, column=0, padx=10)

        # Text to use in the lbl_info variable
        info_text = '''Make sure when you steer, your direction colours
don't rotate past 180 degrees.'''

        # Label displaying the information
        self.lbl_info = tk.Label(self.master, text=info_text, font=("Helvetica", 13))
        self.lbl_info.grid(row=2, column=0, pady=10)

        # Label displaying what page the user is on
        self.lbl_pages = tk.Label(self.master, text="Page 5/5", font=("Helvetica", 13))
        self.lbl_pages.grid(row=3, column=0, pady=10)

        # Previous button
        self.btn_previous = tk.Button(self.master, text="Previous", background="orange", font=("Helvetica", 13), width=10, height=1, command=self.page_4)
        self.btn_previous.grid(row=3, column=0, sticky="w", padx=10, pady=10)

def main():
    root = tk.Tk() # Represents main window
    app = MainMenuWindow(root) # "root" passed in as the master
    root.mainloop() # Calls tkinter's mainloop function to make sure windows stay open

# Calls the above function
if __name__ == "__main__":
    main()
