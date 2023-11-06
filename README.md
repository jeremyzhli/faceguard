# faceguard
A simple facial recognition system for your webcam that notifies you by email when unauthorised individuals are detected.

---

### Code Analysis and Challenges
The program has several functions:
- `register_faces()`
  - This essentially 'registers' the user's face by scanning through the 'face_references' directory for a reference image and asking the user for an email address. It will then encode the image using the `face_recognition.face_encodings()` and store it in a list
  - This function will return 3 things, a list of registered faces, a list of registered names, and an email address through which the program will provide notifications
- `recognise()`
  - This is the main loop that the program will continuously run to detect and recognise faces through a live video feed from the webcam
  - It uses OpenCV to obtain a capture object from the primary video source (line 41), and it will take each individual frame and pass it to several functions to determine the location of faces in the frame (lines 49, 50), and finally run the facial recognition algorithm to determine a face confidence value (line 53-62) before displaying the frame
  - To slightly improve the performance of the program, there is a delay mechanism (line 43-45), which requires only every 1 in 3 frames to run the recognition
  - The email alert system is triggered when an unrecognised face stays in frame for 30 frames (line 60-66)
- `display_frame()`
  - This function displays each video frame on screen and also draws a rectangle around the determined face locations in the previous function
  - The rectangle will be labelled with the file name of the reference image it best matches
- `email_alert()`
  - This function creates an SMTP context using `smtplib`, logs in using a gmail account I created for this purpose and sends an email alert to the provided email address containing a simple message and a timestamp of the current time


As mentioned in the report, one of the main challenges I faced while creating this program was figuring out how OpenCV and the `face_recognition` module worked together. What helped me to understand this was going into the Github repository of the module [here](https://github.com/ageitgey/face_recognition) and reading the functions in the source code. For example, the docstring for `load_image_file()` stated that it required an RGB frame to be passed in, whereas OpenCV uses a BGR colour space. 

A minor roadblock I faced when writing the email alerts was actually the setting up of the gmail account. As of 2022, Google removed the 'Allow less secure apps' option in Google accounts, meaning software cannot sign in using the main account name and password. A workaround I eventually found on a forum was to use an app password, which required some tweaking in the Google account settings.

One of the plans I had in mind to improve the program was to rework the `register_faces()` function. Instead of having users manually put in a reference picture of themselves, the program would use the webcam to take a picture of them in the moment after a countdown. That picture would then be used in the face encodings. Unfortunately, I didn't have time to implement this change. 
