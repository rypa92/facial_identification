# Imports of all our libraries we'll be using.
from flask import *
import facial_recognition_methods as frm
import os
import time

# Defining our upload folder so we can accept images from the user
UPLOAD_FOLDER = './static/images'
# Define the types of files that we want to accept (for security reasons)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Defining a variable so we can configure out current Flask application
app = Flask(__name__)
# Setting our upload folder to what we defined earlier
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Secret key needs to exist for POST methods to work from HTTP
app.secret_key = 'changed4github'


# Defining a method that check the uploaded file and verify it is acceptable
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Define a root route for our Flask application
# "What happens when we load the application?" This ..
@app.route('/')
def index():
    # Literally return our index template
    return render_template('index.html')


# Define a route for out submit method through POST with HTTP
@app.route('/submit', methods=['GET', 'POST'])
def getPicture():
    # If the request was a POST method, we go into this block
    if request.method == 'POST':
        # Grab out file from the POST method
        img_file = request.files.get('file')
        # Define a file name and make it semi-unique because we will store it temporarily
        img_name = str(time.time()) + img_file.filename
        # Quickly save the location of this image cause we're gonna use it soon
        img_loc = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        # Boom, save that image to the location
        img_file.save(img_loc)
        # Please don't break..
        try:
            # Get the results from our facial_recognition_methods.py
            results = frm.checkFaces(img_loc)
            # Delete the file as we won't need it anymore
            os.remove(img_loc)
            # Make sure that results somehow doesn't end up null
            if results is not None:
                # Get the face identity from the results variable
                faceResult = results[0][0]
                # Get the distance match from the results variable
                distResult = results[1][0][0]
                # Check to make sure Obama is the person we got from the results
                if "Obama" in faceResult:
                    # Create a message to pass to the HTML page
                    flash('Based on what I know Barack Obama looks like ..')
                    flash('I say there is a(n) {0:.2f}% match here'
                          # Do some math to get a pretty percentage
                          .format(100 - (distResult * 100)))
                    # Return our success page
                    # Success referring to no errors, more like a results page.
                    return render_template('/success.html')
                # Since Obama wasn't in our results, we failed our mission
                else:
                    # Create a message to show on the HTML page
                    flash('Nope, no Obama in there!')
                    # Return the success page, as in we successfully checked the image
                    return render_template('/success.html')
        # Welp, we messed up, so we catch that
        except Exception as e:
            # Create a message to pass to our HTML
            flash(e)
            # Return our failure page. *sulk*
            return render_template('/failure.html')


# Annnnnnnnnnnnd, go!
if __name__ == "__main__":
    app.run()
