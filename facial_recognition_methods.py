# Imports of all our libraries we'll be using.
import face_recognition as fr
import numpy as np
import cv2
import os


# Define a method to get the faces from our 'knownPeople' folder
def getKnownFaces():
    # Make a set to store the names of our people
    known = {}
    # A for loop to get each image from our 'knownPeople' folder
    for image in os.listdir("./knownPeople"):
        # Load the face into a 'face' variable
        face = fr.load_image_file("knownPeople/" + image)
        # Get the encoding of that face (into a variable)
        encoding = fr.face_encodings(face)[0]
        # Add the encoding into our set of known people
        known[image.split(".")[0]] = encoding
    # Return the set of known people
    return known


# Define a method for the input image to encode
def encodeInputImage(image):
    # Grab the face(s) from the image
    face = fr.load_image_file("./" + image)
    # Encode that face into a variable
    encodedFace = fr.face_encodings(face)[0]
    # Return our now encoded face
    return encodedFace


# Define a method to compare our input faces with our known faces
def checkFaces(input):
    # Run our method to get our known people
    faces = getKnownFaces()
    # From the set, split the values (Encoding)
    knownEncoded = list(faces.values())
    # Then split the keys (Names)
    knownNames = list(faces.keys())

    # Use OpenCV to get our input image
    image = cv2.imread(input, 1)

    # Get the location of our 'unknown' faces from our input
    unknownLocations = fr.face_locations(image)
    # Encode the information of the location of our unknown faces
    unknownEncodings = fr.face_encodings(image, unknownLocations)

    # Create a list to store our names
    faceNames = []
    faceDistances = []

    # Loop through all the known faces we have and try to figure out who they are
    for currentEncoding in unknownEncodings:
        # Check for a match with the known people
        matches = fr.compare_faces(knownEncoded, currentEncoding)
        # Set by default that we will classify this as an unknown person
        name = "Unknown"

        # Based on the closest match, name the unknown person
        distances = fr.face_distance(knownEncoded, currentEncoding)
        # Get the best match using numpy.argmin
        matchIndex = int(np.argmin(distances))
        # Check if the name exists in our known poeple
        if matches[matchIndex]:
            # If so, then change the name from currently "Unknown" to that known person
            name = knownNames[matchIndex]

        # Add the name of the person, if there was a match, we add that name.
        # Other wise, we are adding "Unknown" by default from earlier
        faceNames.append(name)
        faceDistances.append(distances)

    # Finally, we return the names of all the people we suspect to be in the image
    return faceNames, faceDistances
