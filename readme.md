This is a simple facial recognition / identification type application built behind a flask server. The main library that we are using is face_recognition (https://github.com/ageitgey/face_recognition) that allows us to define a group of known people (folder named accordingly) and have the user upload an image of a person they are trying to identify. This small example could be expanded to include a multitude of people to reference, but for a simple demonstration we have our model checking for Barack Obama.

Inscructions:
- Simply run the flask_server.py and allow that flask server to come up.
- Go to your localhost addess, default port should be 5000 for flask.
- Simply click the file selector and choose either the included image of Elon Musk, or Barack Obama.
- Once the file is sent to the server, it runs through several methods to determine if a match is found based on the pictures of 'Known People'
- The server then redirects to a success page to give the user the results
- The server could redirect to a failure page and let you in on any exceptions that were thrown